from scrapy.crawler import CrawlerProcess

from scraper_times_live import TimesLiveSpider

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results/times_live.json'
    })

    process.crawl(TimesLiveSpider, [])
    process.start()
