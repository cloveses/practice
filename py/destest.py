import pyDes
import binascii
import math

key = 'kdljhfijfeih9838928923efefgerertdfwere3ffedertgertaf'[:24]
data = '我胶是踌躇工云蒸霞蔚'

k = pyDes.triple_des(key,padmode=pyDes.PAD_PKCS5)
mdata = k.encrypt(data.encode())
res = binascii.hexlify(mdata).decode()
resb = binascii.unhexlify(res.encode())
cdata = k.decrypt(resb)
def get_key(k):
    times = math.ceil(24 / len(k))
    k *= times
    return k[:24]

def get_des(k):
    k = get_key(k)
    return pyDes.triple_des(k,padmode=pyDes.PAD_PKCS5)

def myencrypt(k,data):
    tri_des = get_des(k)
    secret = tri_des.encrypt(data.encode())
    return binascii.hexlify(secret).decode()

def mydecrypt(k,data):
    tri_des = get_des(k)
    secret = binascii.unhexlify(data.encode())
    return tri_des.decrypt(secret).decode()

schs = ['*****','******']
k = 'cloveses'
res = []
for sch in schs:
    res.append(myencrypt(k,sch))
print(res)
for r in res:
    print(mydecrypt(k,r))
