from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import results

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
links = []

if __name__ == '__main__':
    options = Options()
    options.headless = True  # Enable to run over SSH
    driver = webdriver.Firefox(options=options)
    for url in politics_pages:
        driver.get(url)
        html = driver.page_source.encode('utf-8')

        elems = driver.find_elements_by_xpath("//a[@href]")
        # Get politics links
        new_links = []
        for elem in elems:
            href = elem.get_attribute("href")
            if href.startswith('https://www.news24.com/SouthAfrica/News/'):
                new_links.append(href)
        links += new_links
        print(f'Found {len(new_links)} links on \'{url}\'')
    driver.close()
    print(f'Found {len(links)} links in total')

    # Write unique links to file
    with open(results.absolute_path('news24.urls'), 'w') as f:
        links = list(set(links))
        for elem in links:
            f.write(f'{elem}\n')
        print(f'Found unique {len(links)} links')
