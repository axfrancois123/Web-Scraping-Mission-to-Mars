#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

def init_browser():    
        executable_path = {"executable_path": "chromedriver.exe"}    
        return Browser("chrome", **executable_path, headless=False)


def scrape():

        # Setup splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)


        # # NASA Mars News


        # Visit Mars News Site
        url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
        browser.visit(url)


        #using bs to write it into html
        html = browser.html
        extra = bs(html, "html.parser")
        slide = extra.select_one("ul.item_list li.slide")



        slide.find("div", class_="content_title")



        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title


        latest = slide.find("div", class_="content_title").get_text()
        print(latest)


        # Scraping the latest paragraph

        paragraph = extra.find("div", class_="article_teaser_body").text

        print(paragraph)


        # # JPL Mars Space Images - Featured Image



        # Setup splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)


        # Visiting Image Website

        url_image = "https://spaceimages-mars.com/"
        browser.visit(url_image)

        # Data parsing with bs

        html = browser.html
        soup_pic = bs(html, "html.parser")


        # Use splinter to go to website and click button

        images = soup_pic.find_all("img, class = headerimage fade-in")
        featured_image_url = images[0].get("src")


        # # Mars Facts


        # Use Pandas to scrape data
        tables = pd.read_html('https://galaxyfacts-mars.com/')

        # Take second table for Mars facts
        mars_df = tables[1]

        # Rename columns and set index
        mars_df.columns=['description', 'value']
        mars_df


        # Convert table to html

        mars_table = [mars_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
        mars_table


        # # Mars Hemispheres



        # Open browser to USGS Astrogeology site
        browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')


        html = browser.html
        soup = bs(html, 'html.parser')

        hemi_list = []

        # Search for the names of all four hemispheres
        result = soup.find_all('div', class_="collapsible results")
        hemispheres = results[0].find_all('h3')

        # Get text and store in list
        for name in hemispheres:
                hemi_list.append(name.text)

                

        # Search for thumbnail links
        thumbnail_results = results[0].find_all('a')
        thumbnail_links = []

        for thumbnail in thumbnail_results:
    
                # If the thumbnail element has an image...
                if (thumbnail.img):
        
                # then grab the attached link
                        thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
        
        # Append list with links
                        thumbnail_links.append(thumbnail_url)


        full_imgs = []

        for url in thumbnail_links:
    
                # Click through each thumbanil link
                browser.visit(url)
    
                html = browser.html
                soup = bs(html, 'html.parser')
    
        # Scrape each page for the relative image path
        result = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
    
        # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
    
        # Add full image links to a list
        full_imgs.append(img_link)

        full_imgs

        # Zip together the list of hemisphere names and hemisphere image links
        mars_zip = zip(hemi_names, full_imgs)

        hemisphere_image_urls = []

        # Iterate through the zipped object
        for title, img in mars_zip:
    
                mars_dict = {}
    
        # Add hemisphere title to dictionary
                mars_dict['title'] = title
    
        # Add image url to dictionary
                mars_dict['img_url'] = img
    
        # Append the list with dictionaries
        hemisphere_image_urls.append(mars_dict)

        hemisphere_image_urls

        return mars_dict