# Dmoz Spider

import os

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from tutorial2.items import DmozItem

class DmozSpider(BaseSpider):
	name = "dmoz"
	allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
	]
	
	def parse(self, response):
		
		#~filename = response.url.split("/")[-2]
		#~self_name = self.__class__.__name__
		#~f = 'responses/' + self_name 
		#~if not os.path.exists(f):
			#~os.makedirs(f)
		#~f = f + '/' + filename
		#~open(f, 'w+').write(response.body)
		
		hxs = HtmlXPathSelector(response)
		sites = hxs.select('//ul/li')
		items = []
		
		for site in sites:
			item = DmozItem()
			item['title'] = site.select('a/text()').extract()
			item['link'] = site.select('a/@href').extract()
			item['desc'] = site.select('text()').extract()
			items.append(item)
			
		return items
	


