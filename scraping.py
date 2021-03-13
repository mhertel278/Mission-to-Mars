
# import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# import pandas
import pandas as pd
# import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager


# Set executable path and initialize chrome browser in splinter
executable_path = {'executable_path':ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ### Article Scraping

# visit mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images


url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the Full Image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# create absolute url from base url and relative url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Scrape Mars Facts

# scrape Mars Facts table into DataFrame
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()



browser.quit()

