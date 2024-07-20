from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import requests
import re
import shutil
import os

# TODO: Make the project functional

# webdriver (chromdriver) service
service = Service(executable_path=ChromeDriverManager().install())

# text to search
search_text = input('search for: ')
os.mkdir(f'./{search_text}')

# open browser
driver = Chrome(service=service)


driver.maximize_window()

# target website 
url = "https://www.wikipedia.org/"
driver.get(url)

# selecting persian wikipedia 
driver.find_element(by='id',value='js-link-box-fa').click()
 
# searching
search_box = driver.find_element(by='id',value='searchInput')
search_box.send_keys(search_text)
search_box.send_keys(Keys.ENTER)

# finding all box links
link_box_results = driver.find_elements(by='class name',value='mw-search-result-heading')

# saving all page links
links = []
for link_box in link_box_results:
    a_tag_link = link_box.find_element(by='tag name',value='a').get_attribute('href')
    links.append(a_tag_link)
else:
    # single page result
    links.append(driver.current_url)

# scrolling pages
counter=0
for link in links:
    driver.get(link)
    
    # find all images element
    content_page = driver.find_element(by='id',value='bodyContent')
    images = content_page.find_elements(by="tag name",value="img")

    # save all images 
    for image in images:
        image_url = str(image.get_attribute('src'))
        # find image format
        file_format = re.findall(pattern=r'(png|JPG|svg|jpeg|jpg|jfif|pjpeg|pjp|gif|webp|apng|avif)',string=image_url)
        file_format=file_format[-1]
        # save image by orginal name
        response = requests.get(url=image_url,stream=True)
        target_file_path = f'./{search_text}/{counter}.{file_format}'
        print(f'saving file: {target_file_path}')
        with open(target_file_path,'wb') as out_file:
            shutil.copyfileobj(response.raw,out_file)
        counter+=1

