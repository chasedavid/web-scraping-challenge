#import dependencies: splinter, beautifulsoup, pandas, requests
from splinter import Browser
from bs4 import BeautifulSoup as bs

import pandas as pd
import requests

#variable for mars data
mars_data = {}


#function configure and use chrome browser for splinter
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return (Browser('chrome', **executable_path, headless=False))


def scrap():
    browser = init_browser()
    browser = Browser('chrome', **executable_path, headless=False)
    
    #provided url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text().strip()
    
    mars_data['headline'] = news_title
    mars_data['text'] = news_p
    
    #close browser
    browser.quit()
    
    return (mars_data)


def scrap_img():
    #initate browser
    browser = init_browser()
    
    #provided url
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #obtain full image url
    url_base = 'https://www.jpl.nasa.gov' 
    url_end = soup.find('article')['style']
    
    first_par = int(url_end.find('('))
    last_par = int(url_end.find(')'))
    featured_image_url = url_base + url_end[first_par+2: last_par-1]
    
    mars_data['image_url'] = featured_image_url
    
    browser.quit()
    
    return (mars_data)


def scrape_weather():
    browser = init_browser()
    
    #provided url
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #list of tweets from soup object
    tweets = soup.find_all('div', class_='js-tweet-text-container')
    
    #iterate through each element of the list
    for tweet in tweets:
        mars_weather = tweet.find('p', class_='tweet-text').text
        if 'Sol' and 'pressure' and 'daylight' in test:
            break
        else:
            pass
    mars_data['weather'] = mars_weather
    
    #close browser
    browser.quit()
    
    return(mars_data)
        

def scrape_facts():
    #provided url
    url = 'https://space-facts.com/mars/'
    
    #pandas scraping: read_html
    mars_facts = pd.read_html(url)
    
    df = mars_facts[0]
    #provide useful column discriptors
    df.columns = ['Characteristic', 'Value']
    
    facts = df.to_html()
    
    mars_data['facts'] = facts
    
    return(mars_data)
    

def scrape_hems():
    browser = init_browser()
    
    #provided url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #list of hemispheres
    hems_list = soup.find_all('div', class_='item')
    
    #var to store full image url's
    img_list = []
    
    url_base = 'https://astrogeology.usgs.gov'
    for item in hems_list:
        #store header
        header = item.find('h3').text
        
        #find url ending and concat with url_base
        img_end = item.find('a', class_='itemLink product-item')['href']
        img_url = url_base + img_end
        
        browser.visit(img_url)
        img_html = browser.html
        
        img_soup = bs(img_html, 'html.parser')
        img_full = url_base + img_soup.find('img', class_='wide-image')['src']
        
        img_list.append({'title': header ,'img_url': img_full})
        
    mars_data['hem_img_url'] = img_list
    
    browser.quit()
    return(mars_data)

