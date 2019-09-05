import os
import re
import scrapy
from scrapy_splash import SplashRequest
from scraper.items import ImageItem
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from scraper.spiders import blibli_urls 

class BlibliSpider(scrapy.Spider):
    name = "bliblispider"
    PAGE_LIMIT = 3
    OUTPUT_PATH = "outputs/blibli/"

    def __init__(self):
        # opts = Options()
        # opts.headless = True
        # self.driver = Chrome(options=opts)
        self.driver = Chrome()

    def splash_start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())

        urls = self.list_urls
        for url in urls:
            request = SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 10.0})
            request.meta['download_timeout'] = 90
            yield request

    def start_requests(self):
        self.logger.info("current working directory is : %s" % os.getcwd())
        
        urls = blibli_urls.brands_url[50:]
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 20)
        products = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'product__card')))

        store = response.url.split('?')[0].split('/')[-1]
        for product in products:
            name = product.find_element_by_class_name('product__title').get_attribute('title')
            price = product.find_element_by_class_name('product__body__price__display').text
            image_url = product.find_element_by_css_selector('div.product__image img').get_attribute('data-src')

            yield {
                'store': store.replace('-', ' ').replace(u'\xa0', u' ').strip(),
                'name': name.replace('/', '').strip(),
                'price': price.strip(),
                'image_urls': [image_url],
            }
        
        # self.driver.close()

    def og_parse(self, response):
        CATEGORY_SELECTOR = 'div.product-listing__seo-top h1::text'
        category = response.css(CATEGORY_SELECTOR).extract_first()
        print(category)
        print()

        PRODUCT_CARD_SELECTOR = 'div.product__card'
        for product in response.css(PRODUCT_CARD_SELECTOR):
            NAME_SELECTOR = 'span.product__title__name'
            name = product.css(NAME_SELECTOR).extract_first()
            print(name)