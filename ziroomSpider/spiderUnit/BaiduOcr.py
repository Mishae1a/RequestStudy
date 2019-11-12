from aip import AipOcr
import requests
import config.ocr as ocrConfig

class BaiduOcr(object):
    def __init__(self):
        APP_ID = ocrConfig.config['APP_ID']
        API_KEY = ocrConfig.config['API_KEY']
        SECRET_KEY = ocrConfig.config['SECRET_KEY']
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    
    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        # image = get_file_content('example.jpg')

    def getData(self, url):
        # 获取图片信息
        image = requests.get(url)
        with open('123.png', "wb") as code:
            code.write(image.content)
        image = self.get_file_content('123.png')
        # result = self.client.basicAccurate(image.content)
        result = self.client.custom(image, 'f89f26bdb9a26b18447a025a0e9911a3')
        # result = self.client.webImageUrl(url)
        print(result)
        # return result['words_result'][0]['words']


