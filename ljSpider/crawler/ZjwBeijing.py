import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
import json
import libs.proxyPool as proxyPool
import datetime

class ZjwBeijing(object):
    def __init__(self):
        pass

    def getUrlData(self):
        url = "http://zjw.beijing.gov.cn/bjjs/fwgl/fdcjy/fwjy/index.shtml"
        bsObj = self.getBsObj(url)
        if bsObj == False:
            return False
        # now = datetime.now()
        today=datetime.date.today() 
        oneday=datetime.timedelta(days=1) 
        yesterday=today-oneday
        signTime = yesterday.strftime(r"%Y/%m/%d")
        signText = str(signTime) + '存量房网上签约'
        dayContainer = bsObj.find(text=re.compile("\s*" + signText + "\s*")).parent.parent.parent
        i = 0
        dayData = {
            "dt": yesterday.strftime(r"%Y-%m-%d")
        }
        for tr in dayContainer.find_all("tr"):
            # print(tr)
            i += 1
            if (i == 1):
                continue
            elif (i == 2):
                td = tr.find('td').find_next_sibling()
                tdContent = re.findall(r"\s*(.+)\s*", str(td.string))
                dayData['net_number'] = tdContent[0]
            elif (i == 3):
                td = tr.find('td').find_next_sibling()
                tdContent = re.findall(r"\s*(.+)\s*", str(td.string))
                dayData['net_area'] = tdContent[0]
            elif (i == 4):
                td = tr.find('td').find_next_sibling()
                tdContent = re.findall(r"\s*(.+)\s*", str(td.string))
                dayData['residence_number'] = tdContent[0]
            elif (i == 5):
                td = tr.find('td').find_next_sibling()
                tdContent = re.findall(r"\s*(.+)\s*", str(td.string))
                dayData['residence_area'] = tdContent[0]
        return dayData

    def runRequest(self, url):
        # 保证一定可以成功 进行50次proxy获取
        proxyIndex = 0
        while proxyIndex < 50:
            retry_count = 5
            proxy = proxyPool.get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    proxies = {
                        "http": "http://{}".format(proxy)
                    }
                    # print(proxies)
                    # resp = requests.get('http://www.zsfucai.cn/admin/privilege.php?act=login&operator=rd',
                    #     proxies=proxies,
                    #     timeout=10
                    #     )
                    resp = requests.get(
                        url,
                        params={
                        },
                        headers={
                                'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                'Accept':'text/html;q=0.9,*/*;q=0.8',
                                'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            },
                        proxies=proxies,
                        timeout=30
                    )
                    return resp
                except Exception:
                    retry_count -= 1
            proxyIndex += 1
            # print(proxyIndex)
            # 出错5次, 删除代理池中代理
            proxyPool.delete_proxy(proxy)
        return False



    def getBsObj(self, url):
        # 获取sku的网页信息
        # resp = self.runRequest(url)
        resp = requests.get(
            url,
            params={
            },
            headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept':'text/html;q=0.9,*/*;q=0.8',
                    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                },
            timeout=30
        )
        if (resp == False):
            return False
        print('[resp] [code %s]' % (resp.status_code))
        resp.encoding=('utf8')
        r = resp.text
        return BeautifulSoup(r, 'lxml')

