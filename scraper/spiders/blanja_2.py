import os
import re
import scrapy

class Blanja2Spider(scrapy.Spider):
    name = "blanja2scraper"
    PAGE_LIMIT = 5
    OUTPUT_PATH = "output/blanja/"
    proxy_meta = ""
    list_urls = [
        "https://www.blanja.com/katalog/c/fnb/kuliner-indonesia",
        "https://www.blanja.com/katalog/c/fnb/sembako",
        "https://www.blanja.com/store/unileverofficialstore",
    ]

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        for url in self.list_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        PRODUCT_BOX_SELECTOR = "div.product-box"
        for product_box in response.css(PRODUCT_BOX_SELECTOR):
            URL_SELECTOR = '.prod-anchor::attr(href)'
            NAME_SELECTOR = '.product-name::text'
            PRICE_SELECTOR = '.product-price::text'
            IMAGE_SELECTOR = 'img.lazy ::attr(data-original)'

            product = {
                "name": product_box.css(NAME_SELECTOR).extract_first(),
                "url": product_box.css(URL_SELECTOR).extract_first(),
                "price": product_box.css(PRICE_SELECTOR).extract_first(),
                "image_url": product_box.css(IMAGE_SELECTOR).extract_first()[2:],
            }
            
            yield {
                'url': product_box.css(URL_SELECTOR).extract_first(),
                'name': product_box.css(NAME_SELECTOR).extract_first(),
                'price': ''.join(re.findall("\d+", product_box.css(PRICE_SELECTOR).extract_first())),
                'image_url': product_box.css(IMAGE_SELECTOR).extract_first()[2:],
            }

        BOX_SELECTOR = "div.box-item"
        for box_item in response.css(BOX_SELECTOR):
            NAME_SELECTOR = ".item-title a::text"
            URL_SELECTOR = ".item-title a::attr(href)"
            PRICE_SELECTOR = ".price::text"
            IMAGE_URL_SELECTOR = ".item-image a img.lazy::attr(data-original)"

            yield {
                "name": box_item.css(NAME_SELECTOR).extract_first(),
                "url": box_item.css(URL_SELECTOR).extract_first(),
                "price": box_item.css(PRICE_SELECTOR).extract_first(),
                "image": box_item.css(IMAGE_URL_SELECTOR).extract_first(),
            }

    def store_data(self, data):
        directory = os.path.join(os.path.dirname(os.getcwd()), self.output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, 'blanja.json')
        if not os.path.isfile(filename):
            a.append(product)
            with open(filename, mode='w',encoding='utf-8') as f:
                f.write(dumps(a, indent=4,cls=PythonObjectEncoder))
        else:
            with open(filename) as feedsjson:
                feeds = loads(feedsjson.read(),object_hook=self.as_python_object)
            feeds.append(product)
            with open(filename, mode='w',encoding='utf-8') as f:
                f.write(dumps(feeds, indent=4,cls=PythonObjectEncoder))
        self.logger.info('Processed : %s' % product_details["title"])