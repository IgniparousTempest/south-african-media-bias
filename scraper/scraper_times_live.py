import re

from overrides import overrides
from scrapy.http import Response

from scraper.mentions import MentionsParser
from scraper.scraper_parent import NewsSpider


class TimesLiveSpider(NewsSpider):
    name = 'times_live'

    def __init__(self, start_urls_path=None, **kwargs):
        super().__init__('times_live', 'https://www.timeslive.co.za/politics/', 'https://www.timeslive.co.za', r'https://www\.timeslive\.co\.za/politics/(.*)/', **kwargs)

    def get_month_year(self, url: str):
        page_url = self.get_politics_page_name_substring(url)
        date_match = re.search(r'^(\d{4})-(\d{2})-\d{2}', page_url)
        return date_match.group(1), date_match.group(2)

    @overrides
    def parse_politics_page(self, response: Response):
        print('hit: ', response.url)
        page_url = self.get_politics_page_name_substring(response.url)
        mentions_anc, mentions_da, mentions_eff = 0, 0, 0
        # The article tag is inconsistent, this seems to be the best way to get the results.
        for article in response.css('div.article-widgets'):
            text = article.get()
            article_body = article.css(".article-widget:not([class*='article-widget-related_articles'])").xpath('.//text()').extract()
            article_text = '\n'.join(article_body)
            mentions = MentionsParser.calculate_mentions(article_text)
            mentions_anc += mentions.anc
            mentions_da += mentions.da
            mentions_eff += mentions.eff
        year, month = self.get_month_year(response.url)
        return {
            'url': response.url,
            'year': year,
            'month': month,
            'anc': mentions_anc,
            'da': mentions_da,
            'eff': mentions_eff,
        }


if __name__ == '__main__':
    TimesLiveSpider.run()
