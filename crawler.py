import telegram
import praw
import random
import itertools
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import websocket
import requests
import json
import time
import os
import pdb

def search_craigslist():
    locations_list = [
        'auburn', 'bham', 'dothan', 'shoals', 'gadsden', 'huntsville', 'mobile', 'montgomery',
        'tuscaloosa', 'anchorage', 'fairbanks', 'kenai', 'juneau', 'flagstaff', 'mohave', 'phoenix',
        'prescott', 'showlow', 'sierravista', 'tucson', 'yuma', 'fayar', 'fortsmith', 'jonesboro',
        'littlerock', 'texarkana', 'bakersfield', 'chico', 'fresno', 'goldcountry', 'hanford', 'humboldt',
        'imperial', 'inlandempire', 'losangeles', 'mendocino', 'merced', 'modesto', 'monterey', 'orangecounty',
        'palmsprings', 'redding', 'sacramento', 'sandiego', 'sfbay', 'slo', 'santabarbara', 'santamaria', 'siskiyou',
        'stockton', 'susanville', 'ventura', 'visalia', 'yubasutter', 'boulder', 'cosprings', 'denver', 'eastco',
        'fortcollins', 'rockies', 'pueblo', 'westslope', 'newlondon', 'hartford', 'newhaven', 'nwct', 'delaware',
        'washingtondc', 'miami', 'daytona', 'keys', 'fortlauderdale', 'fortmyers', 'gainesville', 'cfl',
        'jacksonville', 'lakeland', 'miami', 'lakecity', 'ocala', 'okaloosa', 'orlando', 'panamacity', 'pensacola',
        'sarasota', 'miami', 'spacecoast', 'staugustine', 'tallahassee', 'tampa', 'treasure', 'miami', 'albanyga',
        'athensga', 'atlanta', 'augusta', 'brunswick', 'columbusga', 'macon', 'nwga', 'savannah', 'statesboro',
        'valdosta', 'honolulu', 'boise', 'eastidaho', 'lewiston', 'twinfalls', 'bn', 'chambana', 'chicago', 'decatur',
        'lasalle', 'mattoon', 'peoria', 'rockford', 'carbondale', 'springfieldil', 'quincy', 'bloomington',
        'evansville', 'fortwayne', 'indianapolis', 'kokomo', 'tippecanoe', 'muncie', 'richmondin', 'southbend',
        'terrehaute', 'ames', 'cedarrapids', 'desmoines', 'dubuque', 'fortdodge', 'iowacity', 'masoncity', 'quadcities',
        'siouxcity', 'ottumwa', 'waterloo', 'lawrence', 'ksu', 'nwks', 'salina', 'seks', 'swks', 'topeka', 'wichita', 'bgky',
        'eastky', 'lexington', 'louisville', 'owensboro', 'westky', 'batonrouge', 'cenla', 'houma', 'lafayette', 'lakecharles',
        'monroe', 'neworleans', 'shreveport', 'maine', 'annapolis', 'baltimore', 'easternshore', 'frederick', 'smd', 'westmd',
        'boston', 'capecod', 'southcoast', 'westernmass', 'worcester', 'annarbor', 'battlecreek', 'centralmich', 'detroit',
        'flint', 'grandrapids', 'holland', 'jxn', 'kalamazoo', 'lansing', 'monroemi', 'muskegon', 'nmi', 'porthuron', 'saginaw',
        'swmi', 'thumb', 'up', 'bemidji', 'brainerd', 'duluth', 'mankato', 'minneapolis', 'rmn', 'marshall', 'stcloud', 'gulfport',
        'hattiesburg', 'jackson', 'meridian', 'northmiss', 'natchez', 'columbiamo', 'joplin', 'kansascity', 'kirksville', 'loz',
        'semo', 'springfield', 'stjoseph', 'stlouis', 'billings', 'bozeman', 'butte', 'greatfalls', 'helena', 'kalispell', 'missoula',
        'montana', 'grandisland', 'lincoln', 'northplatte', 'omaha', 'scottsbluff', 'elko', 'lasvegas', 'reno', 'nh', 'cnj',
        'jerseyshore', 'newjersey', 'southjersey', 'albuquerque', 'clovis', 'farmington', 'lascruces', 'roswell', 'santafe',
        'albany', 'binghamton', 'buffalo', 'catskills', 'chautauqua', 'elmira', 'fingerlakes', 'glensfalls', 'hudsonvalley',
        'ithaca', 'longisland', 'newyork', 'oneonta', 'plattsburgh', 'potsdam', 'rochester', 'syracuse', 'twintiers', 'utica',
        'watertown', 'asheville', 'boone', 'charlotte', 'eastnc', 'fayetteville', 'greensboro', 'hickory', 'onslow',
        'outerbanks', 'raleigh', 'wilmington', 'winstonsalem', 'bismarck', 'fargo', 'grandforks', 'nd', 'akroncanton', 'ashtabula',
        'athensohio', 'chillicothe', 'cincinnati', 'cleveland', 'columbus', 'dayton', 'limaohio', 'mansfield', 'sandusky', 'toledo',
        'tuscarawas', 'youngstown', 'zanesville', 'lawton', 'enid', 'oklahomacity', 'stillwater', 'tulsa', 'bend', 'corvallis', 'eastoregon',
        'eugene', 'klamath', 'medford', 'oregoncoast', 'portland', 'roseburg', 'salem', 'altoona', 'chambersburg', 'erie', 'harrisburg',
        'lancaster', 'allentown', 'meadville', 'philadelphia', 'pittsburgh', 'poconos', 'reading', 'scranton', 'pennstate', 'williamsport',
        'york', 'providence', 'charleston', 'columbia', 'florencesc', 'greenville', 'hiltonhead', 'myrtlebeach', 'nesd', 'csd', 'rapidcity',
        'siouxfalls', 'sd', 'chattanooga', 'clarksville', 'cookeville', 'jacksontn', 'knoxville', 'memphis', 'nashville',
        'tricities', 'abilene', 'amarillo', 'austin', 'beaumont', 'brownsville', 'collegestation', 'corpuschristi', 'dallas',
        'nacogdoches', 'delrio', 'elpaso', 'galveston', 'houston', 'killeen', 'laredo', 'lubbock', 'mcallen', 'odessa', 'sanangelo',
        'sanantonio', 'sanmarcos', 'bigbend', 'texoma', 'easttexas', 'victoriatx', 'waco', 'wichitafalls', 'logan', 'ogden', 'provo',
        'saltlakecity', 'stgeorge', 'burlington', 'charlottesville', 'danville', 'fredericksburg', 'norfolk', 'harrisonburg',
        'lynchburg', 'blacksburg', 'richmond', 'roanoke', 'swva', 'winchester', 'bellingham', 'kpr', 'moseslake', 'olympic',
        'pullman', 'seattle', 'skagit', 'spokane', 'wenatchee', 'yakima', 'charlestonwv', 'martinsburg', 'huntington',
        'morgantown', 'wheeling', 'parkersburg', 'swv', 'wv', 'appleton', 'eauclaire', 'greenbay', 'janesville', 'racine',
        'lacrosse', 'madison', 'milwaukee', 'northernwi', 'sheboygan', 'wausau', 'wyoming', 'micronesia', 'puertorico', 'virgin',
        'brussels', 'bulgaria', 'zagreb', 'copenhagen', 'bordeaux', 'rennes', 'grenoble', 'lille', 'loire', 'lyon', 'marseilles',
        'montpellier', 'cotedazur', 'rouen', 'paris', 'strasbourg', 'toulouse', 'budapest', 'reykjavik', 'dublin', 'luxembourg',
        'amsterdam', 'oslo', 'bucharest', 'moscow', 'stpetersburg', 'ukraine', 'bangladesh', 'micronesia', 'jakarta', 'tehran',
        'baghdad', 'haifa', 'jerusalem', 'telaviv', 'ramallah', 'kuwait', 'beirut', 'malaysia', 'pakistan', 'dubai', 'vietnam',
        'auckland', 'christchurch', 'wellington', 'buenosaires', 'lapaz', 'belohorizonte', 'brasilia', 'curitiba', 'fortaleza',
        'portoalegre', 'recife', 'rio', 'salvador', 'saopaulo', 'caribbean', 'santiago', 'colombia', 'costarica', 'santodomingo',
        'quito', 'elsalvador', 'guatemala', 'managua', 'panama', 'lima', 'puertorico', 'montevideo', 'caracas', 'virgin', 'cairo',
        'addisababa','accra','kenya','casablanca','tunis'
    ]

    connection = f"mongodb+srv://mkrul:b!gdumbd0gwithmongodb@cluster0.uadok.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection)
    db = client["craigslist"]
    random.shuffle(locations_list)
    reddit = praw.Reddit('puppysearch')

    for location in itertools.cycle(locations_list):
        search(location, 'sss', db, reddit)
        search(location, 'pet', db, reddit)
        search(location, 'pas', db, reddit)

