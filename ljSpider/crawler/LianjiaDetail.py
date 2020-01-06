import requests
from bs4 import BeautifulSoup
import lxml
import re
import time
import json
import libs.proxyPool as proxyPool

class LianjiaDetail(object):
    def __init__(self):
        pass

    def getUrlData(self, lj_id, url):
        # url = "https://bj.lianjia.com/chengjiao/" + lj_id + ".html"
        bsObj = self.getBsObj(url)
        if bsObj == False:
            return False

        infoContainer = bsObj.find(id="introduction")
        # 取所有基本属性
        allinfo = {}
        baseInfo = infoContainer.find(class_="base").find('ul').find_all('li')
        for infoItem in baseInfo:
            try:
                infoKey = str(infoItem.find("span").string)
                infoValue = re.findall(r"</span>\n\s*(.+)\n</li>", str(infoItem.prettify()))
                infoValue = infoValue[0]
                allinfo[infoKey] = infoValue
            except BaseException as e:
                pass
        # 取所有交易属性
        tradeInfo = infoContainer.find(class_="transaction").find('ul').find_all('li')
        for infoItem in tradeInfo:
            try:
                infoKey = str(infoItem.find("span").string)
                infoValue = re.findall(r"</span>\n\s*(.+)\n</li>", str(infoItem.prettify()))
                infoValue = infoValue[0]
                allinfo[infoKey] = infoValue
            except BaseException as e:
                pass

        if '所在楼层' in allinfo:
            floor = allinfo['所在楼层']
        else: 
            floor = ''
        if '户型结构' in allinfo:
            house_type = allinfo['户型结构']
        else:
            house_type = ''
        if '建筑面积' in allinfo:
            area = allinfo['建筑面积']
        else:
            area = ''
        if '套内面积' in allinfo:
            real_araa = allinfo['套内面积']
        else:
            real_araa = ''
        if '挂牌时间' in allinfo:
            guapai_time = allinfo['挂牌时间']
        else:
            guapai_time = ''
        if '交易权属' in allinfo:
            ownership = allinfo['交易权属']
        else:
            ownership = ''
        if '房屋用途' in allinfo:
            house_usage = allinfo['房屋用途']
        else:
            house_usage = ''
        if '房屋年限' in allinfo:
            house_limit = allinfo['房屋年限']
        else:
            house_limit = ''
        attr_detail = str(allinfo)

        # 取交易记录
        try:
            tradeListOrigin = bsObj.find(class_='chengjiao_record').find("ul", class_='record_list').find_all('li')
            tradeList = []
            for tradeOrigin in tradeListOrigin:
                price = tradeOrigin.find(class_='record_price').string
                detail = tradeOrigin.find(class_='record_detail').string
                tradeList.append({
                    'price': str(price),
                    'detail': str(detail),
                })
            trade_list = str(tradeList)
        except BaseException as e:
            trade_list = ''

        # 取小区信息
        originHtml = bsObj.prettify()
        try:
            plot = re.findall(r"resblockName:'(.+)'", originHtml)
            plot = plot[0]
        except BaseException as e:
            plot = ''
        try:
            plot_id = re.findall(r"resblockId:'(.+)'", originHtml)
            plot_id = plot_id[0]
        except BaseException as e:
            plot_id = ''
        try:
            location = re.findall(r"resblockPosition:'(.+)'", originHtml)
            location = location[0]
        except BaseException as e:
            location = ''

        houseDetail = {
            'lj_id' : lj_id,
            'floor' : floor,
            'house_type' : house_type,
            'area' : area,
            'real_araa' : real_araa,
            'guapai_time' : guapai_time,
            'ownership' : ownership,
            'house_usage' : house_usage,
            'house_limit' : house_limit,
            'attr_detail' : attr_detail,
            'trade_list' : trade_list,
            'plot' : plot,
            'plot_id' : plot_id,
            'location' : location,
        }
        return houseDetail

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

