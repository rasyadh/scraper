import os
import re
import scrapy
from scraper.items import ImageItem
from scraper.spiders import idmarco_urls

class IDMarcoSpider(scrapy.Spider):
    name = "idmarcospider"
    PAGE_LIMIT = 3
    OUTPUT_PATH = "outputs/idmarco/"
    
    # change according to urls you want to scrap
    list_urls = idmarco_urls.babymother_urls

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        urls = self.list_urls
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        STORE_SELECTOR = 'li.current strong::text'
        store = response.css(STORE_SELECTOR).extract_first()

        RESULT_SELECTOR = "ul.products-grid"
        result = response.css(RESULT_SELECTOR)

        ITEM_SELECTOR = "li.item"
        index = 1

        for item in result.css(ITEM_SELECTOR):
            if index > 50:
                break

            URL_SELECTOR = "h2.product-name a::attr(href)"
            url = item.css(URL_SELECTOR).extract_first()

            yield scrapy.Request(url, callback=self.parse_detail, meta={"store": store})

            index += 1
        
    def parse_detail(self, response):
        NAME_SELECTOR = "div.product-name h1::text"
        PRICE_SELECTOR = "span.price::text"
        IMAGE_URL_SELECTOR = "img.etalage_thumb_image::attr(src)"

        store = response.meta.get("store").strip()
        name = response.css(NAME_SELECTOR).extract_first().replace('/', '').strip()
        price = response.css(PRICE_SELECTOR).extract_first().strip()
        image_url = response.css(IMAGE_URL_SELECTOR).extract_first()

        yield {
            "store": store,
            "name": name,
            "price": price,
            "image_urls": [image_url],
        }