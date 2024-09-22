# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MedicosPipeline:
    def process_item(self, item, spider):
        """
        Process a scraped item.
        
        Args:
            item (dict): The scraped item to be processed.
            spider (scrapy.Spider): The spider that scraped the item.
        
        Returns:
            dict: The processed item, unmodified in this implementation.
        """
        return item
