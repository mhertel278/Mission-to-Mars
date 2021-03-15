# Mission-to-Mars

## Resources

python 3.7.9, vs code 1.54, mongoDB 4.4.4, Flask 1.1.2

## Project Overview

The purpose of this project was to scrape the NASA webpage for the latest news and images of Mars.  I wrote a python script incorporating splinter to browse the website, and beautiful soup to scrape the html for the most recent article title and summary, as well as the url of the featured image and facts about the planet.  I then created a Flask app to run the python script and store the scraping results in a mongo database and create a webpage to display article title and summary, the image, and the facts table.  Finally, I incorporated a button on the webpage that re-runs the python script to scrape for a new article to display.