import requests
import pandas as pd
import time
import os

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



# Api-Key from google devmode,Youll have to get your api Key from the Google developers console, 
# link for the same has been provided below for further info on this you can refer my blog

#API_Key = "Get your API Key from - https://console.cloud.google.com/apis/dashboard"
           
API_Key = "DIsdsdFss93FJdsd8c9sJHD7dddYGkhd98Ffjbd " #--your Key will look like this
pageToken = ""

#path of the chrome webdriver local
chrome_path = r"C:\SeleniumDriver\chromedriver.exe"




#we're connecting to the Chromedriver for selenium to get the html response

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()


##getting the urls of the trnding music videos
driver.get("https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D")
user_data = driver.find_elements(by=By.XPATH,value = '//ytd-video-renderer/div//h3/a') ##fetch urls by X.path
trending_video_links = []
for i in user_data:
    trending_video_links.append(i.get_attribute('href'))

print("\nNo of videos on Trending",len(trending_video_links))
print("\nurl examples")
print(trending_video_links[:5])



##we'll define a function to clean urls for video id of each video & get the response
def get_response_data (urls):
    response_data=[]
    for url in urls:
        
        videoid = url.split("watch?v=")[-1].split("&list")[0]

        #URL to get the data/stats of Any video on youtube
        videostats_url = "https://www.googleapis.com/youtube/v3/videos?id="+videoid+"&part=snippet,statistics&key="+API_Key
        response_data.append(requests.get(videostats_url).json())
        
    return response_data


response_data = get_response_data(trending_video_links)






#Here from the json returned by the sending the request,we'll fetch the required data that's relevant for us

title = [];channel=[]; released=[]; viewcount=[]; likecount=[]; commentscount=[];
for video_data in response_data:
    if video_data['items'][0]['kind'] ==  "youtube#video":
        
        title .append(video_data['items'][0]['snippet']['title'])

        channel.append(video_data['items'][0]['snippet']['channelTitle'])

        released .append(video_data['items'][0]['snippet']['publishedAt'])

        viewcount .append(video_data['items'][0]['statistics']['viewCount'])

        likecount .append(video_data['items'][0]['statistics']['likeCount'])

        commentscount .append(video_data['items'][0]['statistics']['commentCount'])
        
        
        
        
  
  Videodf = pd.DataFrame({"Title":title,"Channel Name":channel,
                        "Release Date-Time":released,"Views":viewcount,"Likes":likecount,
                        "No of Comments":commentscount,"url":trending_video_links})

Videodf



import os
Videodf.to_csv(os.path.join(r'C:\Users\ranap\OneDrive\Desktop\Crawling & API\Youtube Extraction',
                            r'Youtube trending music.csv'),index=False)
        
        
        
        
        



























