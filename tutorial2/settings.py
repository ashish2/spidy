# Scrapy settings for tutorial2 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys

folderName = ''

try:
	if sys.argv[2]:
		folderName = sys.argv[2]
except:
	print "Error"


BOT_NAME = 'tutorial2'

SPIDER_MODULES = ['tutorial2.spiders']
NEWSPIDER_MODULE = 'tutorial2.spiders'

# For Downloading IMAGES
ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
#~IMAGES_STORE = 'downloaded_images'
IMAGES_STORE = '/opt/lampp/htdocs/ash3_opt_www/www2/python/venv/pyth_django/scrapy/1/tutorial2/downloaded_images/'+folderName
# 90 days of delay for image expiration
IMAGES_EXPIRES = 90

IMAGES_THUMBS = {
	'small': (50, 50),
	'big': (270, 270),
}


DOWNLOAD_DELAY = 1.0

# AUTOTHROTTLE
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 60.0

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial2 (+http://www.yourdomain.com)'
