# -*- coding: UTF-8 -*-

import os

def get_data(filename,headlines=5):
    years = []
    temperatures = []
    if not os.path.exists(filename):
        print('File is not exist!')
        return
    datas = None
    with open(filename) as my_file:
        datas = my_file.readlines()[5:]
    if datas:
        datas = [line.strip() for line in datas]
        for data in datas:
            year,temperature = data.split(',')
            years.append(year)
            temperatures.append(float(temperature))
        with open('tempAnomaly.txt','w+') as my_file:
            my_file.write("Year\tValue")
            for year,temp in zip(years,temperatures):
                my_file.write('\n')
                my_file.write(year)
                my_file.write('\t')
                my_file.write("{:.4f}".format(temp))


if __name__ == '__main__':
    get_data('Sacramento-1880-2018.NOAA.csv')