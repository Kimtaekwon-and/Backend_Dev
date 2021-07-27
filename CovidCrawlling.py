from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


## 다운로드한 크롬 드라이버의 경로 를 설정
driver = webdriver.Chrome(ChromeDriverManager().install())

## 구글에 코로나 확진자 라는 키워드로 검색하는 url 작성
firebaseKey =''
search_key = '코로나 확진자'
url = 'https://www.google.com/search?q={}'.format(search_key)

# 검색 키워드 url로 크롬드라이버를 이용하여 접속
driver.get(url)


#드라이버로 접속한 페이지의 소스를 읽어온다.
html = driver.page_source

#BeautifulSoup을 이용해서 html형식으로 파싱한다.
#아래의 soup을 출력하면 페이지의 모든 소스를 출력하게 된다.
soup = BeautifulSoup(html,'html.parser')

# 페이지의 소스중 ol 태그를 가진 모든 소스만 soup에 저장한다.
soup = soup.findAll("ol")

print(soup)