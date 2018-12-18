import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
import json
import spiderUnit.BaiduOcr as BaiduOcr

class ZiroomList(object):
    def __init__(self, keyword):
        self.keyword = keyword

    def getDataList(self):
        bsObj = self.getBsObj()
        if bsObj == False:
            self.dataList = False
            return self.dataList
        container = bsObj.find(class_="t_newlistbox")
        if container == None:
            self.dataList = []
            return self.dataList
        # 判断数据html中是否有未找到提示
        nomsgContainer = container.find(class_="nomsg")
        if nomsgContainer != None:
            self.dataList = []
            return self.dataList
        # 获取数据进行处理
        houseContainer = container.find(id="houseList")
        if houseContainer == None:
            self.dataList = []
            return self.dataList
        houseList = houseContainer.find_all('li')
        result = []
        for item in houseList:
            # 获取单个房子数据
            # zid
            houseHref = item.find('a').attrs['href']
            zid = re.findall(r"vr/(.+).html", houseHref)
            zid = int(zid[0])
            # house_name
            house_name = item.find('h3').find('a').string
            # detail  先不截取了
            detailObj = item.find(class_ = "detail")
            detail = detailObj.prettify()
            # area
            try:
                area = re.findall(r"(.+)㎡", detailObj.prettify())
                area = area[0].strip(' \t\n\r')
            except BaseException as e:
                area = 0
            # floor
            try:
                floor = re.findall(r"(.+)层", detailObj.prettify())
                floor = floor[0].strip(' \t\n\r')
            except BaseException as e:
                floor = 0
            
            # tags
            tagsObj = item.find(class_ = "room_tags").find_all('span')
            tags = ""
            for tagItem in tagsObj:
                tags += tagItem.string + ','
            
            # unit
            try:
                unit = item.find(class_ = "priceDetail").find(class_ = "gray-6").string.strip(' \t\n\r')
            except BaseException as e:
                unit = ''
            
            # price
            price = 0
            house = {
                'zid' : int(zid),
                'house_name' : house_name,
                'detail' : detail,
                'area' : area,
                'floor' : floor,
                'tags' : tags,
                'unit' : unit,
                'price' : price,
            }
            result.append(house)
        # 处理价格信息 先获取本页面的价格信息
        if result == []:
            self.dataList = []
            return []
        # var ROOM_PRICE = {"image":""};
        try:
            priceInfo = re.findall(r"var ROOM_PRICE = (.+);", bsObj.prettify())
            priceInfo = json.loads(priceInfo[0])
            priceList = self.getZiroomPriceList(priceInfo)
            i = 0
            for house in result:
                house['price'] = priceList[i]
                i += 1
        except BaseException as e:
            # 啥都不做
            pass

        self.dataList = result
        return result

    # 获取自如的价格列表
    def getZiroomPriceList(self, priceInfo):
        if (priceInfo == None or priceInfo == False or priceInfo == {} or priceInfo['image'] == ''):
            return []
        ocr = BaiduOcr.BaiduOcr()
        pictureInfo = ocr.getData('http:' + priceInfo['image'])
        priceList = []
        for offset in priceInfo['offset']:
            itemPrice = ''
            for n in offset:
                itemPrice += pictureInfo[n]
            priceList.append(itemPrice)
        return priceList
    
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

