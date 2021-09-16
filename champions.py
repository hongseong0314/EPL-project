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
season_number = {2010:[2474, 5021, 6222],
                 2011:[2944, 6021, 6223],
                 2012:[3416, 7228, 6885],
                 2013:[3872, 8462, 8175],
                 2014:[4333, 11810, 11564],
                 2015:[5848, 13185, 12933],
                 2016:[6349, 14361, 14201],
                 2017:[6842, 15619, 15511],
                 2018:[7352, 16651, 16704],
                 2019:[7804, 18065, 17993],
                 2020:[8177, 19130, 19009],
                 2021:8618
                 }

def Champions_dataload(*arg):

    path = "https://1xbet.whoscored.com/"

    for season in arg:
        home_team = []
        away_team = []
        time_day = []
        season_idx = season_number[season]

        # groub stage
        browser.get("https://1xbet.whoscored.com/Regions/250/Tournaments/12/Seasons/{}/Stages/{}/Show/Europe-Champions-League-{}-{}".format(season_idx[0], season_idx[2], season, season+1))

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
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'team-link')))
            except:
                print('team-link not founded')
                browser.quit()
            home_team.append(browser.find_elements_by_class_name("team-link")[0].text)
            away_team.append(browser.find_elements_by_class_name("team-link")[2].text)  
            time_day.append(browser.find_elements_by_class_name("info-block")[2].text.split("\n")[3])


        # final stage
        browser.get("https://1xbet.whoscored.com/Regions/250/Tournaments/12/Seasons/{}/Stages/{}/Show/Europe-Champions-League-{}-{}".format(season_idx[0], season_idx[1], season, season+1))

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
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'team-link')))
            except:
                print('team-link not founded')
                browser.quit()
            home_team.append(browser.find_elements_by_class_name("team-link")[0].text)
            away_team.append(browser.find_elements_by_class_name("team-link")[2].text)  
            time_day.append(browser.find_elements_by_class_name("info-block")[2].text.split("\n")[3])
        
        form = pd.DataFrame((home_team, away_team, time_day), index=['home_team', 'away_team', 'time_day']).T
        
        print("샘플 5개를 출력 합니다.")
        print("*" * 100)
        print(form.sample(5))

        form.to_csv(os.getcwd() + "/champions_{}_{}.csv".format(season,season+1))


Champions_dataload(2021)