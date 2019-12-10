from overrides import overrides
from scrapy.http import Response

from scraper.mentions import MentionsParser
from scraper.scraper_parent import NewsSpider


class IOLSpider(NewsSpider):
    name = 'iol'

    def __init__(self, start_urls_path=None, **kwargs):
        super().__init__('iol', 'https://www.iol.co.za/news/politics/', 'https://www.iol.co.za', r'https://www\.iol\.co\.za/news/politics/(.*)', **kwargs)  # python3

    def get_month_year(self, response: Response):
        date_string = response.css('span[itemprop="datePublished"]::attr(content)').extract_first().split('-')
        return date_string[0], date_string[1]

    @overrides
    def parse_politics_page(self, response: Response):
        page_url = self.get_politics_page_name_substring(response.url)
        article_body = response.css(".article-body").xpath('.//text()').extract()
        article_text = '\n'.join(article_body)
        mentions = MentionsParser.calculate_mentions(article_text)
        year, month = self.get_month_year(response)
        # print(page_url, year, month)
        return {
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
        'FEED_URI': 'results/iol.json'
    })

    process.crawl(IOLSpider)
    process.start()
