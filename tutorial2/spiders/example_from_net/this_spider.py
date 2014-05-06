from scrapy.spider import BaseSpider

class thisSpider(BaseSpider):
	#~name = "dmoz"
	#~allowed_domains = ["dmoz.org"]
	#~start_urls = [
    	#~"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #~"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    #~]

	def parse(self, response):
		filename = response.url.split("/")[-2]
		open(filename, 'wb').write(response.body)
		
	
	# Page1 & then Page2
	# Maybe inside, main parse() func, 
	# i can also just use fetch,
	# on all listpage items & next_links 
	# & then call page2 on it
	#~def parse_page1(self, response):
		#~item = MyItem()
		#~item['main_url'] = response.url
		#~request = Request("http://www.example.com/some_page.html",
						  #~callback=self.parse_page2)
		#~request.meta['item'] = item
		#~return request
#~
	#~def parse_page2(self, response):
		#~item = response.meta['item']
		#~item['other_url'] = response.url
		#~return item		
#~
#~
