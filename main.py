from scraper.scraper_iol import IOLSpider
from scraper.scraper_times_live import TimesLiveSpider

if __name__ == '__main__':
    # Run all scrapers
    TimesLiveSpider.run()
    IOLSpider.run()
