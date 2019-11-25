from selenium import webdriver
import time

url = "https://www.timeslive.co.za/politics/"
driver = webdriver.Firefox()
driver.get(url)
html = driver.page_source.encode('utf-8')
page_num = 0
outerHTML = ""

driver.find_element_by_css_selector('#button-close').click()  # Get rid of annoying cookie banner

while True:
    driver.find_element_by_css_selector('.load-more').find_element_by_css_selector('.featured').click()
    page_num += 1
    print("getting page number "+str(page_num))
    time.sleep(2)  # There seems to be some for of rate limiting. It was '1'.
    outerHTML_new = driver.execute_script("return document.documentElement.outerHTML")
    if outerHTML == outerHTML_new:
        break
    outerHTML = outerHTML_new
print('Done loading page')

elems = driver.find_elements_by_xpath("//a[@href]")
with open('results/times_live.urls', 'w') as f:
    num_links = 0
    for elem in elems:
        href = elem.get_attribute("href")
        if href.startswith('https://www.timeslive.co.za/politics/'):
            f.write(href)
            f.write('\n')
            num_links += 1
    print(f'Found {num_links} links')

html = driver.page_source.encode('utf-8')
