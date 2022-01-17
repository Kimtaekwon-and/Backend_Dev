from typing import Type
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib

import json
from datetime import datetime,timedelta
import pandas as pd

import requests # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다
import xmltodict
import time
from array import *


class RegionCovidApi:

    def __init__(self) -> None:
        pass

    startDay = (datetime.today()-timedelta(7)).strftime("%Y%m%d")
    endDay = (datetime.today()-timedelta(0)).strftime("%Y%m%d")
    todayIncArray = []
    
    myApiKey = 'nbn40a7ueWp1yZGB6%2Bt%2F%2F7tpEL54yRnYZeLOsqhsj7WxVf4rsv9ROEhvN%2BtRSzsD5aWChJKEE6zkx1AcHuJBWQ%3D%3D'
    # 서비스 url 주소
    covidPageUrl = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
        
    # 서비스에 필요한 파라미터 모음
    queryParams = '?' + \
    'serviceKey=' + '{}'.format(myApiKey) + \
    '&pageNo='+ '1' + \
    '&numOfRows='+ '10' + \
    '&startCreateDt={}&endCreateDt={}'.format(startDay,endDay)

    #서비스url에 필요한 파라미터들을 붙여서 응답결과를 얻음.
    requestToApi = requests.get(covidPageUrl + queryParams) 
    requestToApi = requestToApi.content 
    covidDataDict = json.dumps(xmltodict.parse(requestToApi), indent = 4)
    covidDataDict = covidDataDict.replace('resultCode', '결과코드').replace('resultMsg', '결과메세지').replace('numOfRows', '한 페이지 결과 수').replace('pageNo', '페이지 번호').replace('totalCount', '전체 결과 수').replace('seq', '게시글번호(감염현황 고유값)').replace('createDt', '등록일시분초').replace('deathCnt', '사망자수').replace('gubun', '시도명').replace('gubunCn', '시도명(중국어)').replace('gubunEn', '시도명(영어)').replace('incDec', '전일대비증감수').replace('isolClearCnt', '격리 해제 수').replace('qurRate', '10만명당 발생률').replace('stdDay', '기준일시').replace('updateDt', '수정일시분초').replace('defCnt', '확진자수').replace('isolIngCnt', '격리중 환자수').replace('overFlowCnt', '해외유입 수').replace('localOccCnt', '지역발생수')
    
    covidDataJson = json.loads(covidDataDict)
    covidDataJson = covidDataJson['response']['body']['items']['item']
    covidDataDataframe = pd.DataFrame(covidDataJson)
    
    covidDataDataframe['기준일시'] =(datetime.today().replace(hour=0, minute=0)-timedelta(1)).strftime("%Y-%m-%d %H%m")
    covidDataDataframe = covidDataDataframe[covidDataDataframe['시도명'] != "검역" ]
    covidDataDataframe.loc[(covidDataDataframe['10만명당 발생률'] == '-'),'10만명당 발생률'] = 0
    covidDataDataframe = covidDataDataframe[['등록일시분초','시도명','전일대비증감수','10만명당 발생률','기준일시','확진자수','지역발생수']]

    print(covidDataDataframe)
    covidDataDataframe['등록일시분초'] = pd.to_datetime(covidDataDataframe['등록일시분초'])
    covidDataDataframe['전일대비증감수'] = pd.to_numeric(covidDataDataframe['전일대비증감수'])
    covidDataDataframe['10만명당 발생률'] = pd.to_numeric(covidDataDataframe['10만명당 발생률'])
    covidDataDataframe['기준일시'] = pd.to_datetime(covidDataDataframe['기준일시'])
    covidDataDataframe['확진자수'] = pd.to_numeric(covidDataDataframe['확진자수'])
    covidDataDataframe['지역발생수'] = pd.to_numeric(covidDataDataframe['지역발생수'])



    for i in range(len(covidDataDataframe)):

        if(covidDataDataframe.iloc[i].iloc[1] == '합계' ):
            todayIncArray.append(int(covidDataDataframe.iloc[i].iloc[2]))
    