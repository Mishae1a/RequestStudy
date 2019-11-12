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
        container = bsObj.find(class_="Z_list-box")
        if container == None:
            self.dataList = []
            return self.dataList
        # # 判断数据html中是否有未找到提示
        # nomsgContainer = container.find(class_="nomsg")
        # if nomsgContainer != None:
        #     self.dataList = []
        #     return self.dataList
        # # 获取数据进行处理
        # houseContainer = container.find(id="houseList")
        # if houseContainer == None:
        #     self.dataList = []
        #     return self.dataList
        houseContainer = container
        houseList = houseContainer.find_all(class_="item")
        amountResult = {}
        result = []
        for item in houseList:
            # 获取单个房子数据
            # zid
            houseHref = item.find('a').attrs['href']
            zid = re.findall(r"x/(.+).html", houseHref)
            zid = int(zid[0])
            # house_name
            house_name = item.find('h5').find('a').string
            # detail  先不截取了
            detailObj = item.find(class_ = "desc")
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
            try:
                tagsObj = item.find(class_ = "tag").find_all('span')
                tags = ""
                for tagItem in tagsObj:
                    tags += tagItem.string + ','
            except BaseException as e:
                tags = ""
            
            # unit
            try:
                unit = item.find(class_ = "unit").string
            except BaseException as e:
                unit = ''

            # 金额处理 每个字母21.4px
            # 取金额图片
            url = re.findall(r"url\(\/\/(.+)\)", item.prettify())
            url = url[0]
            priceList = []
            if url in amountResult:
                priceList = amountResult[url]
            else:
                # try:
                priceList = self.getZiroomPriceList(url)
                amountResult[url] = priceList
                # except BaseException as e:
                #     # 啥都不做
                #     pass
                # amountList = 
            
            print(amountResult)
            
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
            # print(house)
            result.append(house)
        

        self.dataList = result
        return result

    # 获取自如的价格列表
    def getZiroomPriceList(self, priceInfo):
        # if (priceInfo == None or priceInfo == False or priceInfo == {} or priceInfo['image'] == ''):
        #     return []
        ocr = BaiduOcr.BaiduOcr()
        print('http://' + priceInfo)
        pictureInfo = ocr.getData('http://' + priceInfo)
        print(pictureInfo)
        # priceList = []
        # for offset in priceInfo['offset']:
        #     itemPrice = ''
        #     for n in offset:
        #         itemPrice += pictureInfo[n]
        #     priceList.append(itemPrice)
        return pictureInfo
    
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
        # print(r)
        # exit()
        return BeautifulSoup(r, 'lxml')

