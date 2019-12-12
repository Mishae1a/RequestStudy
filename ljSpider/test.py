import crawler.LianjiaList as LianjiaList

lianjiaObj = LianjiaList.LianjiaList()
r = lianjiaObj.getUrlData('https://bj.lianjia.com/chengjiao/tiantongyuan1/ba100ea110/')
print(r)