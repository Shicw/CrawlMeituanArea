import requests
import json
from bs4 import BeautifulSoup
import os

#从美团API中获取城市url
def get_url_from_api(city_name):
    url = "https://apimobile.meituan.com/group/v1/area/search/"
    res = requests.get(url + city_name).text
    res = json.loads(res)
    if len(res['data']) == 0 :
        return 0
    else:
        acronym = res['data'][0]['cityAcronym']
        if len(acronym) == 0:
            return 0
        else:
           return ('https://' + acronym + '.meituan.com/meishi/')

#从本地json文件从获取城市url
def get_url_from_json(city_name):
    if os.path.exists('city.json') == True:
        file = open('city.json', 'r').read()
        city_json = json.loads(file)
        if city_json.__contains__(city_name):
            return city_json[city_name]
        else:
            return 0
    else:
        return 0
#获取商圈数据
def get_area_data(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    if len(html) == 0 :
        print ('未找到该城市的商圈信息')
        return 0
    else:
        html = BeautifulSoup(html, "html.parser").find_all('script')
        city_json = '' #存放包含商圈信息的json字符串
        for i in html:
            i = str(i.string)
            if i.find('window._appState') != -1:
                city_json = i
                break
        city_json = city_json[19:-1]#去除首位不需要的字符,仅保留json数据
        city_json = json.loads(city_json)
        city_json = city_json['filters']['areas']
        return city_json
#处理数据 json=>txt
def process_data(data):
    res = ""
    for key,i in enumerate(data):
        res += i['name'] + "\r\n"
        for j in data[key]['subAreas']:
            if j['name'] != '全部':
                res += "   " + j['name'] + "\r\n"
    return res

def init():
    city_name = input("请输入城市名：")
    url = get_url_from_json(city_name)
    if url == 0 :
        url = get_url_from_api(city_name)
        if url == 0 :
            print ("输入的城市名有误,请重新输入")
            init()
    data = get_area_data(url)
    if data != 0 :
        data = process_data(data)
        print (data)
        file = open('city_area_' + city_name +'.txt', 'w')
        file.write(data)
        file.close()


if __name__ == '__main__':
    init()