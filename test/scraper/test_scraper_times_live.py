import unittest

from scraper.scraper_times_live import TimesLiveSpider


class MyTestCase(unittest.TestCase):
    def test_is_in_domain(self):
        spider = TimesLiveSpider()
        self.assertFalse(spider.is_in_domain('https://www.businesslive.co.za/bd/world/europe/2019-04-23-volodymyr-zelenskiy-faces-battles-with-ukraines-hostile-parliament/'))
        self.assertFalse(spider.is_in_domain('https://www.amazon.com/product-reviews/B07VRMVT3N/ref=pd_cp_309_cr_4/136-9194889-5780825?ie=UTF8&pd_rd_i=B07VRMVT3N&pd_rd_r=25c3884b-daf8-4005-b0fd-397b93885049&pd_rd_w=Ml7MV&pd_rd_wg=jWHX5&pf_rd_p=0e5324e1-c848-4872-bbd5-5be6baedf80e&pf_rd_r=YNZQR1W5S2M41TZ978HQ&refRID=YNZQR1W5S2M41TZ978HQ'))

        self.assertTrue(spider.is_in_domain('https://www.timeslive.co.za/politics/2019-11-23-ramaphosa-defends-eskom-ceo-appointment/'))


if __name__ == '__main__':
    unittest.main()
