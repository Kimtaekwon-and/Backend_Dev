from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib

import json
from datetime import datetime,timedelta
from numpy import string_
import pandas as pd

import requests # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다
import xmltodict


# 어제 날짜와 오늘날짜를 구하기 위해서  datetime과 timedelta를 사용

class CovidApiConnect:

    #start,enddate 구하기
    yester = (datetime.today() - timedelta(1)).strftime("%Y%m%d")
    now_today = datetime.today().strftime("%Y%m%d")
    #api key
    my_api_key = 'nbn40a7ueWp1yZGB6%2Bt%2F%2F7tpEL54yRnYZeLOsqhsj7WxVf4rsv9ROEhvN%2BtRSzsD5aWChJKEE6zkx1AcHuJBWQ%3D%3D'
    # 서비스 url 주소
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
    #Api요청정보
    queryParams = '?' + \
    'ServiceKey=' + '{}'.format(my_api_key) + \
    '&pageNo='+ '1' + \
    '&numOfRows='+ '10' + \
    '&startCreateDt={}&endCreateDt={}'.format(yester,now_today)
    #쿼리 요청
    requestApiInform = requests.get(url + queryParams)
    requestApiInform = requestApiInform.content 
    #xml->json인코딩,영어정보 ->한글 변경
    jsonString = json.dumps(xmltodict.parse(requestApiInform), indent = 4)
    jsonString = jsonString.replace('resultCode', '결과코드').replace('resultMsg', '결과메세지').replace('numOfRows', '한 페이지 결과 수').replace('pageNo', '페이지 수').replace('totalCount', '전체 결과 수').replace('seq', '게시글번호(감염현황 고유값)').replace('stateDt', '기준일').replace('stateTime', '기준시간').replace('decideCnt', '확진자 수').replace('clearCnt', '격리해제 수').replace('examCnt', '검사진행 수').replace('deathCnt', '사망자 수').replace('careCnt', '치료중 환자 수').replace('resutlNegCnt', '결과 음성 수').replace('accExamCnt', '누적 검사 수').replace('accExamCompCnt', '누적 검사 완료 수').replace('accDefRate', '누적 환진률').replace('createDt', '등록일시분초').replace('updateDt', '수정일시분초')
    #json 디코딩
    js = json.loads(jsonString)
    js = js['response']['body']['items']['item']
    pdata = pd.DataFrame(js)
    #DataFrame row추가
    pdata['전일대비증감수'] = str(int(pdata.loc[0][7]) - int(pdata.loc[1][7]))
    #필요정보만 삽
    pdata = pdata[['기준일','기준시간','확진자 수','격리해제 수','검사진행 수','사망자 수','전일대비증감수']]
