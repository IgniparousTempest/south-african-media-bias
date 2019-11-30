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
    # An example news page is 'https://www.iol.co.za/news/politics/jacob-zuma-will-finally-have-his-day-in-court-38238221'
    if href.startswith('https://www.iol.co.za/news/politics/'):# and href.split('-')[-1].isnumeric():
        links.append(href)
print(f'Found {len(links)} links')
# Write unique links to file
with open('results/iol.urls', 'w') as f:
    links = list(set(links))
    for elem in links:
        f.write(f'{elem}\n')
    print(f'Found unique {len(links)} links')

html = driver.page_source.encode('utf-8')