def search(location, path, db, reddit):
    keywords = [
      'pitbull', 'pittbull' 'pit bull', 'pitt bull', 'american bully', 'american bulldog', 'xl bullies'
      'xl bully', 'xl bulldog', 'staffie', 'pocket bully', 'exotic bully', 'bullys', 'xl babies',
      'exotic bullies', 'pocket bullies', 'bullies', 'xl bulley', 'pocket bullys', 'micro bullies',
      'micro bullies', 'micro bulleys', 'pocket bullie', 'apbt', 'rednose', 'bluenose',
      'pit/bully', 'pitbull/bully', 'american bulldog', 'xl bulldog', 'xl bullie'
    ]

    ignore_list = [
        'concert', 'tickets', 'weldar', 'tailgate', 'camouflage', 'truck', 'dump truck', 'recorder',
        'pizza oven', 'head banger ball', 'head bangers ball', 'bathroom sink', 'road base',
        'battery charger', 'battery and charger', 'hairband', 'necklace', 'tools', 'dump trailer',
        'dinnerware', 'headbands', 'pizza restaurants', 'cratsman', 'craftsman', 'star wars',
        'dewalt', 'salad', 'basket', 'snowman', 'plate', 'dinnerware', 'headband', 'head band', 'hair band',
        "can't stop us now", 'cant stop us now', 'bully dog gt', 'national champions', 'fire wood',
        'georgia bulldogs', 'diesel gauge', 'collectable', 'collectible', 'cigar', 'bosch'
    ]

    url = f"https://{location}.craigslist.org/search/{path}"
    print(f'making request to {url}')
    record = send_request(url)
    search_results = record.find_all("a", { "class": "result-title" })

    for result in search_results:
        title = result.contents[0].replace("&", " ")
        description = get_description(record)

        # downcase and remove white space
        result_string = result.contents[0].lower() + description

        # check record against blacklist of ignored words
        ignored_words = any(word in result_string for word in ignore_list)

        # check record against whitelist
        if any(word in result_string for word in keywords) and ignored_words == False:
            record = initialize_record(reddit, db, title, result["href"])
            if record == None:
                pass

            record_count = db["records"].count_documents({
                "url": url
            })

            # check to see if the document already exists
            if record_count == 0:
                print (f"Creating new record: {record['title']}")
                post_record_to_telegram(title, result["href"])
                submission = post_record_to_reddit(reddit, title, result["href"])
                record["shortlink"] = submission.shortlink
                record["removed"] = 0
                db["records"].insert_one(record)
        else:
            pass

