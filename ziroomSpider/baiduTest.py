import spiderUnit.BaiduOcr as BaiduOcr

ocr = BaiduOcr.BaiduOcr()
# result = ocr.getData("http://static8.ziroom.com/phoenix/pc/images/price/9f3ec377d708b42e848160072ba83b6as.png")
result = ocr.getData("http://static8.ziroom.com/phoenix/pc/images/price/new-list/2e120609b7f35a9ebec0c72c4b7502b2.png")
print(result)
