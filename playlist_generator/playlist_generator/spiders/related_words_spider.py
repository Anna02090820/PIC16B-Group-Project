# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class wordsSpider(scrapy.Spider):
    name = 'related_words_spider'
    ui="bakery"
    start_urls = ["https://relatedwords.io/"] 
  
    def parse(self, response):
<<<<<<< Updated upstream
            """
            """
            cast_url=response.url + self.ui 
            yield scrapy.Request(cast_url,callback=self.parse_word_links)
            #acesses the cast and crew page
     
    def parse_word_links(self,response):
        #get the links and yield a request to parse_related_words in each link page
=======
        """
        """
        cast_url=response.url + ui 
        yield scrapy.Request(cast_url,callback=self.parse_related_words)
        #acesses the cast and crew page

    def parse_word_links(self.response):
        
    
    def parse_related_words(self,response):
>>>>>>> Stashed changes
    
    def parse_related_words(self,response):
        
            words=response.css('span.term a::text')[0:10].getall()
        
            for word in words:
                yield{
                    "topic": self.ui,
                    "related_word": word
                }
