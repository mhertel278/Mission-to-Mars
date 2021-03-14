

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import random
import time


# In[5]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# # ### Visit the NASA Mars News Site

# # In[3]:


# # Visit the mars nasa news site
# url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
# browser.visit(url)

# # Optional delay for loading the page
# rand_num = random.randint(3,7)
# browser.is_element_present_by_css('div.list_text', wait_time=rand_num)


# # In[4]:


# # Convert the browser html to a soup object and then quit the browser
# html = browser.html
# news_soup = soup(html, 'html.parser')

# slide_elem = news_soup.select_one('div.list_text')


# # In[5]:


# slide_elem.find('div', class_='content_title')


# # In[6]:


# # Use the parent element to find the first a tag and save it as `news_title`
# news_title = slide_elem.find('div', class_='content_title').get_text()
# news_title


# # In[7]:


# # Use the parent element to find the paragraph text
# news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
# news_p


# # ### JPL Space Images Featured Image

# # In[8]:


# # Visit URL
# url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
# browser.visit(url)


# # In[9]:


# # Find and click the full image button
# full_image_elem = browser.find_by_tag('button')[1]
# full_image_elem.click()


# # In[10]:


# # Parse the resulting html with soup
# html = browser.html
# img_soup = soup(html, 'html.parser')
# img_soup


# # In[11]:


# # find the relative image url
# img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# img_url_rel


# # In[12]:


# # Use the base url to create an absolute url
# img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
# img_url


# # ### Mars Facts

# # In[13]:


# df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
# df.head()


# # In[14]:


# df.columns=['Description', 'Mars', 'Earth']
# df.set_index('Description', inplace=True)
# df


# # In[15]:


# df.to_html()


# # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# # ### Hemispheres

# # In[63]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)
# add delay for loading page
time.sleep(5)


# In[69]:


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


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# In[70]:


# 5. Quit the browser
browser.quit()


# In[ ]:




