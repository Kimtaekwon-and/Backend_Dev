
from six import u
from RegionCovidApi import RegionCovidApi
from KoreaCovidApi import CovidApiConnect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials


Koreadata = CovidApiConnect.pdata
Koreadata.sample()
defaultapp = firebase_admin.initialize_app()

regionData = RegionCovidApi.pdata
regionData.sample()

credFirebase = credentials.Certificate("/Users/maegbug/Downloads/PrivateCovid.json")
firebase_admin.initialize_app(credFirebase,name = 'dbInput')
coAvoidDb = firestore.client()


def inputKoreaData():

    doc_ref = coAvoidDb.collection(u'국내확진데이터').document(u(Koreadata.iloc[0].iloc[0]))
    doc_ref.set({

        u'기준일': u(Koreadata.iloc[0].iloc[0]),
        u'기준시간': u(Koreadata.iloc[0].iloc[1]),
        u'확진자수': u(Koreadata.iloc[0].iloc[2]),
        u'격리해제 수' : u(Koreadata.iloc[0].iloc[3]) ,
        u'검사진행 수' : u(Koreadata.iloc[0].iloc[4]),
        u'사망자 수' : u(Koreadata.iloc[0].iloc[5]),
        u'전일대비증감수' : u(Koreadata.iloc[0].iloc[6])

    })

def inputRegionData():
    
    for i in range(1,37):
       
        doc_ref = coAvoidDb.collection(u'지역확진데이터').document(u(regionData.iloc[i].iloc[1])).collection(u'날짜별').document(u(regionData.iloc[i].iloc[0]))
        doc_ref.set({

            u'등록일시분초': u(regionData.iloc[i].iloc[0]),
            u'시도명': u(regionData.iloc[i].iloc[1]),
            u'전일대비증감수' : u(regionData.iloc[i].iloc[2]),
            u'10만명당발생률' : u(regionData.iloc[i].iloc[3]) ,
            u'기준일시' : u(regionData.iloc[i].iloc[4]),
            u'확진자수' : u(regionData.iloc[i].iloc[5]),
            u'지역발생수' : u(regionData.iloc[i].iloc[6])
        })


inputKoreaData()
inputRegionData()




