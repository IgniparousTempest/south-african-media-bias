from typing import Tuple

from overrides import overrides
from scrapy.http import Response

from scraper.mentions import MentionsParser
from scraper.scraper_parent import NewsSpider

from urllib.parse import urlsplit, urlunsplit, urljoin, SplitResult


class News24Spider(NewsSpider):
    """
    This one works a bit differently. News24's desktop website is a mess. So scraping happens on the desktop website,
    but parsing happens on the mobile page.
    """
    name = 'news24'

    def __init__(self, start_urls_path=None, **kwargs):
        super().__init__(
            name='news24',
            politics_page_url='https://www.news24.com/SouthAfrica/News/',
            domain_url='https://www.news24.com',
            politics_url_regex=r'https://www\.news24\.com/SouthAfrica/News/(.*)',
            **kwargs
        )

    def get_month_year(self, url: str) -> Tuple[str, str]:
        # format: https://www.news24.com/SouthAfrica/News/sa-born-man-tells-of-moment-he-apprehended-london-bridge-attacker-20191221
        iso_date_string = url.split('-')[-1]
        return iso_date_string[0:4], iso_date_string[4:6]

    def is_mobile(self, url: str) -> bool:
        return url.startswith('https://m.news24.com')

    @overrides
    def parse(self, response: Response):
        if self.is_mobile(response.url):
            # Parse mobile politics page
            yield self.parse_politics_page(response)
        else:
            # Go to mobile page instead
            if self.is_politics_page(response.url):
                yield response.follow(response.url.replace('www', 'm', 1), self.parse)

            for href in response.css('a::attr(href)'):
                absolute_url = urljoin(response.url, href.get())  # Make relative links absolute
                if self.is_in_domain(href.get(), response.url):
                    # Remove parameters
                    o: SplitResult = urlsplit(absolute_url)
                    base_href = urlunsplit((o.scheme, o.netloc, o.path, '', ''))
                    yield response.follow(base_href, self.parse)

    @overrides
    def parse_politics_page(self, response: Response):
        print(f'hit \'{response.url}\'.')

        mentions_anc, mentions_da, mentions_eff = 0, 0, 0
        article_body = response.css(".article_content").xpath('.//text()').extract()
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
    News24Spider.run()
