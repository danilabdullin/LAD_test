# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.jobs

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['salary_'] = self.clean_up_salary(item['salary'])
        del item['salary']
        collection.insert_one(item)

        return item

    def clean_up_salary(self, salary_list: list):
        # cleaning salary data
        result_list = []
        if salary_list:
            for i in salary_list:
                i = i.strip().replace('\xa0', '').replace(' ', '')
                if i:
                    result_list.append(i)
            return " ".join(result_list)
        return salary_list



