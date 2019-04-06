# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import connections


class SpiderPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1', user='root', passwd='', db='recruit', use_unicode=False, charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            city = item['city']
            district = item['district']
            title = item['title']
            job_salary = item['job_salary']
            company = item['company']
            edu = item['edu']
            exp = item['exp']
            come_from = item['come_from']

            sql = "insert into s_data(city, district, title, job_salary, company, edu, exp, come_from) VALUES(%s,%s,%s,%s,%s,%s,%s, %s)"
            self.cursor.execute(sql, (city, district, title,
                                      job_salary, company, edu, exp, come_from))
            self.conn.commit()
            return item
        except Exception, err:
            print err.message

        return item

    def close_spider(self, spider):
        self.conn.close()
