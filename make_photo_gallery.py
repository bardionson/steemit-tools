import collections
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

options = webdriver.ChromeOptions()
options.add_argument('headless')
username = sys.argv[1]
root_url = "http://wowak.com/blog.html?user="+username
page = requests.get(root_url, verify=True).content
url = "https://steemit.com"
browser = webdriver.Chrome(chrome_options=options) #replace with .Firefox(), or with the browser of your choice
browser.get(root_url)
time.sleep(5)
links = browser.find_elements_by_xpath("//*[@href]")
data_links = collections.OrderedDict()
for link in links:
   #print link.get_attribute("href")
   a = link.get_attribute("href")
   # filter out the resteems
   if (username in a):
      key = a.decode('utf-8') 
      data_links[key] = a.decode('utf-8') 

data_images = collections.OrderedDict()
for keys,values in data_links.items():
   page = requests.get(values, verify=True).content
   soup = BeautifulSoup(page, "html.parser")
   images = soup.find_all('img')
   counter = 0
   for image in images:
      # filter out steemitboard
      if ('steemitboard' not in image.attrs['src']):
         try:
            key = "<img src='"+image.attrs['src']+"' alt='"+image.attrs['alt']+"'>"
         except KeyError:
	    key = "<img src='"+image.attrs['src']+"' alt='"+values+"'>"
         data_images[key] = values

for keys,values in data_images.items():
   print "<div class='pull-left'><a href='"+values+"'>"
   print keys.decode('utf-8') 
   print "</a></div>"

browser.quit()
