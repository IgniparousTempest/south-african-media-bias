from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

url = "https://www.iol.co.za/news/politics"
options = Options()
options.headless = True  # Enable to run over SSH
driver = webdriver.Firefox(options=options)
driver.get(url)
html = driver.page_source.encode('utf-8')
page_num = 0
outerHTML = ""

while True:
    driver.find_element_by_css_selector('#viewMoreButton').click()
    page_num += 1
    print("getting page number "+str(page_num))
    time.sleep(1)
    outerHTML_new = driver.execute_script("return document.documentElement.outerHTML")
    if outerHTML == outerHTML_new:
        break
    outerHTML = outerHTML_new
print('Done loading page')

elems = driver.find_elements_by_xpath("//a[@href]")
# Get politics links
links = []
for elem in elems:
    href = elem.get_attribute("href")
    if href.startswith('https://www.iol.co.za/news/politics/'):
        links.append(href)
print(f'Found {len(links)} links')
# Write unique links to file
with open('results/iol.urls', 'w') as f:
    num_links = 0
    for elem in list(set(links)):
        f.write(href)
        f.write('\n')
        num_links += 1
    print(f'Found unique {num_links} links')

html = driver.page_source.encode('utf-8')
