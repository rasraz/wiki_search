from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import requests
import re
import shutil

# webdriver (chromdriver) service
service = Service(executable_path=ChromeDriverManager().install())

# text to search
search_text = input('search for: ')

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

# find all images element
images = driver.find_elements(by="tag name",value="img")

# save all images 
for image in images:
    # find image names
    image_url = str(image.get_attribute('src'))
    index = re.search(pattern=r'([a-zA-Z0-9_.%-]+)$',string=image_url)
    image_name = image_url[index.start():]
    # save image by orginal name
    response = requests.get(url=image_url,stream=True)
    with open(image_name,'wb') as out_file:
        shutil.copyfileobj(response.raw,out_file)

