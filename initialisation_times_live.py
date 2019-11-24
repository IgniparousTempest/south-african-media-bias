from selenium import webdriver
import time

url = "https://www.timeslive.co.za/politics/"
driver = webdriver.Firefox()
driver.get(url)
html = driver.page_source.encode('utf-8')
page_num = 0

driver.find_element_by_css_selector('#button-close').click()

while driver.find_elements_by_css_selector('.load-more'):
    driver.find_element_by_css_selector('.load-more').find_element_by_css_selector('.featured').click()
    page_num += 1
    print("getting page number "+str(page_num))
    time.sleep(1)

elems = driver.find_elements_by_xpath("//a[@href]")
with open('results/times_live.urls', 'w') as f:
    for elem in elems:
        href = elem.get_attribute("href")
        if href.startswith('/politics'):
            f.write(href)
            f.write('\n')

html = driver.page_source.encode('utf-8')