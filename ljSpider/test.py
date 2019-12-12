import crawler.LianjiaList as LianjiaList
import crawler.LianjiaDetail as LianjiaDetail

# lianjiaObj = LianjiaList.LianjiaList()
# r = lianjiaObj.getUrlData('https://bj.lianjia.com/chengjiao/tiantongyuan1/ba100ea110/')
# print(r)

lianjiaObj = LianjiaDetail.LianjiaDetail()
r = lianjiaObj.getUrlData('101105987964')
print(r)