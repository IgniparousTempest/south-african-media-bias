from pathlib import Path
import re
from pprint import pprint
from typing import Optional

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Response

import results
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
        urls_file_path = results.absolute_path(f'{name}.urls')
        if Path(urls_file_path).is_file():
            with open(urls_file_path, 'r') as f:
                self.start_urls = f.read().splitlines()
        else:
            self.start_urls = [politics_page_url]
        super().__init__(**kwargs)  # python3
        dispatcher.connect(self.on_spider_closed, signals.spider_closed)

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

    def on_spider_closed(self, spider: scrapy.Spider):
        stats = self.crawler.stats.get_stats()
        with open(results.absolute_path(f'{self.name}.stats'), 'w') as f:
            pprint(stats, stream=f)

    @classmethod
    def run(cls):
        """Runs the scraper. This can be considered the main() method."""

        from scrapy.crawler import CrawlerProcess

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': results.absolute_path(f'{cls.name}.json')
        })

        process.crawl(cls)
        process.start()
