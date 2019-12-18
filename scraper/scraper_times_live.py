import re

from overrides import overrides
from scrapy.http import Response

from scraper.mentions import MentionsParser
from scraper.scraper_parent import NewsSpider


class TimesLiveSpider(NewsSpider):
    name = 'times_live'

    def __init__(self, start_urls_path=None, **kwargs):
        super().__init__('times_live', 'https://www.timeslive.co.za/politics/', 'https://www.timeslive.co.za', r'https://www\.timeslive\.co\.za/politics/(.*)/', **kwargs)

    def get_month_year(self, response: Response):
        page_url = self.get_politics_page_name_substring(response.url)
        date_match = re.search(r'^(\d{4})-(\d{2})-\d{2}', page_url)
        return date_match.group(1), date_match.group(2)

    @overrides
    def parse_politics_page(self, response: Response):
        page_url = self.get_politics_page_name_substring(response.url)
        for article in response.css('div.article-widgets'):
            text = article.get()
            article_body = article.css(".article-widget:not([class*='article-widget-related_articles'])").xpath('.//text()').extract()
            article_text = '\n'.join(article_body)
            mentions = MentionsParser.calculate_mentions(article_text)
            year, month = self.get_month_year(response.url)
            yield {
                'url': response.url,
                'year': year,
                'month': month,
                'anc': mentions.anc,
                'da': mentions.da,
                'eff': mentions.eff,
            }


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': f'results/{TimesLiveSpider.name}.json'
    })

    process.crawl(TimesLiveSpider)
    process.start()
