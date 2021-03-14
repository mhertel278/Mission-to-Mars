from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import time
import random

def scrape_all():
    # Set executable path and initialize chrome browser in splinter
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # set variables for mars_news output
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# ### Article Scraping
def mars_news(browser):
    
    # visit mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    rand_num = random.randint(3,7)
    browser.is_element_present_by_css("div.list_text", wait_time=rand_num)


    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Add try/except for error handling
    try:
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
def featured_image(browser):
    # Visit url
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the Full Image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # create absolute url from base url and relative url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    

    return  img_url

def mars_facts():

    # ### Scrape Mars Facts

    try:
        # scrape Mars Facts table into DataFrame
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None
    
    # Assign columns and set index to the dataframe
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    # add delay for loading page
    time.sleep(1)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # add delay to load the page

    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # find all the image link names
    hemis = hemi_soup.find_all('h3')


    # loop through each link title
    for hemi in hemis:
        # create dictionary to hold image url and title
        hemi_dict = {}
        
        # add title to dict
        link_text = hemi.text
        hemi_dict['title'] = link_text
        
        # follow link to image page
        browser.click_link_by_partial_text(link_text)
        time.sleep(1)
        
        # scrape the image url
        img_html = browser.html
        img_soup = soup(img_html, 'html.parser')
        img_url = img_soup.find('div', class_='downloads').find('a', target="_blank")['href']
        
        # add url to dict
        hemi_dict['img_url'] = img_url
        
        # go back to home page
        browser.back()
        time.sleep(1)
        
        # add dict to urls list
        hemisphere_image_urls.append(hemi_dict)
    
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped date
    print(scrape_all())

