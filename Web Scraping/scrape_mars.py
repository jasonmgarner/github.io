
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import datetime as dt
import time as time

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}
    
    #Visit Nasa Website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(8)
    news_title = soup.find('div', 'content_title', 'a').text
    time.sleep(5)
    news_p = soup.find('div', 'article_teaser_body').text
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p              
    
    # Visit JPL website             
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "html.parser")


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)              
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    start_img_url = image_soup.find('img', 'main_image')
    img_url = start_img_url.get('src')

    jpl_img_url = "https://www.jpl.nasa.gov" + img_url
    mars_dict["featured_img_src"] = jpl_img_url

    #Visit Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, "html.parser")

    mars_weather = twitter_soup.find('p', "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_dict["mars_weather"] = mars_weather
    
    #Mars Facts Website              
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)
    facts_html = browser.html
    facts_soup = bs(facts_html, "html.parser")
    facts_table = pd.read_html(facts_url)
    df = facts_table[0]
    df.columns = ["Parameter", "Values"]
    table = df.set_index(["Parameter"])
    table_html = table.to_html()
    table_html = table_html.replace("\n", "")
    mars_dict["table_facts"] = table_html
                  
    #Hemisphere images                  
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html.parser")
    


    cerberus = browser.find_by_tag('h3')[0].text
    schiaparelli = browser.find_by_tag('h3')[1].text
    syrtis_major = browser.find_by_tag('h3')[2].text
    valles_marineris = browser.find_by_tag('h3')[3].text

    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    cerberus_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    schiaparelli_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    syrtis_major_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    valles_marineris_img = browser.find_by_text('Sample')['href']
    browser.back()


    hemisphere_image_urls = [
        {'title': cerberus, 'img_url': cerberus_img},
        {'title': schiaparelli, 'img_url': schiaparelli_img},
        {'title': syrtis_major, 'img_url': syrtis_major_img},
        {'title': valles_marineris, 'img_url': valles_marineris_img}]
    
    mars_dict["Mars_Hemis"] = hemisphere_image_urls            


    return mars_dict
             
            