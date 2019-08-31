import os
import re
import scrapy
from scraper.items import ImageItem

class BlanjaSpider(scrapy.Spider):
    name = "blanjaspider"
    PAGE_LIMIT = 3
    OUTPUT_PATH = "outputs/blanja/"

    officialstores_urls = [
        "https://www.blanja.com/store/perumbulogofficial?keyword=&order=orders_desc",
        "https://www.blanja.com/store/khongguanbiscuitsshop?keyword=&order=orders_desc",
        "https://www.blanja.com/store/otstoreofficial?keyword=&order=orders_desc",
        "https://www.blanja.com/store/kinoindonesia?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore?keyword=&order=orders_desc",
    ]

    pngstorecategory_list = [
        "https://www.blanja.com/store/pngofficialstore/pantene?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore/rejoice?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore/head-&-shoulder?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore/gillette?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore/herbal-essences?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore/olay?keyword=&order=orders_desc",
        "https://www.blanja.com/store/pngofficialstore/oral-b-?keyword=&order=orders_desc",
    ]

    unilevercategory_list = [
        "https://www.blanja.com/store/unileverofficialstore/body-care/dove?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/body-care/lifebuoy?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/body-care/vaseline?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/body-care/lux?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/skin-care/pond's?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/skin-care/dove?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/skin-care/vaseline?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/skin-care/citra?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/hair-care/lifebuoy?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/hair-care/tresemme?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/hair-care/clear?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/hair-care/sunsilk?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/deodorant/axe?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/deodorant/rexona?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/toothpaste/close-up?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/toothpaste/pepsodent?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/baby-care/zwitsal?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/groceries/bango?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/groceries/sariwangi?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/groceries/blueband?keyword=&order=orders_desc",
        "https://www.blanja.com/store/unileverofficialstore/groceries/molto?keyword=&order=orders_desc",
    ]

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        urls = self.unilevercategory_list
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request


    def parse(self, response):
        # Global Brand
        # STORE_SELECTOR = 'h1.fColor-orange a::text'
        # store = response.css(STORE_SELECTOR).extract_first()

        # Category Brand
        store = response.url.split("?")[0].split("/")[-1]
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
        