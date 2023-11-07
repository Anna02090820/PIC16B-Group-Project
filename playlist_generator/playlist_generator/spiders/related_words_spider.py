# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class wordsSpider(scrapy.Spider):
    name = 'related_words_spider'
    start_urls = ["https://relatedwords.io/"] 

    def _init_(self, **kwargs):
        super()._init_(**kwargs)
  
    def parse(self, response):
        """
        """
        topic_url=response.url + "-".join((self.ui).lower().split())
        yield scrapy.Request(topic_url,callback=self.parse_word_links)
     
    def parse_word_links(self, response):
        """
        get the links of first 10 keywords of user input's word
        """
        #gets links from page
        related_words=response.css('span.term a::text')[0:10].getall()
        link_list=["https://relatedwords.io/" + "-".join((word).split()) for word in related_words]
        
        # get the link for the first 10 related words 
        for link in link_list:
             yield scrapy.Request(url=link, callback = self.parse_related_words)
    
    def parse_related_words(self,response):
        
        words=response.css('span.term a::text')[0:10].getall()
    
        for word in words:
            yield{
                "topic": response.css('title::text').get().split(" Words")[0].lower(),
                "related_word": word
            }
