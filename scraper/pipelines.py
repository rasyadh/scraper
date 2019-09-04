# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item
        
class ScraperImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item["image_urls"][0]
        meta = { 
            "store": item["store"],
            "name": item["name"], 
            "price": item["price"],
        }
        yield scrapy.Request(url=img_url, meta=meta, dont_filter=True)

    def file_path(self, request, response=None, info=None):
        filename = request.meta.get("store") + "_" + request.meta.get("name") + '_' + request.meta.get("price")
        return "full/{}/{}.jpg".format(request.meta.get("store"), filename)