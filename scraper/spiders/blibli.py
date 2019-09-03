import os
import re
import scrapy
from scrapy_splash import SplashRequest
from scraper.items import ImageItem

class BlibliSpider(scrapy.Spider):
    name = "bliblispider"
    PAGE_LIMIT = 3
    OUTPUT_PATH = "outputs/blibli/"
    
    # change according to urls you want to scrap
    list_urls = [
        "https://www.blibli.com/c/2/makanan/MA-1000160/53400",
    ]

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())

        urls = self.list_urls
        for url in urls:
            request = SplashRequest(url, self.parse, args={'wait': 0.5})
            yield request

    def temp_start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        urls = self.list_urls
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        print(response.body)
        print()
        CATEGORY_SELECTOR = 'div[data-v-7df892c8].product-listing__seo-top h1[data-v-7df892c8]::text'
        category = response.css(CATEGORY_SELECTOR).extract_first()
        print(category)