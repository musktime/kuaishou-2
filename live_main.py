# coding=gbk

import redis
from hashlib import md5
from selenium import webdriver
import time
import pymongo
from lxml import etree
import pymongo

# ���⽨��
client = pymongo.MongoClient('localhost', port=27017)  # ����
db = client['kuaishou']  # ������
fs_kuaishou = db['a_min_zi']  # ������

# redis
r = redis.Redis(host='localhost', port=6379, db=0)
md = md5()



from selenium.webdriver import ActionChains
# 1.������������� - �Ѿ����������
driver = webdriver.Chrome()
driver.maximize_window()
# 2.����: http://www.baidu.com/
driver.get('https://live.kuaishou.com/live')

# �����¼�
# driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/header/div/div[2]/div/div[2]/span[2]').click()
time.sleep(3)
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/header/div/div[2]/div/div[2]/span[2]').click()

time.sleep(25)
# element = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/header/div/div[2]/span[1]')
# ActionChains(driver).move_to_element(element).perform()
# driver.find_element_by_link_text('�߼�����').click()



# ������ע
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/header/div/div[2]/span[1]').click()
time.sleep(13)
# ����ֱ��
# ��ʱ����
#driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]/div/ul/li/div/div[2]/p[1]/a[1]').click()
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]/div/ul/li/div/div[2]/p[1]/a[1]').click()
time.sleep(10)
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/p[1]/a').click()
# driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/p[1]/a').click()
time.sleep(10)

# ��ȡ����

# html = etree.HTML(driver.page_source)

list_name = []
list_text = []
t = 0
while True:
    # print("************����ѭ����*********")

    html = etree.HTML(driver.page_source)
    li_list = html.xpath('//li[@class="chat-info"]')
    # print(li_list)
    # print(len(li_list))
    # time.sleep(1)
    s = len(li_list)

    for li in li_list[t:s]:
        user_info = dict()
        # print("li>>>>",li)

        name = li.xpath('.//div/span[1]/text()')[0]
        list_name.append(name)
        user_info['nema'] = name
        # name1 = li.xpath('.//div/span[1]/text()')[0]
        # print(name,name1)

        # if not li.xpath('.//div/span[2]/text()'):
        try:
            text = li.xpath('.//div/span[2]/span/span/span/text()')[0]
            list_text.append(text)
            user_info['text'] = text
        except Exception as e:
            text = li.xpath('.//div/span[2]/text()')[0]
            list_text.append(text)
            user_info['text'] = text
        # text1 = li.xpath('.//div/span[2]/span/span/span/text()')[0]
        t += 1
        fs_kuaishou.insert(user_info)
        time.sleep(1)
        print("*******************��",t,"��ֱ����Ļ*****************************")
        print(name,text)
    if len(li_list) == 300:
        print("ѭ��������")
        break
t = 300
while True:
    # print("************����ѭ����*********")
    html = etree.HTML(driver.page_source)
    li_list = html.xpath('//li[@class="chat-info"]')
    # print(len(li_list))
    for li in li_list[-3:]:
        list_dict = []
        user_info = dict()
        # print("li>>>>",li)
        name = li.xpath('.//div/span[1]/text()')[0]
        list_name.append(name)
        user_info['nema'] = name
        # name1 = li.xpath('.//div/span[1]/text()')[0]
        # print(name,name1)

        # if not li.xpath('.//div/span[2]/text()'):
        try:
            text = li.xpath('.//div/span[2]/span/span/span/text()')[0]
            list_text.append(text)
            user_info['text'] = text

        except Exception as e:
            text = li.xpath('.//div/span[2]/text()')[0]
            list_text.append(text)
            user_info['text'] = text

        if user_info in list_dict:
            print("***********�����Ѵ���**********")
        else:
            fs_kuaishou.insert(user_info)
            t += 1
            print("*******************��", t, "��ֱ����Ļ*****************************")
            print(name, text)
            list_dict.append(user_info)
            time.sleep(1)
        # md5����
        # str1 = data['user']['nickname'] + data['user']['uid'] + data['text']
        # str1 = user_info['nema'] + user_info['text']
        # md.update(str1.encode())
        # finger = md.hexdigest()
        # print(finger)
        # print(user_info, 'md5ָ�ƣ�', finger)
        # if r.sadd('douyin:spider', finger) == 0:
        #     print("***********�����Ѵ���**********")
        # else:
        #     fs_kuaishou.insert(user_info)
        #     time.sleep(1)
        #     print("*******************��", t, "��ֱ����Ļ*****************************")
        #     print(name, text)
