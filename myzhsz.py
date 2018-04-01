import re
import time
import pyDes
import binascii
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "myDynamicElement"))
# element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id(“someId”))

SLEEP_TIME = 1

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

def decrypt_lst(k,datalst):
    ret = []
    for data in datalst:
        ret.append(mydecrypt(k,data))
    return ret

def init_web(username,myppp):
    """
    登录并进入页面
    """
    br = webdriver.Firefox()
    br.get("http://www.ahedu.cn/EduResource/index.php?app=resource&mod=Index&act=index")
    time.sleep(SLEEP_TIME)
    br.find_element_by_id('username').send_keys(username)
    br.find_element_by_id('password').send_keys(myppp)
    br.find_element_by_id('sso_login').click()
    time.sleep(SLEEP_TIME+4)
    # br.find_element_by_css_selector('.ah_gr span').click()
    delay_find(br.find_element_by_css_selector,'.ah_gr span',meth_name='click')
    time.sleep(SLEEP_TIME+4)
    # br.find_element_by_css_selector('a.entrance-szpj-ma').click()
    delay_find(br.find_element_by_css_selector,'a.entrance-szpj-ma',meth_name='click')
    time.sleep(SLEEP_TIME)
    crrw = br.current_window_handle
    wds = br.window_handles
    for wd in wds:
        if wd != crrw:
            br.switch_to_window(wd)
    time.sleep(SLEEP_TIME+2)
    # br.find_element_by_link_text("数据录入").click()
    delay_find(br.find_element_by_link_text,"数据录入",meth_name='click')
    time.sleep(SLEEP_TIME)
    return br

def delay_find(find_meth,context,meth_name=None,attr_name=None):
    # 自动延时操作元素
    time.sleep(SLEEP_TIME+4)
    for i in range(5):
        try:
            element = find_meth(context)
            if meth_name:
                getattr(element,meth_name)()
                return
            if attr_name:
                return getattr(element,attr_name)
        except:
            print("Wait a time!",context)
            time.sleep((SLEEP_TIME+4)*(i+1))

def delay_pagedown(br):
    # 自动延时操作下一页元素
    time.sleep(SLEEP_TIME+4)
    for i in range(5):
        try:
            elements = br.find_elements_by_tag_name('span')
            for element in elements:
                if element.text == '下一页':
                    element.click()
                    return
        except:
            print("Wait a time,delay_pagedown")
            time.sleep((SLEEP_TIME+4)*(i+1))


def delay_get_elements(find_meth,context):
    # 自动延时获取元素
    time.sleep(SLEEP_TIME+4)
    for i in range(5):
        try:
            elements = find_meth(context)
            return elements
        except:
            print("Wait a time!",context)
            time.sleep((SLEEP_TIME+4)*(i+1))


def get_sch_total(br,sch):
    delay_find(br.find_element_by_css_selector,'input.first_select',meth_name='click')
    delay_find(br.find_element_by_link_text,sch,meth_name='click')
    delay_find(br.find_element_by_id,'search-a',meth_name='click')
    txt = delay_find(br.find_element_by_id,'total_num_span',attr_name='text')
    # time.sleep(SLEEP_TIME+2)
    # br.find_element_by_css_selector('input.first_select').click()
    # time.sleep(SLEEP_TIME+4)
    # br.find_element_by_link_text(sch).click()
    # time.sleep(SLEEP_TIME)
    # br.find_element_by_id('search-a').click()
    # time.sleep(SLEEP_TIME)
    # # 获取 共xxxx条记录
    # txt = br.find_element_by_id('total_num_span').text
    return get_num(txt) if txt else 0

def get_apage_names(allelements):
    # 获取当前页激活人姓名
        names = []
        if allelements:
            for element in allelements[::4]:
                try:
                    names.append(element.text)
                except:
                    print("Have a error!")
        return names

def get_sch_names(br,sch):
    # 获取某校激活人姓名
    delay_find(br.find_element_by_css_selector,'input.first_select',meth_name='click')
    delay_find(br.find_element_by_link_text,sch,meth_name='click')
    delay_find(br.find_element_by_id,'search-a',meth_name='click')
    txt = delay_find(br.find_element_by_id,'total_num_span',attr_name='text')
    totals = int(get_num(txt)) if txt else 0
    if totals:
        pages = math.ceil(totals / 10)
        # allelements = br.find_elements_by_css_selector('.ell-txt118')
        allelements = delay_get_elements(br.find_elements_by_css_selector,'.ell-txt118')
        names = get_apage_names(allelements)
        if pages > 1:
            for page in range(pages-1):
                print(page)
                delay_pagedown(br)
                # delay_find(br.find_element_by_css_selector,
                #     'li.fl:nth-child(9) > span:nth-child(1)',meth_name='click')
                # br.find_element_by_css_selector('li.fl:nth-child(9) > span:nth-child(1)').click()
                allelements = delay_get_elements(br.find_elements_by_css_selector,'.ell-txt118')
                names.extend(get_apage_names(allelements))
        for name in names:
            print(name)
        with open('names.txt','w',encoding='utf-8') as f:
            f.write("\n".join(names))

