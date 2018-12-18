import requests
from bs4 import BeautifulSoup
import lxml
import re
import time

class ziroomList(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def getDataList(self):
        bsObj = self.getBsObj()
        if bsObj == False:
            self.dataList = False
            return self.dataList
        rawList = bsObj.find_all(class_="cfix")
        if rawList == [] or rawList == None:
            self.dataList = []
            return self.dataList

        return self.dataList
    
    def getBsObj(self):
        # 获取sku的网页信息
        resp = requests.get(
            'http://www.ziroom.com/z/nl/z2-o1.html',
            params={
                'qwd': self.keyword,
            },
            headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept':'text/html;q=0.9,*/*;q=0.8',
                    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                },
            # proxies={
            #     'http' : '116.255.169.214:16819',
            # }
        )
        print('[resp] [code %s]' % (resp.status_code))
        exit()
        if resp.status_code == 200:
            r = resp.json()
            self.hasMore = r['hasMore']
            return BeautifulSoup(r['html'], 'lxml')
        else:
            # 触发重试机制
            if self.retry > 3:
                self.hasMore = False
                return False
            else:
                self.retry += 1
                time.sleep(0.1)
                return self.getBsObj()

