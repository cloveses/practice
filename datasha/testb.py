import fileinput
import os
import sys


def getdata(filename):
    if not os.path.exists(filename):
        print('File is not exists!')
        return
    i = -1
    rets = [0,] * 40
    for line in fileinput.input(filename):
        i += 1
        if i % 41==0:
            continue
        else:
            data = float(line.split(' ')[-1])
            rets[i%41 - 1] += data
    n = i // 41 + 1
    rets = [r/n for r in rets]
    print(rets)
    return rets

def tofile(data,filename):
    with open(filename,'wt') as f:
        for d in data:
            f.write(str(d))
            f.write('\n')
            
if __name__ == '__main__':
    inputf = 'abc.txt'
    outputf = 'result.txt'
#     print(len(sys.argv),sys.argv)
    if len(sys.argv) >= 2:
        inputf = sys.argv[1]
    if len(sys.argv) >= 3:
        outputf = sys.argv[2]
        
#     print(inputf,outputf)
    data = getdata(inputf)
    tofile(data,outputf)
