import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
import json
import libs.proxyPool as proxyPool

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

    def getFirstLevelUrlList(self, url):
        bsObj = self.getBsObj(url)
        if bsObj == False:
            return False
        # 取关键词总数量 获取结果
        dlList = bsObj.find(class_="position").find_all('dl')
        # 取第二个dl
        dlContainer = dlList[1]
        urlList = dlContainer.find_all('a')
        result = []
        for urlContainer in urlList:
            result.append(urlContainer['href'])
        return result

    def getSecondLevelUrlList(self, url):
        bsObj = self.getBsObj(url)
        if bsObj == False:
            return False
        # 取关键词总数量 获取结果
        dlList = bsObj.find(class_="position").find_all('dl')
        # 取第二个dl
        dlContainer = dlList[1]
        urlContainer = dlContainer.find('dd').div.find_all('div')
        # 判断dom中的url 是否有chengjiao 没有则没有公布成交房源信息
        # isExistChengjiao = re.match(r".*成交房源.*", bsObj.prettify())
        existChengjiaoUrl = urlContainer[0].find_all('a')[0]
        isExistChengjiao = re.match(r".*chengjiao.*", existChengjiaoUrl.prettify())
        if (isExistChengjiao == None):
            return {
                'code': 500,
                'data': [],
            }

        if (len(urlContainer) < 2):
            return {
                'code': 201,
                'data': []
            }
        urlContainer = urlContainer[1]
        urlList = urlContainer.find_all('a')
        result = []
        for urlContainer in urlList:
            result.append(urlContainer['href'])
        return {
            'code': 0,
            'data': result
        }

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
            try:
                total_price_origin = item.find(class_="totalPrice")
                total_price = total_price_origin.find("span", class_="number").string
                total_unit = re.findall(r"</span>\n\s*(.+)\n</div>", total_price_origin.prettify())
                total_unit = total_unit[0]
            except BaseException as e:
                total_price = ''
                total_unit = ''
            # unit_price
            # unit_unit
            try:
                unit_price_origin = item.find(class_="unitPrice")
                unit_price = unit_price_origin.find("span", class_="number").string
                unit_unit = re.findall(r"</span>\n\s*(.+)\n</div>", unit_price_origin.prettify())
                unit_unit = unit_unit[0]
            except BaseException as e:
                unit_price = ''
                unit_unit = ''

            house = {
                'lj_id' : lj_id,
                'title' : str(title),
                'trade_time' : str(trade_time),
                'total_price' : str(total_price),
                'total_unit' : total_unit,
                'unit_price' : str(unit_price),
                'unit_unit' : unit_unit,
                'status' : 1,
            }
            # print(house)
            result.append(house)
        return {
            'code': 0,
            'data': result,
        }

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
                    # html = requests.get('https://www.baidu.com', proxies=proxies)
                    # 使用代理访问
                    # print(resp)
                    # exit()
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
        resp = self.runRequest(url)
        if (resp == False):
            return False
        print('[resp] [code %s]' % (resp.status_code))
        r = resp.text
        return BeautifulSoup(r, 'lxml')

