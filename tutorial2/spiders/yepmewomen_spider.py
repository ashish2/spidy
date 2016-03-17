# Yep Me Women Spider

# Needed 
# 21 + 25 + 65 + 13 + 41 = 165 in CompuIndia
#1] Got: only, 106, total products/items are around 165 on website, CHECK Y? - 
#2] GET IMAGES NOW - DONE
#3] In IMAGES, item['image_paths'] have not come in json file, check y?, item['image_paths'] is mentioned in ImagePipelines - 

# filename = response.url.split("/")[-2]
# self_name = self.__class__.__name__
# f = 'responses/' + self_name 
# if not os.path.exists(f):
# 	os.makedirs(f)
# f = f + '/' + filename
# open(f, 'w+').write(response.body)



from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial2.items import YepmewomenItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import *
import sys, re, os



class YepmewomenSpider(CrawlSpider):
	name = 'compuindia'
	allowed_domains = ['compuindia.']
	start_urls = ['http://www.compuindia.']
	
	urlList = []
	
	def pv(value):
		"""This function takes values links from Rules, and can process those links in any manner"""
		# Removing a link having "deals.html" in it, as we dont want that link to be crawled
		if re.search('.*deals\.html', value):
			return None
		else:
			return value
	
	# NOT USED FTM
	def pl(value):
		print sys._getframe().f_code.co_name
		print 'value'
		print type(value)
		print value
		print 'length: ' + str( len(value))
		sys.exit('X')
	
	def parse_item(response):
		hxs = HtmlXPathSelector(response)
		
		# ATM, all these item values are coming in a List type with just the 0th key
		item = YepmewomenItem()

		item['sourceurl'] = [ response.url ]
		item['code'] = hxs.select('//td[@class="data"]/text()')[0].extract().encode('utf-8') # Code: String
		item['price'] = hxs.select('//span[@class="price"]/text()')[0].extract().encode('utf-8')

		item['discountPrice'] = []
		item['sizes'] = []
		item['color'] = []

		item['name'] = hxs.select("//div[@class='product-name']/h1/text()").extract()[0]
		item['features'] = [None]
		item['specs'] = [None]
		item['description'] = hxs.select('//div[@class="box-collateral box-description"]').extract()[0].encode('utf-8')
		item['moreDescription'] = [None]
		item['additionalInfo'] = hxs.select('//div[@id="additional"]').extract()[0].encode('utf-8')		
		item['relatedProducts'] = [None] # FTM
		
		#IMAGES
		main_img = []
		image_urls = []
		main_img = hxs.select("//p[@class='product-image']/a/@href").extract()
		img_urls = hxs.select("//div[@class='more-views']/ul/li/a/@href").extract()		
		item['image_urls'] =  list( set( main_img + img_urls ) )
		#IMAGES-		
		#~sys.exit('S')
		return item
		
		
	rules = (
		#PAGE2: NEXT LINKS
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//a[@class='next i-next']", ] ), follow=True ),
		# PAGE2: PRODUCT LINKS
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='category-products']" ], deny = [".*dir=.*", ".*order=.*", ],  ), callback=parse_item , follow = False ),
		### 1st Page
		Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='parentMenu']", deny = [".*deals\.htm.*"], ) , follow=True ),
	)
	



