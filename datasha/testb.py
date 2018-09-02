import fileinput
import os
import sys


def getdata(filename):
    if not os.path.exists(filename):
        print('File is not exists!')
        return
    i = -1
    rets = [0,] * 40 #用于保存结果
    # 循环获取
    for line in fileinput.input(filename):
        i += 1
        if i % 41==0:
            continue
        else:
            data = float(line.split(' ')[-1])
            rets[i%41 - 1] += data
    n = i // 41 + 1
    rets = [round(r/n,4) for r in rets]
    print(rets)
    return rets

def tofile(data,filename):
    #写入文件
    with open(filename,'wt') as f:
        for i,d in enumerate(data):
            f.write(' '.join((str(i+1),str(d))))
            f.write('\n')
            
if __name__ == '__main__':
    # 可以在命令行提供输入和输出文件名
    inputf = 'abc.txt' #默认输入文件名
    outputf = 'result.txt' #默认输出文件名
##    print(len(sys.argv),sys.argv)
    if len(sys.argv) >= 2:
        inputf = sys.argv[1]
    if len(sys.argv) >= 3:
        outputf = sys.argv[2]
        
##    print(inputf,outputf)
    data = getdata(inputf)
    tofile(data,outputf)
