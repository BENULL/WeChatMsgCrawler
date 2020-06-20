import requests
import json
import re
import time

class WeChatCrawler():

    def __init__(self, wxList):
        self.wxList = wxList
        self.cookies = self.__getCookiesFromText()
        self.token = self.__getToken()
        self.headers = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }
        self.searchBizParam = {
            'action': 'search_biz',
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'query': '',
            'begin': '0',
            'count': '5',
        }
        self.getMsgListParam = {
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'action': 'list_ex',
            'begin': '0',
            'count': '5',
            'query': '',
            'fakeid': '',
            'type': '9'
        }

    def __getCookiesFromText(self):
        # 手动获取cookie
        with open('cookie.txt', 'r', encoding='utf-8') as f:
            cookieStr = f.read()
            # 处理cookieStr格式转化成json
            cookieStr = "{\"" + cookieStr + "\"}"
            cookieStr = cookieStr.replace("rewardsn=;", "").replace(";", "\",\"").replace("=", "\":\"").replace(
                "\":\"\"", "=\"").replace(' ', '')
            # print(cookieStr)
            cookies = json.loads(cookieStr)
            return cookies

    def __getToken(self):
        url = 'https://mp.weixin.qq.com'
        response = requests.get(url=url, cookies=self.cookies)
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        return token

    def __getWXFakeid(self, wx):
        searchUrl = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        self.searchBizParam['query'] = wx
        searchResponse = requests.get(searchUrl, cookies=self.cookies, headers=self.headers, params=self.searchBizParam)
        fakeid = searchResponse.json().get('list')[0].get('fakeid')
        return fakeid

    def __getWXMsgCnt(self, fakeId):
        self.getMsgListParam['fakeid'] = fakeId
        appmsgUrl = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        appmsgResponse = requests.get(appmsgUrl, cookies=self.cookies, headers=self.headers,
                                      params=self.getMsgListParam)
        wxMsgCnt = appmsgResponse.json().get('app_msg_cnt')
        return wxMsgCnt

    def __getWXMsgList(self, fakeId):
        appmsgUrl = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        wxMsgCnt = self.__getWXMsgCnt(fakeId)
        if wxMsgCnt is not None:
            pages = int(wxMsgCnt) // 5
            begin = 0
            for _ in range(pages):
                print('====翻页====', begin)
                self.getMsgListParam['begin'] = str(begin)
                msgListResponse = requests.get(appmsgUrl, cookies=self.cookies, headers=self.headers,
                                               params=self.getMsgListParam)
                msgList = msgListResponse.json().get('app_msg_list')
                for item in msgList:
                    # todo more
                    msgLink = item.get('link')
                    print(msgLink)
                    msgTitle = item.get('title')
                    print(msgTitle)
                begin += 5
                time.sleep(3)

    def runCrawler(self):
        fakeIds = list(map(self.__getWXFakeid, self.wxList))
        list(map(self.__getWXMsgList, fakeIds))

if __name__ == '__main__':
    # example
    wxList = ['量子位', ]
    wc = WeChatCrawler(wxList)
    wc.runCrawler()
