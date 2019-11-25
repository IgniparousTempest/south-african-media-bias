import re

import scrapy
from scrapy.http import Response

from scraper.mentions import MentionsParser


class TimesLiveSpider(scrapy.Spider):
    name = 'times_live'
    start_urls = [
        'https://www.timeslive.co.za/politics/',
    ]

    def __init__(self, start_urls_path=None, **kwargs):
        if start_urls_path is not None:
            with open(start_urls_path) as f:
                self.start_urls = f.read().splitlines()
        super().__init__(**kwargs)  # python3

    @classmethod
    def is_in_domain(cls, url: str) -> bool:
        if url.startswith('/'):
            url = 'https://www.timeslive.co.za' + url
        return re.search('https:\/\/www\.timeslive\.co\.za\/', url) is not None

    @classmethod
    def get_politics_page_name_substring(cls, url: str):
        if url.startswith('/'):
            url = 'https://www.timeslive.co.za' + url
        return re.search('https:\/\/www\.timeslive\.co\.za\/politics\/(.*)\/', url).group(1)

    @classmethod
    def get_month_year(cls, url: str):
        page_url = cls.get_politics_page_name_substring(url)
        date_match = re.search(r'^(\d{4})-(\d{2})-\d{2}', page_url)
        return date_match.group(1), date_match.group(2)

    @classmethod
    def is_politics_page(cls, url: str) -> bool:
        try:
            cls.get_politics_page_name_substring(url)
            return True
        except AttributeError:
            return False

    def parse(self, response: Response):
        # Parse politics pages
        if self.is_politics_page(response.url):
            page_url = self.get_politics_page_name_substring(response.url)
            for article in response.css('div.article-widgets'):
                text = article.get()
                article_body = article.css(".article-widget:not([class*='article-widget-related_articles'])").xpath('.//text()').extract()
                article_text = '\n'.join(article_body)
                mentions = MentionsParser.calculate_mentions(article_text)
                year, month = self.get_month_year(response.url)
                yield {
                    'url': page_url,
                    'year': year,
                    'month': month,
                    'anc': mentions.anc,
                    'da': mentions.da,
                    'eff': mentions.eff,
                }

        for href in response.css('a::attr(href)'):
            if self.is_politics_page(href.get()):
                yield response.follow(href, self.parse)