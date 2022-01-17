
from CovidCrawlling import CovidCrawlling
from datetime import datetime
from numpy import uint
from six import u
import os
from RegionCovidApi import RegionCovidApi
from KoreaCovidApi import CovidApiConnect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import numpy as np

db_url = 'https://co-avoid19-77829.firebaseio.com/'

#korea Data 
Koreadata = CovidApiConnect.covidDataframe
Koreadata.sample()
koreaTodayData = RegionCovidApi.todayIncArray

#Region Data - Region definitiong
regionData = RegionCovidApi.covidDataDataframe
regionData.sample()

#Region Data - Region Rank
regionRankData = CovidCrawlling.region_dic


credFirebase = credentials.Certificate("/Users/maegbug/Downloads/PrivateCovid.json")
default_app = firebase_admin.initialize_app(credFirebase,{'databaseURL':db_url})

coAvoidDb = firestore.client()

def inputKoreaData():

    todayIndex = 0

    for i in range(len(Koreadata)):

        doc_ref = coAvoidDb.collection(u'korea').document()
        doc_ref.set({

            u'state_date_kor': Koreadata.iloc[i].iloc[0],                    
            u'decide_cnt_kor': int(Koreadata.iloc[i].iloc[1]),
            u'clear_cnt_kor' : int(Koreadata.iloc[i].iloc[2]) ,
            u'exam_cnt_kor' : int(Koreadata.iloc[i].iloc[3]),
            u'death_cnt_kor' : int(Koreadata.iloc[i].iloc[4]),
            u'today_covid_define' : int(koreaTodayData[todayIndex])
        })

        todayIndex += 1

        

def inputRegionData():
    
    for i in range(len(regionData)):


        data = {

            u'create_date_reg': (regionData.iloc[i].iloc[0]),
            u'gubun_reg': u(regionData.iloc[i].iloc[1]),
            u'inc_dec_reg' : int(regionData.iloc[i].iloc[2]),
            u'qur_rate_reg' : float(regionData.iloc[i].iloc[3]) ,
            u'std_day_reg' : (regionData.iloc[i].iloc[4]),
            u'def_cnt' : int(regionData.iloc[i].iloc[5]),
            u'local_occ_cnt_reg' : int(regionData.iloc[i].iloc[6])
           
        }
       
        doc_ref = coAvoidDb.collection(u'region').document(u(regionData.iloc[i].iloc[1])).collection(u'date').add(data)
        
        

def inputRegionRankData():

    print(type(regionRankData))
    print(regionRankData)

    for key,value in regionRankData.items():

        print(key,value)

        data = {

            u'region_name': u(key),
            u'region_rank': int(value)
           
        }
        doc_ref = coAvoidDb.collection(u'region_rank').document(key).set(data)
        print(key,value)

    

inputKoreaData()
inputRegionData()
inputRegionRankData()




