import crawler.LianjiaList as LianjiaList
import crawler.LianjiaDetail as LianjiaDetail
import redis

# lianjiaObj = LianjiaList.LianjiaList()
# r = lianjiaObj.getUrlData('https://bj.lianjia.com/chengjiao/tiantongyuan1/ba100ea110/')
# print(r)

# lianjiaObj = LianjiaDetail.LianjiaDetail()
# r = lianjiaObj.getUrlData('101105987964')
# print(r)

r = redis.Redis(host='127.0.0.1', port=6379, password='ectouch')

r.lpush('ljDetail1', '123')
print(r.llen('ljDetail1'), r.lpop('ljDetail1'))