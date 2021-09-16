from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
import time
import numpy as np
import pandas as pd
import requests
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome() 
# browser.find_element_by_class_name("match-link match-report rc").click()
season_number = {2010:2458,
                 2011:2935,
                 2012:3389,
                 2013:3853,
                 2014:4311,
                 2015:5826,
                 2016:6335,
                 2017:6829,
                 2018:7361,
                 2019:7811,
                 2020:8228,
                 2021:8618
                 }

def Epl_dataload(*arg):
    """
    년도를 20xx형태(다수가능)로 받아서 현재 경로에 EPL리그 데이터 저장합니다.
    
    컬럼 설명
    home_team = 홈팀 이름
    away_team = 어웨이팀 이름
    home_score = 홈팀 스코어
    away_score = 어웨이팀 스코어
    start_time = 킼오프 시간
    time_day = 매치데이

    home_open_play = 홈팀 오픈 플레이 수
    away_open_play = 어웨이팀 오픈 플레이 수
    home_setpiece = 홈팀 세트피스 수
    away_setpiece = 어웨이팀 세트피스 수
    home_counterattack = 홈팀 카운터 어택 수
    away_counterattack = 어웨이팀 카운터 어택 수
    home_penalty = 홈팀 패털티 수
    away_penalty = 어웨이팀 패털티 수

    home_cross = 홈팀 크로스 수
    away_cross = 어웨이팀 크로스 수
    home_longball = 홈팀 롱볼 수
    away_longball = 어웨이팀 롱볼 수
    home_throughball = 홈팀 돌파 수
    away_throughball = 어웨이팀 돌파 수
    home_stortball = 홈팀 짧은패스 수
    away_stortball = 어웨이팀 짧은 패스 수

    home_form = 홈팀 포메이션
    away_form = 어웨이팀 포메이션
    home_player = 홈팀 플레이어별 이름 및 평점
    away_player = 어웨이팀 플레이어별 이름 및 평점
    """
    path = "https://1xbet.whoscored.com/"
    for season in arg:

        home_team = []
        away_team = []
        home_score = []
        away_score = []
        start_time = []
        time_day = []

        home_open_play = []
        away_open_play = []
        home_setpiece = []
        away_setpiece = []
        home_counterattack = []
        away_counterattack = []
        home_penalty = []
        away_penalty = []

        home_cross = []
        away_cross = []
        home_longball = []
        away_longball = []
        home_throughball = []
        away_throughball = []
        home_stortball = []
        away_stortball = []

        home_form = []
        away_form = []
        home_player = []
        away_player = []

        #시즌 초기 화면
        season_idx = season_number[season]
        browser.get("https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/{}/England-Premier-League".format(season_idx))

        #전체 url
        seasonfull_url_list = []
        
        for round in range(1, 39):
            soup = BeautifulSoup(browser.page_source, "lxml")
            time.sleep(1)
            week_list = soup.findAll("a", attrs={"class":"match-link match-report rc"})
            browser.find_element_by_xpath('//*[@id="date-controller"]/a[1]').click()
            time.sleep(1.5)
            
            if round == 1:
                round_check = week_list
            if round_check == week_list and round != 1:
                break
            
            week_url_list = [a["href"] for a in week_list]
            seasonfull_url_list.extend(week_url_list)
            round_check = week_list
            
        for idx, url in enumerate(seasonfull_url_list):
            browser.get(path + url)
            
            #overall
            time.sleep(2)
            home_score.append(int(browser.find_element_by_class_name("result").text.split(":")[0]))
            away_score.append(int(browser.find_element_by_class_name("result").text.split(":")[1]))

            #Attempt Types
            time.sleep(1)
            home_team.append(browser.find_elements_by_class_name("team-link ")[0].text)
            away_team.append(browser.find_elements_by_class_name("team-link ")[2].text)  
            start_time.append(browser.find_elements_by_class_name("info-block")[2].text.split("\n")[1])
            time_day.append(browser.find_elements_by_class_name("info-block")[2].text.split("\n")[3])

            home_open_play.append(browser.find_elements_by_class_name("stat-value")[2].text)
            away_open_play.append(browser.find_elements_by_class_name("stat-value")[3].text)

            home_setpiece.append(browser.find_elements_by_class_name("stat-value")[4].text)
            away_setpiece.append(browser.find_elements_by_class_name("stat-value")[5].text)

            home_counterattack.append(browser.find_elements_by_class_name("stat-value")[6].text)
            away_counterattack.append(browser.find_elements_by_class_name("stat-value")[7].text)

            home_penalty.append(browser.find_elements_by_class_name("stat-value")[8].text)
            away_penalty.append(browser.find_elements_by_class_name("stat-value")[9].text)
                
            #Pass Types
            browser.find_element_by_link_text("Pass Types").click()
            time.sleep(1)
            home_cross.append(browser.find_elements_by_class_name("stat-value")[20].text)
            away_cross.append(browser.find_elements_by_class_name("stat-value")[21].text)
            home_longball.append(browser.find_elements_by_class_name("stat-value")[22].text)
            away_longball.append(browser.find_elements_by_class_name("stat-value")[23].text)
            home_throughball.append(browser.find_elements_by_class_name("stat-value")[24].text)
            away_throughball.append(browser.find_elements_by_class_name("stat-value")[25].text)
            home_stortball.append(browser.find_elements_by_class_name("stat-value")[26].text)
            away_stortball.append(browser.find_elements_by_class_name("stat-value")[27].text)

            #preview
            browser.find_element_by_link_text("Preview").click()
            time.sleep(2)
            home_form.append(browser.find_elements_by_class_name("formation-label")[0].text)
            away_form.append(browser.find_elements_by_class_name("formation-label")[1].text)
            home_player.append(browser.find_element_by_class_name("pitch").text.split("\n")[:22])
            away_player.append(browser.find_element_by_class_name("pitch").text.split("\n")[22:-1])


        season_data = pd.DataFrame((home_team, away_team, home_score, away_score, start_time, time_day, 
        home_open_play, away_open_play, home_setpiece, away_setpiece, home_counterattack, away_counterattack, home_penalty, away_penalty,
        home_cross, away_cross, home_longball, away_longball, home_throughball, away_throughball, home_stortball, away_stortball, 
        home_form, away_form, home_player, away_player), index=['home_team', 'away_team', 'home_score', 'away_score', 'start_time', 'time_day', 
        'home_open_play', 'away_open_play', 'home_setpiece', 'away_setpiece', 'home_counterattack', 'away_counterattack', 'home_penalty', 'away_penalty', 
        'home_cross', 'away_cross', 'home_longball', 'away_longball', 'home_throughball', 'away_throughball', 'home_stortball', 'away_stortball', 
        'home_form', 'away_form', 'home_player', 'away_player']).T
        
        print("샘플 5개를 출력 합니다.")
        print("*" * 100)
        print(season_data.sample(5))

        season_data.to_csv(os.getcwd() + "/season_data_{}_{}.csv".format(season,season+1))

Epl_dataload(2018)