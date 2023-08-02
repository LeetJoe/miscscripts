import requests

from config import api_baidu

def geocodeB(address):
    """
    @ address: 名称字符串
    @ 返回值：经度，纬度
    """
    base_url = "http://api.map.baidu.com/geocoder?address={address}&output=json&key={apikey}".format(address=address, apikey=api_baidu['map_key'])

    response = requests.get(base_url)
    answer = response.json()
    latitude = answer['result']['location']['lng']
    longitude = answer['result']['location']['lat']

    return latitude, longitude

print(geocodeB('九龙江口'))  # (101.513416, 29.006432)

