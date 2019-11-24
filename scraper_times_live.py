import re

import scrapy
from scrapy.http import Response

from mentions import MentionsParser


class TimesLiveSpider(scrapy.Spider):
    name = 'times_live'
    start_urls = [
        'https://www.timeslive.co.za/politics/',
    ]

    def __init__(self, years=[], **kwargs):
        self.years = years
        super().__init__(**kwargs)  # python3

    @classmethod
    def get_politics_page_name_substring(cls, url: str):
        if url.startswith('/'):
            url = 'https://www.timeslive.co.za' + url
        return re.search('https:\/\/www\.timeslive\.co\.za\/politics\/(.*)\/', url).string

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
                print(dir(article))
                print(type(article))
                text = article.get()
                article_body = article.css(".article-widget:not([class*='article-widget-related_articles'])").xpath('.//text()').extract()
                article_text = '\n'.join(article_body)
                mentions = MentionsParser.calculate_mentions(article_text)
                yield {
                    'url': page_url,
                    'anc': mentions.anc,
                    'da': mentions.da,
                    'eff': mentions.eff,
                }

        for href in response.css('a::attr(href)'):
            if self.is_politics_page(href.get()):
                yield response.follow(href, self.parse)