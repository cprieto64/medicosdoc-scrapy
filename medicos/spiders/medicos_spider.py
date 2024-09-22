# from symbol import pass_stmt
import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

# from scraper_api import ScraperAPIClient

from pymongo import MongoClient
import time
import re
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb+srv://user:pass@cluster0.mamup.mongodb.net')
db = client['medicosdoc']
col = db['instituciones-scrapeops']


class Empresa(Item):
    nombre_premium = Field()
    # telefono = Field()

class MedicosDoc(CrawlSpider):
    name = 'medicosdoc'
    custom_settings = {        
    "DOWNLOADER_MIDDLEWARES": { # pip install Scrapy-UserAgents and pip install scrapy_proxy_pool and pip install scrapy-user-agents
        # 'scrapyx_scraperapi.ScraperApiProxyMiddleware': 610,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    },    
    "USER_AGENTS": [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        # chrome
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        # chrome
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',  # firefox
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        # chrome
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        # chrome
    ],
    # pip install scrapyx-scraperapi-v2 and pip install scraperapi-sdk https://snyk.io/advisor/python/scrapyx-scraperapi-v2
    #"SCRAPERAPI_ENABLED" : True,
    #"SCRAPERAPI_KEY" : 'c93021d36148fad4a9a44d9cc46c803d',
    #"SCRAPERAPI_RENDER" : False,
    #"SCRAPERAPI_PREMIUM" : False,
    #"SCRAPERAPI_COUNTRY_CODE": 'US',
    
    #"PROXY_POOL_ENABLED" : True,
    'LOG_LEVEL' : 'ERROR',

    'CLOSESPIDER_PAGECOUNT': 50,
    #'CONCURRENT_REQUESTS': 1,   
    #'FEED_EXPORT_FIELDS': ['titulo', 'telefono', 'actividad', 'nit', 'ciudad', 'direccion'],  # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    'FEED_EXPORT_ENCODING': 'utf-8'
    }

    allowed_domain = ['https://medicosdoc.com']
    start_urls = ['https://medicosdoc.com/categoria/instituciones-barranquilla']

    # download_delay = 1

    rules = {
        # Para cada item
        Rule(LinkExtractor(allow = (), restrict_xpaths = ('//ul[@class="pagination"]/li/a[@id="ContentPlaceHolderContent_ResultMedicos_RepeaterPager_HyperLinkNext"]'))),
        Rule(LinkExtractor(allow =(), restrict_xpaths = ('//ul[@id="resultmedicos"]/li//h3/a')),
                            callback = 'parse_item', follow = False)
    }

    def parse_item(self, response):

        """Parses and processes doctor information from a web page response.
        
        Args:
            self: The instance of the class containing this method.
            response (scrapy.http.Response): The response object containing the web page data.
        
        Returns:
            None: This method doesn't return a value, but updates a database collection with doctor information.
        """        nombre_premium = response.xpath('.//div[@class="headerprofilepremium"]/h1/text()').get()
         
        
        if nombre_premium is None:
            nombre = response.xpath('.//article[@class="detailfree"]/main/h3/text()').get()
            nombre = nombre.strip()
        else:
            nombre = nombre_premium.strip()

        doctor_id = hashlib.md5(nombre.encode('utf-8')).hexdigest()

        tel_premium = response.xpath('.//p[@class="vertelefonos"]/a/@data-tels').get()
        phone = []
        if tel_premium is None:
            tel = response.xpath('.//p[@id="ContentPlaceHolderContent_contentphonefree"]/a/@data-tels').get()
            if "," in tel:
                tel= tel.split(",")               
                # phone = []
                for i in tel:
                    tel = re.sub(r'[^0-9]', '', i)
                    # print(result)
                    phone.append(tel)
                # print(phone)
            else:
                tel = re.sub(r'[^0-9]', '', tel)
                phone.append(tel)
                # print(tel)          
        else:
            tel= tel_premium.split(",")
            # phone = []
            for i in tel:
                tel = re.sub(r'[^0-9]', '', i)
                phone.append(tel)
            # print(phone)

        especializacion_premium = response.xpath('.//div[@class="headerprofilepremium"]/h3/a/text()').getall()
        # print(len(especializacion_premium), response.url)
        if len(especializacion_premium) <= 0:            
            especializacion = response.xpath('.//article[@class="detailfree"]/main/h5/a/text()').getall()
            
            if "Barranquilla" in especializacion:
                especializacion = especializacion.replace("Barranquilla", "")
                especializacion = especializacion.strip()
                # print(especializacion)
            else:
                pass
        else:           
            especializacion = especializacion_premium
            # print(especializacion)
            # if "Barranquilla" in especializacion_premium:
            #     especializacion_premium = especializacion_premium.replace("Barranquilla", "")
            #     especializacion = especializacion_premium.strip()
            #     # print(especializacion)
            # else:
            #     pass
        
        
        location_free = response.xpath('.//article[@class="detailfree"]/main/p[@class="doclocation"]/text()').getall()
        if location_free:
            if len(location_free) > 0:
                address = []            
                for i in location_free:
                
                    location = i.replace("\n", "")
                    location = re.sub(' {2,}', ' ', location)
                    location = location.strip()
                    address.append(location)
                    
                    #print(address) 
                    # print(location)
                    # print(response.url)
                    
                    ubi = ''.join(address)
                    # ubi = ubi.replace("Barranquilla, Colombia", ". Barranquilla, Colombia")
                    # location = re.sub(' {2,}', ' ', location)
                    # location = location.strip()
                # print(ubi)
                
                
            else:
                pass
        
        else:
            location_premium = response.xpath('.//p[@class="doclocation"]/text()').getall()
            
            if len(location_premium) > 0:
                address_premium = []            
                for i in location_premium:
                    
                    location = i.replace("\n", "")
                    location = re.sub(' {2,}', ' ', location)
                    location = location.strip()
                    # print(location)
                    address_premium.append(location)
                    # print(address_premium)
                    # print(adress) 
                    # print(location)
                    # print(response.url)
                    
                    ubi = ' '.join(address_premium)
                    # ubi = ubi.replace("Barranquilla, Colombia", " Barranquilla, Colombia")                    
                    # location = re.sub(' {2,}', ' ', location)
                    # location = location.strip()
                # print(ubi)               
                
            else:
                pass
        
        seguro = response.xpath('.//p[@class="insurancesaccepted"]/text()[2]').get()
        
        if seguro:
            seguro = seguro.strip()
            # print(len(seguro), response.url)
            if len(seguro) > 1:
                seguro = seguro            
        else:
            seguro = "N/A"        
        

        get_item_id = col.find_one({'doctor_id' : doctor_id}, {'_id': 1})
        
        if get_item_id is not None:
            get_item_id = get_item_id["_id"]
            get_item_id = col.find_one({'_id': ObjectId(get_item_id) })           
            get_nombre = get_item_id["doctor_id"]
            print(f"DUPLICATED: {get_nombre}")

            col.update_one({
                'doctor_id': doctor_id
            }, {
            '$set': {
                'doctor_id': doctor_id,
                'nombre': nombre,
                'telefono': phone,
                'especializacion': especializacion,
                'seguro': seguro,
                'direccion': ubi,
                'source': response.url,
                # 'Website': website,
                # 'Ciudad': ciudad,
                # 'Direccion': direccion,
                # 'Slogan': slogan 
                }
            }, upsert=True)
        else:
            print(f"SAVE: {nombre}")

            col.update_one({
                'doctor_id': doctor_id
            }, {
            '$set': {
                'doctor_id': doctor_id,
                'nombre': nombre,
                'telefono': phone,
                'especializacion': especializacion,
                'seguro': seguro,
                'direccion': ubi,
                'source': response.url,
                # 'Website': website,
                # 'Ciudad': ciudad,
                # 'Direccion': direccion,
                # 'Slogan': slogan 
                }
            }, upsert=True)


# scrapy runspider odontologos.py