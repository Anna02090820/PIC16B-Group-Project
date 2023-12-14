# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class wordsSpider(scrapy.Spider):
    name = 'related_words_spider'
    start_urls = ["https://relatedwords.io/"] 

    def _init_(self, **kwargs):
        """
        Initialize the spider with the given keyword arguments.

        :param kwargs: Keyword arguments passed to the spider.
        """
        super()._init_(**kwargs)
  
    def parse(self, response):
        """
        Parse the initial response from the start URL and generate a request to
        fetch related words for a given topic.

        param response: The response object from the initial request to the start URL.
        return: Yields a scrapy Request for fetching related words for a specific topic.
        """
        topic_url=response.url + "-".join((self.ui).lower().split())
        yield scrapy.Request(topic_url,callback=self.parse_word_links)
     
    def parse_word_links(self, response):
         """
        Parse the response to extract the first 10 related words and generate requests
        to fetch more related words for each.

        param response: The response object containing the initial set of related words.
        return: Yields scrapy Requests for each of the first 10 related words.
        """
        #gets links from page
        related_words=response.css('span.term a::text')[0:10].getall()
        link_list=["https://relatedwords.io/" + "-".join((word).split()) for word in related_words]
        
        # get the link for the first 10 related words 
        for link in link_list:
             yield scrapy.Request(url=link, callback = self.parse_related_words)
    
    def parse_related_words(self,response):
        """
        Parse the response to extract and yield the first 10 related words 
        from the following links.

        param response: The response object from the following link, containing additional related words.
        return: Yields a dictionary containing the 'topic' and each 'related_word'.
        """
        words=response.css('span.term a::text')[0:10].getall()
    
        for word in words:
            yield{
                "topic": response.css('title::text').get().split(" Words")[0].lower(),
                "related_word": word
            }
