import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from selenium import webdriver
import time
import numpy as np
import requests
import sys
import math
import time
from bs4 import BeautifulSoup
import functools
import csv
import pandas as pd

path = "/home/tony/Data_Science_Project/"
youtuber_list = pd.read_csv(path + 'youtuber.csv')
#youtuber_list


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = path + "client_secret.json"
def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client = get_authenticated_service()


def print_response(response):
    print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
    resource = {}
    for p in properties:
        # Given a key like "snippet.title", split into "snippet" and "title", where
        # "snippet" will be an object and "title" will be a property in that object.
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]

            # For properties that have array values, convert a name like
            # "snippet.tags[]" to snippet.tags, and set a flag to handle
            # the value as an array.
            if key[-2:] == '[]':
                key = key[0:len(key)-2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                # Leave properties without values out of inserted resource.
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                # For example, the property is "snippet.title", but the resource does
                # not yet have a "snippet" object. Create the snippet object here.
                # Setting "ref = ref[key]" means that in the next time through the
                # "for pa in range ..." loop, we will be setting a property in the
                # resource's "snippet" object.
                ref[key] = {}
                ref = ref[key]
            else:
                # For example, the property is "snippet.description", and the resource
                # already has a "snippet" object.
                ref = ref[key]
    return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


category_id_to_string = {2:'Autos_and_Vehicles',
    1:'Film_and_Animation',
    10:'Music',
    15:'Pets_and_Animals',
    17:'Sports',
    18:'Short_Movies',
    19:'Travel_and_Events',
    20:'Gaming',
    21:'Videoblogging',
    22:'People_and_Blogs',
    23:'Comedy',
    24:'Entertainment',
    25:'News_and_Politics',
    26:'Howto_and_Style',
    27:'Education',
    28:'Science_and_Technology',
    29:'Nonprofits_and_Activism',
    30:'Movies',
    31:'Anime_and_Animation',
    32:'Action_and_Adventure',
    33:'Classics',
    34:'Comedy',
    35:'Documentary',
    36:'Drama',
    37:'Family',
    38:'Foreign',
    39:'Horror',
    40:'Sci-Fi_and_Fantasy',
    41:'Thriller',
    42:'Shorts',
    43:'Shows',
    44:'Trailers'
}



def videos_info_by_id(client, today, **kwargs):
    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.videos().list(
        **kwargs
    ).execute()
    
    attributes = []
    
    title = response['items'][0]['snippet']['title']
    
    
    comments_count = 0
    likes = 0
    dislikes = 0
    views = 0
    
    try:
        views = response['items'][0]['statistics']['viewCount']
    except:
        print('No views')    
    
    try:
        likes = response['items'][0]['statistics']['likeCount']
    except:
        print('No likeCount') 
        
    try:
        dislikes = response['items'][0]['statistics']['dislikeCount']
    except:
        print('No dislikeCount')   
        
    try:
        comments_count = response['items'][0]['statistics']['commentCount']
    except:
        print('No commentCount')   
        
    release_date = response['items'][0]['snippet']['publishedAt']
    release_date = release_date[:10]
    category_id = int(response['items'][0]['snippet']['categoryId'])
    category = ""
    if category_id in category_id_to_string:
        category = category_id_to_string[category_id]
        
    start_date = release_date
    end_date = today
    start_sec = time.mktime(time.strptime(start_date,'%Y-%m-%d'))
    end_sec = time.mktime(time.strptime(end_date,'%Y-%m-%d'))
    video_exist_day = int((end_sec - start_sec)/(24*60*60))
    description =  response['items'][0]['snippet']['description']   
    
    attributes.append(title)
    attributes.append(views)
    attributes.append(release_date)
    attributes.append(video_exist_day)
    attributes.append(likes)
    attributes.append(dislikes)
    attributes.append(category)
    attributes.append(comments_count)
    attributes.append(description)
    
    return attributes
       
with open(path + 'all_videos.csv', 'w+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User_Name', 'Link', 'Uploads', 'Subscribers', 'Total_Video_Views', 'Country', \
                        'Channel_Type', 'User_Created_Date', "Today_Date", 'User_Exist_Days', \
                        'Video_Link', 'Title', 'Views', 'Release_date', 'Video_exist_day', 'Likes', 'Dislikes', \
                        'Category', 'Comments_count', 'Discription'])
    
    counter = 0  
    for row in youtuber_list.iterrows():
        # for debug
        counter += 1
        if counter >=101:
            continue
        
        
        
        youtuber_videos_info = [] # record this youtuber all attributes
        base_attributes = [] # record youtuber base info wihtout video info
        index, data = row
        for i in range(0, len(data.values)):
            base_attributes.append(data.values[i])
        today = data.values[8]
        
        uploads = int(data.values[2])
        if uploads <= 6000 or uploads >=10000:
            continue 
            
        # Get the video page of channel
        url = data.values[1] + "/videos"
        print ("This youtuber video channel = ", url)
    
        '''
        ######################################################################################################
            Scroll down to the bottom of page to find all vidoes link
        ######################################################################################################
        '''
        driver = webdriver.Chrome(path + "chromedriver")
        driver.get(url)
    
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
    
            # Wait to load page
            time.sleep(2.0)
    
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight;")
    
    
            if new_height == last_height:
                break
            last_height = new_height
    
        print("Arrive Bottom")
    
        page_source = driver.page_source
        
        driver.close()
        
        # Get all videos links
        page_soup = BeautifulSoup(page_source, 'html.parser')
        a_class = page_soup.find_all('a', {"id":"thumbnail"})
    
        
        '''
        ######################################################################################################
            Find the 
            Video_Link, Title, Views, Release_date, Video_exist_day, Likes, Dislikes, 
            Category, Comments_count, Discription 
            in the video
        ######################################################################################################
        '''
        # Get all link url
        for link in a_class:
            base_attributes_cp = base_attributes.copy()
            video_id = link.get('href')
            print ('https://www.youtube.com'+video_id)
            base_attributes_cp.append('https://www.youtube.com'+video_id)
            video_id = video_id[9:]
            #print (video_id)
            
            video_attributes = videos_info_by_id(client, today, 
                          part='snippet,contentDetails,statistics',
                          id=video_id)
            
            youtuber_videos_info.append(base_attributes_cp + video_attributes)
            #print(base_attributes_cp + video_attributes)
        '''
        ######################################################################################################
            Wrtie the the all_videos.csv file
        ######################################################################################################
        '''    
        print("Write Data")
        for i in range(len(youtuber_videos_info)):
            decode = []
            for info in youtuber_videos_info[i]:
                if type(info) == str:
                    decode.append(info.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
                else:
                    decode.append(info)
            #print(decode)
            writer.writerow(decode)
        
        
print("Done")











































