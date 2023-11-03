# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class wordsSpider(scrapy.Spider):
    name = 'related_words_spider'
    ui="bakery"
    start_urls = ["https://relatedwords.io/"] 
  
    def parse(self, response):
        """
        """
        topic_url=response.url + self.ui 
        yield scrapy.Request(topic_url,callback=self.parse_word_links)
     
    def parse_word_links(self,response):
        #get the links and yield a request to parse_related_words in each link page
    
    def parse_related_words(self,response):
        
        words=response.css('span.term a::text')[0:10].getall()
        words.append(response.css('title::text').get().split(" Words")[0].lower())
    
        for word in words:
            yield{
                "topic": self.ui,
                "related_word": word
            }
