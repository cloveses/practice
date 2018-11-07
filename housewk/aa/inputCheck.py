# -*- coding: UTF-8 -*-

def check(data):
    if data.isdigit():
        data = int(data)
        if 0 <= data <= 60:
            return data
