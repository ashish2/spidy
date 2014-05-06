"""
From page
http://doc.scrapy.org/en/0.18/topics/spiders.html
"""

"""
XMLFeedSpider example
These spiders are pretty easy to use, let’s have a look at one example:
"""

from scrapy import log
from scrapy.contrib.spiders import XMLFeedSpider
from myproject.items import TestItem

class MySpider(XMLFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.xml']
    iterator = 'iternodes' # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        log.msg('Hi, this is a <%s> node!: %s' % (self.itertag, ''.join(node.extract())))

        item = Item()
        item['id'] = node.select('@id').extract()
        item['name'] = node.select('name').extract()
        item['description'] = node.select('description').extract()
        return item

"""
Basically what we did up there was to create a spider that downloads a feed from the given start_urls, and then iterates through each of its item tags, prints them out, and stores some random data in an Item.
"""
