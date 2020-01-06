import crawler.LianjiaList as LianjiaList
import config.pageConf as pageConf
import mysql.connector
import config.mysql as mysqlConfig
import time
import redis

def run(city):
    # 爬取该城市列表 返回城市列表一级数据
    url = "https://" + city + ".lianjia.com/chengjiao"
    urlList = getSecondUrlList(city, url)
    r = redis.Redis(host='127.0.0.1', port=6379, password='ectouch')
    lianjiaObj = LianjiaList.LianjiaList()
    for secondUrl in urlList:
        realSecondUrl = "https://" + city + ".lianjia.com" + secondUrl
        total = lianjiaObj.getUrlTotal(realSecondUrl)
        # 先取总数量 如果总数量超过了3000条 则分片重新请求
        if total == False:
            print(realSecondUrl + ' 请求失败！')
        if total > 3000:
            for area in pageConf.areaList:
                realPage = realSecondUrl + '' +  area
                # 这里应该调用分配逻辑
                r.rpush('spider:ljList', str(realPage))
        else:
            r.rpush('spider:ljList', str(realSecondUrl))
    print(r.llen('spider:ljList'))


def getSecondUrlList(city, url):
    lianjiaObj = LianjiaList.LianjiaList()
    firstUrlList = lianjiaObj.getFirstLevelUrlList(url)
    secondUrlList = []
    for firstUrl in firstUrlList:
        furl = "https://" + city + ".lianjia.com" + firstUrl
        secondUrl = lianjiaObj.getSecondLevelUrlList(furl)
        if secondUrl == False:
            secondUrlList.append(firstUrl)
        else:
            secondUrlList = secondUrlList + secondUrl
    return secondUrlList
