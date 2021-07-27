from typing import Type
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib

import json
from datetime import datetime,timedelta
import pandas as pd

import requests # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다
import xmltodict





#url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
#queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '서비스키', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('startCreateDt') : '20200410', quote_plus('endCreateDt') : '20200410' })

#request = Request(url + queryParams)
#request.get_method = lambda: 'GET'
#response_body = urlopen(request).read()
#print response_body




class RegionCovidApi:

    def __init__(self) -> None:
        pass



    startDay = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
    endDay = datetime.today().strftime("%Y%m%d")

    print(startDay,endDay)

    
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
    result = requests.get(covidPageUrl + queryParams)

    # 응답결과 파싱하기. ( 사용자가 원하는 형태로 변경)
    # 응답 key 값이 영문화 되어 식별이 어려워 openAPI 문서를 참고하여
    # replayce 를 통해 결과를 한글화 했다.
    result = result.content 
    jsonString = json.dumps(xmltodict.parse(result), indent = 4)
    jsonString = jsonString.replace('resultCode', '결과코드').replace('resultMsg', '결과메세지').replace('numOfRows', '한 페이지 결과 수').replace('pageNo', '페이지 번호').replace('totalCount', '전체 결과 수').replace('seq', '게시글번호(감염현황 고유값)').replace('createDt', '등록일시분초').replace('deathCnt', '사망자수').replace('gubun', '시도명').replace('gubunCn', '시도명(중국어)').replace('gubunEn', '시도명(영어)').replace('incDec', '전일대비증감수').replace('isolClearCnt', '격리 해제 수').replace('qurRate', '10만명당 발생률').replace('stdDay', '기준일시').replace('updateDt', '수정일시분초').replace('defCnt', '확진자수').replace('isolIngCnt', '격리중 환자수').replace('overFlowCnt', '해외유입 수').replace('localOccCnt', '지역발생수')
    #print(jsonString)
    js = json.loads(jsonString)
    js = js['response']['body']['items']['item']
    pdata = pd.DataFrame(js)
    #print(pdata)
    # 원하는 정보만 파싱한 결과
    # 누적 검사자 수와 누적 확진자수를 제공하기 때문에
    # 전일과의 차이로 일일 확진자, 검사자 수를 구했다.

    pdata = pdata[['등록일시분초','시도명','전일대비증감수','10만명당 발생률','기준일시','확진자수','지역발생수']]
    print(pdata)
    #print(pdata)

    #print(pdata)
    #print('전일 검사 확진자수 : ',int(pdata.loc[0][7]) - int(pdata.loc[1][7]))
    #print('전일 코로나 검사 수',int(pdata.loc[0][8]))

