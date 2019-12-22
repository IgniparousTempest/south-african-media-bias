import time
from typing import List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

import results

# The load more results button on these pages doesn't work. News24's site is bloody badly broken.
politics_pages = [
    'https://www.news24.com/SouthAfrica/Politics',
    'https://www.news24.com/Tags/Companies/ANC',
    'https://www.news24.com/Tags/Companies/da',
    'https://www.news24.com/Tags/Companies/eff',
    'https://www.news24.com/Tags/Companies/cope',
    'https://www.news24.com/Tags/Companies/IFP',
    'https://www.news24.com/Tags/Companies/udm',
    'https://www.news24.com/Tags/Companies/nfp',
    'https://www.news24.com/Tags/Companies/ffplus',
    'https://www.news24.com/Tags/Companies/acdp',
    'https://www.news24.com/Tags/Companies/SACP',
    'https://www.news24.com/Tags/Companies/ID',
    'https://www.news24.com/Tags/Companies/cosatu'
]
mobile_website_url = 'https://m.news24.com/SouthAfrica'  # The 'load more' button works on the mobile website.


def get_links_from_driver(driver: WebDriver) -> List[str]:
    elems = driver.find_elements_by_xpath("//a[@href]")
    # Get politics links
    links = []
    for elem in elems:
        href = elem.get_attribute("href")
        if href.startswith('https://m.news24.com/'):  # Handle links from the mobile site
            href = 'https://www' + href[9:]
        if href.startswith('https://www.news24.com/SouthAfrica/News/'):
            links.append(href)
    return links


def get_links_on_deskop_website(driver: WebDriver) -> List[str]:
    links = []
    for url in politics_pages:
        driver.get(url)
        html = driver.page_source.encode('utf-8')

        # Get politics links
        new_links = get_links_from_driver(driver)
        links += new_links
        print(f'Found {len(new_links)} links on \'{url}\'')
    print(f'Found {len(links)} links on desktop')
    return links

def get_links_on_mobile_website(driver: WebDriver) -> List[str]:
    page_num = 0
    outer_html = ""
    driver.get(mobile_website_url)

    try:
        while True:
            driver.find_element_by_css_selector('#btn_showmore').click()
            page_num += 1
            print("getting page number " + str(page_num))
            time.sleep(1)
            outer_html_new = driver.execute_script("return document.documentElement.outerHTML")
            if outer_html == outer_html_new:
                break
            outer_html = outer_html_new
    except Exception as e:
        print('Aborting page load:', e)
    new_links = get_links_from_driver(driver)
    print(f'Found {len(new_links)} links on mobile')
    return new_links


if __name__ == '__main__':
    options = Options()
    options.headless = True  # Enable to run over SSH
    driver = webdriver.Firefox(options=options)

    desktop_links = get_links_on_deskop_website(driver)
    mobile_links = get_links_on_mobile_website(driver)
    all_links = desktop_links + mobile_links

    driver.close()

    print(f'Found {len(all_links)} links in total')

    # Write unique links to file
    with open(results.absolute_path('news24.urls'), 'w') as f:
        unique_links = list(set(all_links))
        for elem in unique_links:
            f.write(f'{elem}\n')
        print(f'Found unique {len(unique_links)} links')
