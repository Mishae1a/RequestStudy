import requests
import json

params={'couponCode': 'd44c36a03a0447e79176e1884d64cfca'}
headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Accept' : 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language' : 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Referer' : 'https://huishou.jd.com/couponResult?couponCode=d44c36a03a0447e79176e1884d64cfca',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Content-Length' : '43',
    'Origin' : 'https://huishou.jd.com',
    'Connection' : 'keep-alive',
    'Cookie' : 'shshshfp=f0cea867f3a3a9ab793642dbdf46443b; shshshfpa=e9027db1-26d7-827d-fe34-edd4ab9bc09f-1542002824; shshshsID=9526860979676a515a9643cc3257ace8_22_1542004609168; shshshfpb=2cccc191b7e0241809f27f808fa60ac465be91890737d338032865f297; __jda=122270672.15420035590481669623251.1542003559.1542003559.1542003559.1; __jdb=122270672.43.15420035590481669623251|1.1542003559; __jdv=122270672|direct|-|none|-|1542003559050; user-key=51ab9ee3-01c0-4890-a1c2-482e1e0ce776; cn=0; _pst=Mishaera; unick=Mishaera; pin=Mishaera; _tp=Bca0o0Ko8qCPYn2uqPONRw%3D%3D; __jdc=122270672; pinId=kA555099pNu1ffsfn98I-w; thor=6BF45317CEBA5346F72549EF7B2DEA4D4D39D4CE19BA3D7F1D8975ED51D85BA03EA254422B39DAF5C5157165D61FBA60DEF83342C67C12AD9CE5026AB8F5FF727FB8A65FA6DE3FCB5059C4CA7B9C0BC91D8BBE302A4671714C42F578EB5C5B8C96CFAB59DE4EB3AF7E88A3B05CD5BE2C6ED6AF8867FBB6B7F2ADDE185B68D5F001BB883E17BCC4C6706864F6A0A26F90; TrackID=1vJQfsTQ2rPJj3euKtsKFNSBondFCnNJz1KbxRXuWEh6DgwhVREGR-MwW2e6fZL7p6Wb31vQnyhBAr6KlfTqLddh53O3FjYuULeing5s3qV0|||kA555099pNu1ffsfn98I-w; PCSYCityID=country_2468; 3AB9D23F7A4B3C9B=PQ4H7FGG4CYDSADDJ2IX6YZDJDJO2I24DV6KGWBOGYAOOLPNKINSPXFG5VN2DMTUH24Z7F3J2IXIE5KVP5VZRG6XAA'
}
r = requests.post(
        'https://hsc.jd.com/couponObtain/obtain',
        params=params,
        headers=headers
    )
print(r.status_code)
print(r.json())

