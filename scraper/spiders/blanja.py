import os
import re
import scrapy
from scraper.items import ImageItem
from scraper.spiders import blanja_urls

class BlanjaSpider(scrapy.Spider):
    name = "blanjaspider"
    PAGE_LIMIT = 3
    OUTPUT_PATH = "outputs/blanja/"

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        urls = blanja_urls.new2_list
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        # Global Brand
        # STORE_SELECTOR = 'h1.fColor-orange a::text'
        # store = response.css(STORE_SELECTOR).extract_first()

        # Category Brand
        # store = response.url.split("?")[0].split("/")[-1]
        # Category Brand Search
        store = response.url.split("shopKeyWords=")[1].split("&")[0]
        store = re.sub("[^\w]", " ", store).strip().upper()

        RESULT_SELECTOR = ".result-thumbs"
        result = response.css(RESULT_SELECTOR)

        BOX_SELECTOR = "div.box-item"
        for box_item in result.css(BOX_SELECTOR):
            NAME_SELECTOR = ".item-title a::text"
            PRICE_SELECTOR = ".price::text"
            IMAGE_URL_SELECTOR = ".item-image a img.lazy::attr(data-original)"

            name = box_item.css(NAME_SELECTOR).extract_first().replace('/', '').strip()
            price = box_item.css(PRICE_SELECTOR).extract_first().strip()
            image = box_item.css(IMAGE_URL_SELECTOR).extract_first()
            image_url = ""
            if "blanja" in image:
                if image.endswith('.jpg'):
                    image_url = image
                else:
                    image_url = image[:len(image) - 3] + "720"
                if "https://" not in image_url:
                    image_url = "https://" + image_url
                elif "https:" not in image_url:
                    image_url = "https:" + image_url
            else:
                image_url = image

            yield {
                "store": store.strip(),
                "name": name,
                "price": price,
                "image_urls": [image_url],
            }

        NEXT_PAGE_SELECTOR = "a.btn.next::attr(href)"
        next_page_url = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page_url is not None:
            next_page = int(next_page_url.split("pageNo=")[1][:1])

            if next_page <= self.PAGE_LIMIT:
                yield scrapy.Request(
                    response.urljoin(next_page_url),
                    callback=self.parse
                )
        