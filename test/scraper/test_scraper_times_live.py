import unittest

from scraper.scraper_times_live import TimesLiveSpider


class MyTestCase(unittest.TestCase):
    def test_is_in_domain(self):
        self.assertFalse(TimesLiveSpider.is_in_domain('https://www.businesslive.co.za/bd/world/europe/2019-04-23-volodymyr-zelenskiy-faces-battles-with-ukraines-hostile-parliament/'))

        self.assertTrue(TimesLiveSpider.is_in_domain('https://www.timeslive.co.za/politics/2019-11-23-ramaphosa-defends-eskom-ceo-appointment/'))


if __name__ == '__main__':
    unittest.main()
