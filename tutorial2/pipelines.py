# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class Tutorial2Pipeline(object):
    def process_item(self, item, spider):
        return item

# Compuindia Images PIPELINE
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class CompuindiaImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images")
		item['image_paths'] = image_paths
		return item

#-

class FlipkartImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images")
		item['image_paths'] = image_paths
		return item


class Homeshop18ImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		print "item['image_urls']"
		print item['image_urls']

		for image_url in item['image_urls']:
			yield Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images")
		item['image_paths'] = image_paths
		return item




