
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime


def extract():
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    url='https://10times.com/india?month=july'
    result=requests.get(url,headers)
    soup=BeautifulSoup(result.content,"html.parser")
   
    return soup

def transform(soup):
    divs=soup.find_all('tr', class_ = 'event-card')
    print('Loading',end = '')
    for item in divs:
        try:
            description=item.find('div', class_='small text-wrap text-break').getText().strip()
            href_link=item.find('a',attrs={'href': re.compile("^https://")}) #getting link from each card
            link=href_link.get('href')
    
            # fecting data from other website

            urlx=link
            resultx=requests.get(urlx)
            soupx=BeautifulSoup(resultx.content,"html.parser")
            event_name=soupx.find('input', id='event_name').get('value').strip()
            LatLng=soupx.find('input', id='geoLatLng').get('value')
            date=soupx.find('input', id='event_date').get('value').strip()
            #date=datetime.datetime.strptime(date, '%a %b %d %Y').strftime('%d/%m/%Y')
            #time=soupx.find('tr',id="hvrout1").getText()
            cityName=soupx.find('input', id='cityName').get('value')
            countryName=soupx.find('input', id='countryName').get('value')
            venueName=soupx.find('input', id='venueName').get('value')
            address=soupx.find('section',id='map_dirr').getText('span').strip('Venue Map & Directionsspan').strip()
            eventID=soupx.find('input', id='eventID').get('value')
            venueId=soupx.find('input', id='venueId').get('value')
            event={'Event':event_name,'EventID':eventID,'Date':date,'Description':description,'Latitude and Longitude':LatLng,'Country':countryName,'City':cityName,'VenueName':venueName,'VenueID':venueId,'Address':address,'Website Link':link}
            eventList.append(event)
            print('.',end = '')
        except: continue
        
    return 

#main
eventList=[]
l=len(eventList)
c=extract()
transform(c)
df=pd.DataFrame(eventList)
print(df.head)
df.to_csv('EventList.csv')
df.to_json('EventList.json')




