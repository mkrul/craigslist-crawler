from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import requests
import json
import time
import os

def search_craigslist(event, lambda_context):
    locations_list = [
        'asheville', 'boone', 'charlotte', 'eastnc', 'fayetteville', 'hickory', 
        'jacksonville', 'outerbanks', 'raleigh', 'wilmington', 'winstonsalem'
    ]

    keywords = [
      "plex", "quad", "fix", "flip", "invest", "handy", "multi", "unit", "rehab", "rental"
    ]

    ignore_list = [
        "townhome", "hardmoneylender", "land", "lookingfor", "loan", "gated", 
        "condo", "townhouse", "newhome", "charming", "waterfront", "beach",
        "mountain", "club", "acreage", "buildlot", "newbuild", "acreslot",
        "acrelot", "timeshare", "dreamhome", "dreamhouse"
    ]

    price_min = 0
    price_max = 250000

    password = os.environ['db_password']
    connection = f"mongodb+srv://test:{password}@cluster0-uadok.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(connection)
    db = client["craigslist"]

    for location in locations_list:
        url = f"https://{location}.craigslist.org/d/real-estate/search/rea"
        listing = search_listings(url)
        search_results = listing.find_all("a", { "class": "result-title" })

        for result in search_results:
            title = result.contents[0].replace("&", " ")

            # downcase and remove white space
            result_string = result.contents[0].lower().replace(" ", "")

            # check listing against blacklist of ignored words
            ignored_words = any(word in result_string for word in ignore_list)

            # check listing against whitelist of allowed words
            if any(word in result_string for word in keywords) and ignored_words == False:
                listing = create_listing(title, result["href"])
                listing_count = db["listings"].count_documents({
                    "title": listing["title"],
                    "location": listing["location"],
                    "price": listing["price"],
                })

                # check to see if listing price falls between min and max price and that the document doesn't already exist
                if listing_count == 0 and int(listing["price"]) >= price_min and int(listing["price"]) <= price_max:
                    print (f"Creating new listing: {listing['title']}")
                    db["listings"].insert_one(listing)
            else:
                pass

def search_listings(url):
    retries = 0
    wait = 2
    success = False
    response = ''

    while not success and retries < 3:
        try:
            response = requests.get(url)
            time.sleep(2)
            success = True
        except Exception as e:
            wait *= wait
            time.sleep(wait)
            retries += 1
            if retries >= 3:
                log_error("Retry limit exceeded", e)
    
    response_str = response.content.decode("utf-8")
    return BeautifulSoup(response_str, "html.parser")

def log_error(msg, e):
    print(msg)
    print(e)

def get_price(listing):
    try:
        return listing.find("span", {"class": "price"}).text.replace("$", "")
    except Exception as e:
        log_error("Price missing or invalid", e)
        return "0"

def get_location(listing):
    geocode_url = "https://api.opencagedata.com/geocode/v1/"
    api_key = os.environ['opencagedata_api_key']

    try:
        # use latitude / longitude to get exact property address
        map_data = listing.find("meta", { "name": "geo.position"} )["content"].partition(";")
        opencagedata_uri = f"{geocode_url}json?key={api_key}&q={map_data[0]}%2C{map_data[2]}"
        geolocations = requests.get(opencagedata_uri)
        location_data = json.loads(geolocations.text)
        return location_data['results'][0]['formatted'].replace(", United States of America", "")
    except Exception as e:
        log_error("Geocode location missing or invalid", e)
        return fallback_location(listing)

def fallback_location(listing):
    try:
        placename = listing.find("meta", { "name": "geo.placename"} )["content"]
        region = listing.find("meta", { "name": "geo.region"} )["content"].partition("-")[2]
        return f"{placename}, {region}"
    except Exception as e:
        log_error("Fallback location missing or invalid", e)
        return ""

def get_description(listing):
    try:
        return listing.find("meta", { "name": "description"} )["content"]
    except Exception as e:
        log_error("Description not found or invalid", e)
        return ""

def get_listed_date(listing):
    try:
        return listing.time.attrs["datetime"][:10]
    except Exception as e:
        log_error("Listed date missing or invalid", e)
        return ""

def get_image(listing):
    try:
        return listing.find("meta", property="og:image")["content"]
    except Exception as e:
        log_error("Image missing or invalid", e)
        return ""

def get_created_at():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def create_listing(title, url):
    print(f"Making GET request to {url}")
    listing = search_listings(url)

    price = get_price(listing)
    location = get_location(listing)
    description = get_description(listing)
    listed_date = get_listed_date(listing)
    image = get_image(listing)
    created_at = get_created_at()

    return {
        "title": title,
        "price": price,
        "location": location,
        "description": description,
        "listed_date": listed_date,
        "created_at": created_at,
        "url": url,
        "image": image
    }
