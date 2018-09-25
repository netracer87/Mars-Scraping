# Import necessary libraries
from bs4 import BeautifulSoup as bs 
import requests
from splinter import Browser
import os 
from pprint import pprint
import pandas as pd 
import time
import urllib

def init_browser():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)

def close_browser(Browser):
    Browser.quit()

def scrape_news():
    browser = init_browser()

    # scrape for news title/paragraph on Mars
    news_site_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_site_url)

    news_html = browser.html
    soup = bs(news_html, 'html.parser')

    subjects = soup.find_all('div', class_='list_text')
    
    title = []
    paragraph = []
    for subject in subjects:
        title_ = subject.find('div', class_= 'content_title')
        paragraph_ = subject.find('div', class_= 'article_teaser_body')
        title.append(title_)
        paragraph.append(paragraph_)
    news_title = title[0].text
    news_p = paragraph[0].text

    news_data = {'news_title': news_title,
        'news_summary': news_p,
    }
    return news_data


# scrape for featured image on Mars
def scrape_featured_image():
    browser = init_browser()

    JPL_url= 'https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA19980'
    browser.visit(JPL_url)

    time.sleep(3)
    JPL_html = browser.html
    soup = bs(JPL_html, 'html.parser')
    JPL_image = soup.find('figure', class_= 'lede').a['href']

    JPL_url = JPL_url.split('/')
    JPL_parturl = JPL_url[0:3]
    JPL_parturl2 = '/'.join(JPL_parturl)
    featured_image_url = JPL_parturl2 + JPL_image
    urllib.request.urlretrieve(featured_image_url, 'featured_image.jpg')

    return featured_image_url

# scrape for Mars weather from twitter
def scrape_weather():
    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)  
    weather_html = browser.html
    soup = bs(weather_html, 'html.parser')
    
    weather_info = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    weather = []
    for weather in weather_info:
        weather.append(weather.text.strip())
    weather = list(weather)
    mars_weather = weather[0]
   
    return mars_weather


# scrape for Mars facts
def scrape_facts():
    browser = init_browser()

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # facts_html = browser.html
    # soup = bs(facts_html,'html.parser')
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Category', 'Stats']
    facts_table = df.to_html()

    return facts_table


# scrape for Mars Hemispheres
def scrape_hems():
    browser = init_browser()

    # find common url portion
    Cerbrus_url= 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(Cerbrus_url)
    Cerbrus_url = Cerbrus_url.split('/')
    Cerbrus_parturl = Cerbrus_url[0:3]
    Common_parturl = '/'.join(Cerbrus_parturl)

    # find Cerbrus image url
    time.sleep(3)
    Cerbrus_html = browser.html
    soup = bs(Cerbrus_html, 'html.parser')
    Cerbrus_image = soup.find('img', class_= 'wide-image')['src']
    Cerbrus_image_url = Common_parturl + Cerbrus_image

    # find Schiaparelli image url
    Schia_url= 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(Schia_url)

    time.sleep(3)
    Schia_html = browser.html
    soup = bs(Schia_html, 'html.parser')
    Schia_image = soup.find('img', class_= 'wide-image')['src']
    Schia_image_url = Common_parturl + Schia_image

    # find Syrtis image url
    Syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(Syrtis_url)

    time.sleep(3)
    Syrtis_html = browser.html
    soup = bs(Syrtis_html, 'html.parser')
    Syrtis_image = soup.find('img', class_= 'wide-image')['src']
    Syrtis_image_url = Common_parturl + Syrtis_image

    # find image url
    Valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(Valles_url)

    time.sleep(3)
    Valles_html = browser.html
    soup = bs(Valles_html, 'html.parser')
    Valles_image = soup.find('img', class_= 'wide-image')['src']
    Valles_image_url = Common_parturl + Valles_image


    hemisphere_image_urls = [
        {'title':'Cerbrus Hemisphere', 'image_url': Cerbrus_image_url},
        {'title':'Schiaparelli Hemisphere', 'image_url':Schia_image_url },
        {'title':'Syrtis Major Hemisphere', 'image_url': Syrtis_image_url},
        {'title':'Valles Marineris Hemisphere', 'image_url': Valles_image_url},
    ]

    return hemisphere_image_urls

