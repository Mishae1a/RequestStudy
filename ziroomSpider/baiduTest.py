import spiderUnit.BaiduOcr as BaiduOcr

ocr = BaiduOcr.BaiduOcr()
result = ocr.getData("http://static8.ziroom.com/phoenix/pc/images/price/9f3ec377d708b42e848160072ba83b6as.png")
print(result)