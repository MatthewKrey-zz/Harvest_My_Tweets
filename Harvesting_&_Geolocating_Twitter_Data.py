# Create easy access to Twitter API 
from twython import Twython

API_KEY = # type your API_KEY
API_SECRET = # type your API_SECRET
ACCESS_TOKEN = # type your ACCESS_TOKEN
ACCESS_TOKEN_SECRET = # type your ACCESS_TOKEN_SECRET

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 

# Get some of your status updates from your timeline 

temp = twitter.get_user_timeline()

# Test 

twitter.get_lastfunction_header('x-rate-limit-remaining')

# Beware! If you are checking your code into GitHub or another cloud-based version control solution,
# check whether the repository is public or private. All free repositories on GitHub are public. 
# If your repository is public, the world will have access to your secret Twitter API keys. 
# NOTE: bitbucket.org provides private repositories for free. 

def twitter_oauth_login():
    API_KEY = # type your API_KEY
    API_SECRET = # type your API_SECRET
    ACCESS_TOKEN = # type your ACCESS_TOKEN
    ACCESS_TOKEN_SECRET = # type your ACCESS_TOKEN_SECRET
    
    twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return(twitter)

# Determine who your friends are.
# Determine who your followers are.
# Determine how much overlap there is in each group.

twitter = twitter_oauth_login()

friends_ids = twitter.get_friends_ids(count=5000)
friends_ids = friends_ids['ids']

followers_ids = twitter.get_followers_ids(count=5000)
followers_ids = followers_ids['ids']

# How many Twitter followers and friends do you have?

len(friends_ids), len(followers_ids)

# Examine some properties of your Twitter followers and friends 

friends_set = set(friends_ids)
followers_set = set(followers_ids)

print('Number of Twitter users who either are our friend or follow you (union):')

print(len(friends_set.union(followers_set)))

print('Number of Twitter users who follow you and are your friend (intersection):')
print(len(friends_set & followers_set))

print("Number of Twitter users who follow you that you don't follow (set difference):")
print(len(followers_set - friends_set))

# Never thought Set Notation would be used outside of Math class again?
# BOOM! Unite the set of friends' IDs with the followers' IDs to determine the total set of unique IDs of 
# Twitter users that either follow or are followed by us.

(friends_set | followers_set)
(set(friends_ids + followers_ids))

# First, create a function that will manage pulling Twitter profiles 

def pull_users_profiles(ids):
    users = []
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        users += twitter.lookup_user(user_id=batch)
        print(twitter.get_lastfunction_header('x-rate-limit-remaining'))
    return (users)

# Pull profiles of both friends and followers 

friends_profiles = pull_users_profiles(friends_ids)
followers_profiles = pull_users_profiles(followers_ids)

# Use a list comprehension to extract all of the friends' screen names from the profiles and check whether everything works 

friends_screen_names = [p['screen_name'] for p in friends_profiles]

# We should see a list of our friends' Twitter names! 

print(friends_screen_names)

print(twitter.get_lastfunction_header('x-rate-limit-remaining'))

friends_screen_names = [p['screen_name'] for p in friends_profiles if 'screen_name' in p]

import time 
import math 

def pull_users_profiles_limit_aware(ids):
    users = []
    start_time = time.time()
    # Look up users 
    for i in range(o, len(ids), 10):
        batch = ids[i:i + 10]
        users += twitter.lookup_user(user_id=batch)
        calls_left = float(twitter.get_lastfunction_header('x-rate-limit-remaining'))
        time_remaining_in_window = rate_limit_window - (time.time() - start_time)
        sleep_duration = math.ceil(time_remaining_in_window/class_left)
        print('Sleeping for: ' + str(sleep_duration) + ' seconds; ' +
              str(calls_left) + 'API calls remaining')
        time.sleep(sleep_duration)
        
    return (users)

# We need to be able to store previously retrieved JSON data and 
# We need to be able to load the previously retrieved JSON data back into the Python interpreter's memory 

import json 

def save_json(filename, data):
    with open(filename, 'wb') as outfile:
        json.dump(data, outfile)

def load_json(filename):
    with open(filename) as infile:
        data = json.load(infile)
    return data 

# Save friends' JSON-based Twitter profiles to the disk 

fname = "test_friends_profiles.json"
save_json(fname, friends_profiles)

test_reload = load_json(fname)
print(test_reload[0])

import pymongo

host_string = "mongodb://127.0.0.1"
port = 27017
mongo_client = pymongo.MongoClient(host_string, port)

# Get a reference to the mongodb database 'test'

mongo_db = mongo_client['test']

# Get a reference to the 'user profiles' collection in the 'test' database 

user_profiles_collection = mongo_db['user profiles']

user_profiles_collection.insert(friends_profiles)
user_profiles_collection.insert(followers_profiles)

# Let's find out where some of our Tweets are coming from... 

fname = 'test_friends_profiles.json'
load_json(fname)

geo_enabled = [p['geo_enabled'] for p in friends_profiles]
geo_enabled.count(1)

location = [p['location'] for p in friends_profiles]
location.count('')

print(set(location))

time_zone = [p['time_zone'] for p in friends_profiles]
time_zone.count(None)

print(set(time_zone))

status_geo = [p['status']['geo'] for p in friends_profiles if ('status' in p and p['status']['geo'] is not None)]

if status_geo: print status_geo[0]
    
len(status_geo)

status_geo = []
status_geo_screen_names = []
for fp in friends_profiles:
    if ('status' in fp and fp ['status']['geo'] is not None and 'screen_name' in fp):
        status_geo.append(fp['status']['geo'])
        status_geo_screen_names.append(fp['screen_name'])

# Use folium to map Tweets of user profiles that have Location enabled on Twitter 

import folium
from itertools import izip

map = folium.Map(location= [48, -102], zoom_start=3)

for sg, sn in izip(status_geo, status_geo_screen_names):
    map.simple_marker(sg['coordinates'], popup=str(sn))
    map.circle_marker(location=[10, 20], radius=10000,
                  popup='My Popup Info', line_color='#3186cc',
                  fill_color='#3186cc', fill_opacity=2.0)
    
map.create_map(path='us_states.html')