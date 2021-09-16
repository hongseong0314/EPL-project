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
season_number = {2010:2454,
                 2011:2929,
                 2012:3381,
                 2013:3844,
                 2014:4309,
                 2015:5820,
                 2016:6368,
                 2017:6841,
                 2018:7368,
                 2019:7839,
                 2020:8297,
                 2021:8618
                 }

def carabao_dataload(*arg):

    path = "https://1xbet.whoscored.com/"
    for season in arg:
        home_team = []
        away_team = []
        time_day = []
        #시즌 초기 화면
        season_idx = season_number[season]
        browser.get("https://1xbet.whoscored.com/Regions/252/Tournaments/29/Seasons/{}/England-League-Cup".format(season_idx))

        
        for round in range(1, 39):
            soup = BeautifulSoup(browser.page_source, "lxml")
            time.sleep(1)
            check_day = soup.find("a", attrs={"id":"date-config-toggle-button"})
            check_day = check_day.find('span', attrs={"class":"text"}).text
            
            if round == 1:
                round_check = check_day
            if round_check == check_day and round != 1:
                break
            round_check = check_day

            try:
                elem = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'divtable-row')))
                # 첫번째 결과 출력
                row_list = browser.find_elements_by_class_name('divtable-row')

            finally:
                pass

            for idx, row in enumerate(row_list):
                try:
                    row.find_element_by_class_name('divtable-header').text
                    day = row.find_element_by_class_name('divtable-header').text

                except Exception as ex:
                    time.sleep(1)
                    home = row.text.split('\n')[1]
                    away = row.text.split('\n')[3]
                    home_team.append(home)
                    away_team.append(away)
                    time_day.append(day)
                    print(day, home, away)
            
            browser.find_element_by_xpath('//*[@id="date-controller"]/a[1]').click()
            time.sleep(1.5)
        
        form = pd.DataFrame((home_team, away_team, time_day), index=['home_team', 'away_team', 'time_day']).T
        
        print("샘플 5개를 출력 합니다.")
        print("*" * 100)
        print(form.sample(5))

        form.to_csv(os.getcwd() + "/carabao_{}_{}.csv".format(season,season+1))


carabao_dataload(2015,2016,2017,2018,2019)