def get_num(txt):
    res = re.search(r'\d+',txt)
    return res.group()

def get_schs(br,schs):
    # 获取各校激活人数
    ret = []
    for sch in schs:
        num = get_sch_total(br,sch)
        print(sch,'\t\t',num)
        ret.append((sch,num))
    # for r in ret:
    #     print(r[0],r[1])
    return ret
# allstuds = br.find_elements_by_css_selector('.ell-txt118')


# //下一页
# br.find_element_by_css_selector('li.fl:nth-child(9) > span:nth-child(1)').cl
# ick()

def mycount():
    schs = ['d4e6cfa426cf96d8ff50251bbfa2cfbbaaad89ab4e0afcaa66a5b023abc2acd8f9d959394f06128f', 
            'd4e6cfa426cf96d83f62bc4bed7737324210918816bd4b0aa6ba7a11cae2b43e', 
            'd4e6cfa426cf96d83f62bc4bed7737329e58919974d6f95aa6ba7a11cae2b43e', 
            'd4e6cfa426cf96d8ff50251bbfa2cfbb194c10bb846e0a0166a5b023abc2acd8f9d959394f06128f', 
            '622bdbc151bed972db362fa2b8907b9a', 
            '6cfbe1743942a94e8c64b2b77d3924dfe3feb3c22e7e74b966f334c5cd194ab5', 
            '6cfbe1743942a94ed32eccf13545644de3feb3c22e7e74b966f334c5cd194ab5', 
            'd636a03e697bcc89dccfb701c8cd02ace3feb3c22e7e74b966f334c5cd194ab5', 
            '747c5ebe9eb8024c41498ec1eb5a1979edda3dc300a3085f', 
            '622bdbc151bed972bcea7c7a795cf3e5e3feb3c22e7e74b966f334c5cd194ab5', 
            'e0d658a2471d081097363b96dcac91dae3feb3c22e7e74b966f334c5cd194ab5', 
            'ec81b4fd4fa0ff0dbeef92fed5024a724c7f479578cff523', 
            '3d54c167b5d6854d01bec7a457e952f9e3feb3c22e7e74b966f334c5cd194ab5', 
            '3d54c167b5d6854deb55434e7fc1e51fe3feb3c22e7e74b966f334c5cd194ab5', 
            '0e10357d3e73c10aa7a7aa316f5b400e4c7f479578cff523', 
            '64e0bb6898afb166eb7360adb8643562e3feb3c22e7e74b966f334c5cd194ab5', 
            'a66ec0d4b4b6a203b9d2b527af99727ae3feb3c22e7e74b966f334c5cd194ab5', 
            '5008f8c85a86786f1f98767954880334f19b4171c12c98b266f334c5cd194ab5', 
            '14ea9ff99df3f3ae73ae43412a7584e9e3feb3c22e7e74b966f334c5cd194ab5', 
            '221e0adcffdf3a9adc8a3bf3f362fe0fe3feb3c22e7e74b966f334c5cd194ab5', 
            'd8434d4a3cc22f4fdd1d925031d99fdd4c7f479578cff523', 
            'b0112481c852f73b3bc861f468cdb770edda3dc300a3085f', 
            '53ca6413ab2610a1fc88a8ac89db15b04c7f479578cff523', 
            '41781469e3f31b726c18c883e32e77784c7f479578cff523', 
            '6c223694f3a4640b2f795d4de538fcf2edda3dc300a3085f']
    username = '773e321908018520'
    myppp = '5bae14201316d0cb27df9224e3f0f22d'
    secret = input('Please input password:')
    br = init_web(mydecrypt(secret,username),mydecrypt(secret,myppp))
    schs = decrypt_lst(secret,schs)
    get_schs(br,schs)
    # br.quit()

def get_name_lst():
    username = '773e321908018520'
    myppp = '5bae14201316d0cb27df9224e3f0f22d'
    secret = input('Please input password:')
    br = init_web(mydecrypt(secret,username),mydecrypt(secret,myppp))
    sch = input("Please input schname:")
    get_sch_names(br,sch)
    # br.quit()

if __name__ == '__main__':
    # mycount()
    get_name_lst()