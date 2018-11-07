# -*- coding: UTF-8 -*-

import os

def get_data(filename,headlines=5):
    if os.path.exists(filename):
        datas = None
        with open(filename) as my_file:
            datas = my_file.readlines()[5:]
        if datas:
            datas = [line.strip() for line in datas]
            for data in datas:
                print(data)

if __name__ == '__main__':
    get_data('Sacramento-1880-2018.NOAA.csv')