def send_request(url):
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
                break

    response_str = response.content.decode("utf-8")
    return BeautifulSoup(response_str, "html.parser")

def initialize_record(reddit, db, title, url):
    record = send_request(url)

    # check to see if post has been removed
    has_been_removed = record.find("span", {"id": "has_been_removed"})
    if has_been_removed:
        cleanup_reddit_post(reddit, db, url)
        return None
    else:
        image = get_image(record)
        return {
            "title": title,
            "url": url,
            "image": image
        }

def get_image(record):
    try:
        return record.find("meta", property="og:image")["content"]
    except Exception:
        return ""

def get_description(record):
    try:
        return record.find_all("section", { "id": "postingbody" })[0].text.strip()
    except Exception:
        return ""

def log_error(msg, e):
    print(msg)
    print(e)

def post_record_to_reddit(reddit, title, url):
    submission = reddit.subreddit('puppysearch').submit(title, url)

    return submission

def cleanup_reddit_post(reddit, db, url):
    record = db.records.find({"url": url})

    if record:
        # remove post from reddit and mongo db
        print(f'Cleaning up post for {url}')
        db.records.find_one_and_update({"url": url}, {"$set": {"removed": 1}})
        reddit.submission(record["shortlink"]).delete()

# def test():
#     api_token = '5790809926:AAE6d_R7k5A70HpEhf6d4GDw_et57oBbi9o'
#     chat_id = '-1001884619259'
#     api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'
#     requests.post(api_url, json={'chat_id': chat_id, 'text': 'test'})

def post_record_to_telegram(title, url):
    api_token = '5790809926:AAE6d_R7k5A70HpEhf6d4GDw_et57oBbi9o'
    chat_id = '-1001884619259'
    api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'

    requests.post(api_url, json={'chat_id': chat_id, 'text': url})

search_craigslist()