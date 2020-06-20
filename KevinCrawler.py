import requests
import json
import re
import random
import time
from lxml import html

gzlist = ['kkenglish']
kevin = '何凯文'

url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}
# 手动获取cookie
with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie_str = f.read()
# 处理cookie_str到json_str
cookie_str = "{\""+cookie_str+"\"}"
cookie_str = cookie_str.replace("rewardsn=;", "").replace(
    ";", "\",\"").replace("=", "\":\"").replace("\":\"\"", "=\"").replace(' ', '')
print(cookie_str)
cookies = json.loads(cookie_str)
print(cookies)
response = requests.get(url=url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]
for query in gzlist:
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5',
    }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    search_response = requests.get(
        search_url, cookies=cookies, headers=header, params=query_id)
    lists = search_response.json().get('list')[0]
    fakeid = lists.get('fakeid')
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    appmsg_response = requests.get(
        appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    max_num = appmsg_response.json().get('app_msg_cnt')
    if max_num is not None:
        num = int(int(max_num) / 5)
        begin = 0
        flag = False
        while num + 1 > 0:
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            print('翻页###################', begin)
            query_fakeid_response = requests.get(
                appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            try:
                for item in fakeid_list:
                    msg_link = item.get('link')
                    # print(msg_link)
                    msg_title = item.get('title')
                    if int(item.get('update_time')) > int('1519833600'):
                        print(msg_link+'continue')
                        get_msg_response = requests.get(msg_link)
                        tree = html.fromstring(get_msg_response.text)
                        try:
                            # if tree.xpath('//*[@id="meta_content"]/em[2]/text()')[0] == kevin:
                            print(msg_title, end='\n')
                            # 处理文本
                            msg_content = tree.xpath('//*[@id="js_content"]//text()')
                            with open('sentence.txt', 'a', encoding='utf-8') as f:
                                f.write(
                                    '\n\n====================================================================\n\n'+msg_title+'\n\n')
                                for text in msg_content:
                                    f.write(text+'\n')
                                f.write(
                                    "\n\n====================================================================\n\n")
                            time.sleep(3)
                        except IndexError:
                            continue

                    else:
                        flag = True
                        break
                if flag:
                    break
                num -= 1
                begin = int(begin)
                begin += 5
                time.sleep(3)
            except TypeError:
                continue
