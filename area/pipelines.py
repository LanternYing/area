# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AreaPipeline(object):
    # def __init__(self):
        # self.file = open('results.txt', 'a+')

    def process_item(self, item, spider):
        line = item['number'] + '\t' + item['distinct'] + '\t' + item['location'] + '\t' + item['area'] + \
        '\t' + item['application'] + '\t' + item['way'] + '\t' + item['date'] + '\t' + item['price'] + '\n'
        line = line.encode('utf8')
        with open('results.txt', 'a+') as f:
            f.write(line)
        # print line
        # self.file.write(line)
        return item
