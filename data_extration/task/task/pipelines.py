# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class TaskPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn=sqlite3.connect('bayut.db')
        self.curr=self.conn.cursor()

    def create_table(self):
        self.curr.execute('''DROP TABLE IF EXISTS bayut_table''')
        self.curr.execute('''CREATE TABLE bayut_table(
            property_id text
            purpose text
            type text
            added_on text
            furnishing text
            priceDict text
            permit_number text
            agent_name text
            location text
            bbsDict text
            image_url text
            breadcrumbs text
            f1 text
            description text
            )''')


    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute('''insert on bayut_table values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(
            item['property_id'][0],
            item['purpose'][0],
            item['type'][0],
            item['added_on'][0],
            item['furnishing'][0],
            item['priceDict'][0],
            item['permit_number'][0],
            item['agent_name'][0],
            item['location'][0],
            item['bbsDict'][0],
            item['image_url'][0],
            item['breadcrumbs'][0],
            item['f1'][0],
            item['description'][0],

        ))
        self.conn.commit()
