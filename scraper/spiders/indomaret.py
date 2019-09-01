import os
import re
import json
import scrapy
from scraper.items import ImageItem
from scraper.spiders import indomaret_urls

class IndomaretSpider(scrapy.Spider):
    name = "indomaretspider"
    PAGE_LIMIT = 2
    OUTPUT_PATH = "outputs/indomaret/"
    
    # change according to urls you want to scrap
    all_brand_url = [ "https://www.klikindomaret.com/brand" ]

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        urls = indomaret_urls.brands_11_urls
        for url in urls:
            request = scrapy.Request(url=url+"?sortcol=populer", callback=self.parse)
            yield request

    def get_brands_links(self, response):
        ALL_BRAND_SELECTOR = ".box-item.brand-list-name"
        all_brand = response.css(ALL_BRAND_SELECTOR)

        ITEM_SELECTOR = "a::attr(href)"
        items = all_brand.css(ITEM_SELECTOR).extract()

        links = []
        for item in items:
            links.append("https://www.klikindomaret.com{}".format(item))
        print(json.dumps(links))

    def parse(self, response):
        # get all links brands
        # self.get_brands_links(response)

        STORE_SELECTOR = 'div.breadcrumb.nobg a:nth-child(n+2)::text'
        store = response.css(STORE_SELECTOR).extract_first()
        
        RESULT_SELECTOR = 'div.box-item.clearfix'
        result = response.css(RESULT_SELECTOR)

        index = 1
        for item in result.css("div.item"):
            if index > 50:
                break

            # print(item.css('img.lazy::attr(data-src)').extract_first())

            URL_SELECTOR = "a::attr(href)"
            url = "https://www.klikindomaret.com" + item.css(URL_SELECTOR).extract_first()

            yield scrapy.Request(url, callback=self.parse_detail, meta={"store": store})

            index += 1
    
    def parse_detail(self, response):
        NAME_SELECTOR = "div.each-section.section-title h3::text"
        PRICE_SELECTOR = "span.normal.price-value::text"
        IMAGE_URL_SELECTOR = "img#zoom_03::attr(src)"

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