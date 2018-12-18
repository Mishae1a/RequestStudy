from aip import AipOcr
import requests
import config.ocr as ocrConfig

""" 你的 APPID AK SK """
APP_ID = ocrConfig.config['APP_ID']
API_KEY = ocrConfig.config['API_KEY']
SECRET_KEY = ocrConfig.config['SECRET_KEY']
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

url = "http://static8.ziroom.com/phoenix/pc/images/price/9f3ec377d708b42e848160072ba83b6as.png"

image = requests.get(url)
result = client.basicAccurate(image.content)
print(result)