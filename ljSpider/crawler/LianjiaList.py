import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
import json

class LianjiaList(object):
    def __init__(self):
        pass

    def getUrlTotal(self, url):
        bsObj = self.getBsObj(url)
        if bsObj == False:
            return False
        # 取关键词总数量 获取结果
        totalNumber = bsObj.find(class_="resultDes").find("span").string
        return (int)(totalNumber)

    def getUrlData(self, url):
        bsObj = self.getBsObj(url)
        if bsObj == False:
            return {
                'code': 500,
                'msg': '获取请求失败'
            }
        # 取关键词总数量 获取结果
        totalNumber = bsObj.find(class_="resultDes").find("span").string
        # if (int)(totalNumber) > 5000:
        #     return {
        #         'code': 1001,
        #         'msg': '数量超过100页，请切片[' + url + ']',
        #         # 'data' : (int)(totalNumber)
        #     }
        if (int)(totalNumber) == 0:
            return {
                'code': 0,
                'data': []
            }
        container = bsObj.find(class_="listContent")
        # 取所有列表数据
        houseList = container.find_all("div", class_="info")
        if (len(houseList) == 0):
            return {
                'code': 0,
                'data': []
            }
        
        result = []
        for item in houseList:
            # lj_id
            houseHref = item.find(class_="title").find("a").attrs['href']
            lj_id = re.findall(r"chengjiao/(.+).html", houseHref)
            # lj_id 可能是一个字母开头的字符串 不要转int
            lj_id = lj_id[0]

            # title 
            title = item.find(class_="title").find("a").string
            # trade_time
            trade_time = item.find(class_="address").find(class_="dealDate").string
            # total_price
            # total_unit
            total_price_origin = item.find(class_="totalPrice")
            total_price = total_price_origin.find("span", class_="number").string
            total_unit = re.findall(r"</span>\n\s*(.+)\n</div>", total_price_origin.prettify())
            total_unit = total_unit[0]
            # unit_price
            # unit_unit
            unit_price_origin = item.find(class_="unitPrice")
            unit_price = unit_price_origin.find("span", class_="number").string
            unit_unit = re.findall(r"</span>\n\s*(.+)\n</div>", unit_price_origin.prettify())
            unit_unit = unit_unit[0]

            house = {
                'lj_id' : lj_id,
                'title' : title,
                'trade_time' : trade_time,
                'total_price' : total_price,
                'total_unit' : total_unit,
                'unit_price' : unit_price,
                'unit_unit' : unit_unit,
                'status' : 1,
            }
            # print(house)
            result.append(house)
        return {
            'code': 0,
            'data': result,
        }

    def getBsObj(self, url):
        # 获取sku的网页信息
        resp = requests.get(
            url,
            params={
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
        # print(r)
        # exit()
        return BeautifulSoup(r, 'lxml')

