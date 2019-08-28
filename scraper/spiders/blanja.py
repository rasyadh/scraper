import os
import re
import scrapy
from scraper.items import ImageItem

class BlanjaSpider(scrapy.Spider):
    name = "blanjaspider"
    PAGE_LIMIT = 5
    OUTPUT_PATH = "outputs/blanja/"
    list_urls = [
        "https://www.blanja.com/store/unileverofficialstore",
        "https://www.blanja.com/store/miyakoofficialstore?keyword=&order=orders_desc",
    ]

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        for url in self.list_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request


    def parse(self, response):
        STORE_SELECTOR = 'h1.fColor-orange a::text'
        store = response.css(STORE_SELECTOR).extract_first()

        RESULT_SELECTOR = ".result-thumbs"
        result = response.css(RESULT_SELECTOR)

        BOX_SELECTOR = "div.box-item"
        for box_item in result.css(BOX_SELECTOR):
            NAME_SELECTOR = ".item-title a::text"
            URL_SELECTOR = ".item-title a::attr(href)"
            PRICE_SELECTOR = ".price::text"
            IMAGE_URL_SELECTOR = ".item-image a img.lazy::attr(data-original)"

            yield {
                "store": store,
                "name": box_item.css(NAME_SELECTOR).extract_first().replace('/', ''),
                "url": box_item.css(URL_SELECTOR).extract_first(),
                "price": box_item.css(PRICE_SELECTOR).extract_first(),
                "url_image": "https:" + box_item.css(IMAGE_URL_SELECTOR).extract_first(),
                "image_urls": ["https:" + box_item.css(IMAGE_URL_SELECTOR).extract_first()],
            }
