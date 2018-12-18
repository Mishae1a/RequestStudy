from aip import AipOcr
import requests
import config.ocr as ocrConfig

class BaiduOcr(object):
    def __init__(self):
        APP_ID = ocrConfig.config['APP_ID']
        API_KEY = ocrConfig.config['API_KEY']
        SECRET_KEY = ocrConfig.config['SECRET_KEY']
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def getData(self, url):
        # 获取图片信息
        image = requests.get(url)
        result = self.client.basicAccurate(image.content)
        return result['words_result'][0]['words']


