strs = ['a','b','c','d']
strs.reverse()
n = len(strs)
for i in range(n):
    for j in range(n-i-1):
        print(' ',end=' ')
    for k in range(i+1):
        print(strs[k],end=' ')
    for h in range(i-1,-1,-1):
        print(strs[h],end=' ')
    print()
for i in range(n-1):
    for j in range(i+1):
        print(' ',end=' ')
    for k in range(n-i-1):
        print(strs[k],end=' ')
    for h in range(n-3-i,-1,-1):
        print(strs[h],end=' ')
    print()
