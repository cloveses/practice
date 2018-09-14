import os
import xlrd

def get_digit(path):
    name = os.path.split(path)[-1]
    digits = list(name)
    digits = [d for d in digits if d.isdigit()]
    if digits:
        return int(''.join(digits))
    return 0

def get_files(directory):
    files = []
    files = os.listdir(directory)
    files = [os.path.join(directory,f) for f in files]
    files.sort(key=get_digit)
    return files

def get_data_cols(filename,headline_row_num=1):
    # 按列获取数据
    w = xlrd.open_workbook(filename)
    ws = w.sheets()[0]
    data = ws.col_values(0)[headline_row_num:]
    return data

def main():
    directory = input("请输入照片文件所在文件夹名:")
    filename = input("请输入命名依据电子表格文件名:")
    for f,d in zip(get_files(directory),get_data_cols(filename)):
        ext = os.path.splitext(f)[-1]
        new_name = ''.join((d,ext))
        new_name = os.path.join(os.path.split(f)[0],new_name)
        os.rename(f,new_name)

if __name__ == '__main__':
    main()
