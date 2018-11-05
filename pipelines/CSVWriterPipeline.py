# -*- coding: utf-8 -*-

import csv


class CSVWriterPipeline:
    
    def __init__(self, file_path):
        self.file_path = file_path

    def open_spider(self):
        self.file = open(file_path, 'w', newline='')

    def close_spider(self):
        self.file = close()

    def process_item(self, item):
        fieldnames = items.keys()
        writer = csv.DictWrite(self.file, fieldnames=fieldnames)

        write.writeheader()
        write.writerow(dict(item))

        return item


