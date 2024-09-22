# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MedicosSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        """Create and initialize a spider instance from a Scrapy crawler.
        
        Args:
            cls (type): The class of the spider being instantiated.
            crawler (scrapy.crawler.Crawler): The Scrapy crawler object.
        
        Returns:
            Spider: An instance of the spider class with initialized signal connections.
        """        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        """Process the input for the spider.
        
        Args:
            response (object): The response object that goes through the spider middleware.
            spider (object): The spider instance processing the response.
        
        Returns:
            """
            Process the output of a spider after it has processed a response.
            
            Args:
                response: The response object that was processed by the spider.
                result (Iterable): The results returned from the spider after processing the response.
                spider: The spider instance that processed the response.
            
            Returns:
                Iterable: An iterable of Request or item objects yielded from the input result.
            """
            None: This method should return None or raise an exception.
        """
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        """
        Process spider exceptions and handle the response.
        
        Args:
            response (object): The response object from the spider.
            exception (Exception): The exception raised during spider processing.
            spider (object): The spider instance that raised the exception.
        
        Returns:
            None or iterable: None or an iterable of Request or item objects.
        """
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        """Process the start requests of a spider.
        
        Args:
            start_requests (iterable): An iterable of Request objects to process.
            spider (Spider): The spider instance associated with these requests.
        
        Returns:
            generator: A generator yielding Request objects.
        """
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """
        Handles the event when a spider is opened.
        
        Args:
            spider (Spider): The spider instance that has been opened.
        
        Returns:
            None: This method doesn't return anything.
        """
        spider.logger.info('Spider opened: %s' % spider.name)

"""
Creates and initializes a spider instance from a crawler.

Args:
    cls (class): The class of the spider being instantiated.
    crawler (scrapy.crawler.Crawler): The crawler object associated with this spider.

Returns:
    Spider: An instance of the spider class with initialized signals.
"""

class MedicosDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    """Processes a request in the downloader middleware.
    
    Args:
        request (Request): The request object to be processed.
        spider (Spider): The spider instance that generated the request.
    
    Returns:
        None or Response or Request: 
        - None to continue processing the request.
        - Response object to return a response directly.
        - Request object to return a new request.
        - May also raise IgnoreRequest to trigger process_exception() methods.
    """
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        """Process an exception that occurred during request handling.
        
        Args:
            request (Request): The request that caused the exception.
            exception (Exception): The exception that was raised.
            spider (Spider): The spider instance that generated the request.
        
        Returns:
            Optional[Union[Response, Request]]: None to continue processing the exception,
            a Response object to stop the process_exception() chain, or a Request object
            to stop the process_exception() chain.
        """
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    """Process the response returned from the downloader.
    
    Args:
        self: The instance of the class containing this method.
        request (Request): The request object that generated this response.
        response (Response): The response object returned from the downloader.
        spider (Spider): The spider instance that is handling the response.
    
    Returns:
        Response: The processed response object, which can be modified if needed.
    """
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        """Called when a spider is opened.
        
        Args:
            spider (Spider): The spider instance that was opened.
        
        Returns:
            None: This method doesn't return anything.
        """
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
