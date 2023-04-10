# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv

class ShowbagsPipeline:
    def open_spider(self, spider):
        self.titles = set()
        try:
            with open('showbags.csv', 'r') as fd:
                reader = csv.DictReader(fd)
                for line in reader:
                    self.titles.add(line['name'])
        except FileNotFoundError:
            pass
        
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('name') in self.titles:
            raise DropItem(f"Already processed {item}")
        self.titles.add(adapter.get('name'))
        return item
