from pathlib import Path
import re
from typing import Optional

import scrapy
from scrapy.http import Response

from scraper.mentions import MentionsParser


class NewsSpider(scrapy.Spider):
    def __init__(self, name: str, politics_page_url: str, domain_url: str, politics_url_regex: str, **kwargs):
        """

        :param name: The file names for this scraper. e.g. 'times_live'
        :param politics_page_url: e.g. 'https://www.timeslive.co.za/politics/'
        :param domain_url: e.g. 'https://www.timeslive.co.za'
        :param politics_url_regex: e.g. r'https://www\.timeslive\.co\.za/politics/(.*)/'
        :param kwargs:
        """
        self.politics_page_url = politics_page_url
        self.domain_url = domain_url
        self.politics_url_regex = politics_url_regex
        if Path(f'results/{name}').is_file():
            with open(f'results/{name}', 'r') as f:
                self.start_urls = f.read().splitlines()
        else:
            self.start_urls = [politics_page_url]
        super().__init__(**kwargs)  # python3

    def is_in_domain(self, url: str, parent_url: Optional[str] = None) -> bool:
        if (parent_url is None or self.is_in_domain(parent_url)) and url.startswith('/'):
            url = self.domain_url + url
        return url.startswith(f'{self.domain_url}/')

    def get_politics_page_name_substring(self, url: str):
        if url.startswith('/'):
            url = self.domain_url + url
        return re.search(self.politics_url_regex, url).group(1)

    def is_politics_page(self, url: str) -> bool:
        try:
            self.get_politics_page_name_substring(url)
            return True
        except AttributeError:
            return False

    def parse_politics_page(self, response: Response):
        raise NotImplementedError()

    def parse(self, response: Response):
        # Parse politics pages
        if self.is_politics_page(response.url):
            yield self.parse_politics_page(response)

        for href in response.css('a::attr(href)'):
            if self.is_in_domain(href.get(), response.url):
                yield response.follow(href, self.parse)