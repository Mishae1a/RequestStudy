import requests
from bs4 import BeautifulSoup
import lxml
import re
import time

class ZiroomList(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def getDataList(self):
        bsObj = self.getBsObj()
        print(bsObj.find(class_="t_newlistbox"))
        return []
        if bsObj == False:
            self.dataList = False
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
        r = resp.text
        return BeautifulSoup(r, 'lxml')

