# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class playlistSpider(scrapy.Spider):
    name = 'playlist_spider'
    ui="bakery"
    start_urls = ["https://relatedwords.io/"] 
  
def parse(self, response):
        """
        """
        cast_url=response.url + ui 
        yield scrapy.Request(cast_url,callback=self.parse_related_words)
        #acesses the cast and crew page

def parse_related_words(self,response):
    
        words=response.css('span.term a::text')[0:10].getall()
    
        for word in words:
            yield{
                "topic":ui,
                "related_word": word
            }
