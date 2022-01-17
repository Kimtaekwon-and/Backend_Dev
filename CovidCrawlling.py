import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

class CovidCrawlling:



    url = 'https://m.search.naver.com/p/csearch/content/nqapirender.nhn?where=nexearch&pkid=9005&key=distanceAPI'
    region_dic = dict()

    ## url 접속 - chromeDriver
    request = requests.get(url)
    if(request.status_code == 200):
        stock_data = json.loads(request.text)
        for element in stock_data["result"]["regions"]:
            
            region_dic[element['title']] = element['count']

            #print(region_dic)
    
    print(region_dic)

