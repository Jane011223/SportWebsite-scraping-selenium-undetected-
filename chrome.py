from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


#### Getting page url ####
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# driver = webdriver.Chrome(
#     options=options, executable_path=r'./chromedriver.exe')
driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.maximize_window()
game_links = []

playernames = []
playerscores = []
playtypes = []

player_point = "player-points"
player_rebounds = "player-rebounds"
player_assists = "player-assists"
player_threes = "player-threes"


playerlist_xpath = '//*[@id="main"]/div/div[1]/div/div[2]/div[4]/ul/li[2]/div/div/div/div[3]'
playername_xpath = '/div/div[1]/span'

driver.get("https://sportsbook.fanduel.com/navigation/nba")
def get_score(link, playtype):
    
    print(playtype)
    
    try:
        driver.get(link)
        time.sleep(20)

        try:
            driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/div[2]/div[4]/ul/li[2]/div/div/div/div[4]/div/div/div/span').click()
        except:
            print('can not find show more button')

        playerlist = driver.find_element(By.XPATH, playerlist_xpath)
        playerlists = playerlist.find_elements(By.XPATH, './div')

        for j in range(len(playerlists)):
            playerinfos = playerlists[j].find_element(By.XPATH, './div').find_elements(By.XPATH, './div')

            playername = ""
            playerscore = ""

            try:
                playername = playerinfos[0].find_element(By.XPATH, './span').get_attribute('innerHTML')

                try:
                    playerscore = playerinfos[1].find_elements(By.XPATH, './div')[0].find_elements(By.XPATH, './span')[0].get_attribute('innerHTML')
                    playerscore = playerscore[2:]
                        
                except:
                    print("Can not find the score of that player")

                print(playername)
                print(playerscore)

                playtypes.append(playtype)
                playernames.append(playername)
                playerscores.append(playerscore)
                        
            except:
                print("Can not find the name of that player")
   
    except:
        print("game link error")


def main():
    time.sleep(30)

    try:
        list = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/div[2]/div[3]/ul')


        lists = list.find_elements(By.TAG_NAME, 'li')

        for i in range(2, len(lists)-1):
            game_link = lists[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(game_link)
            game_links.append(game_link)

        for i in range(len(game_links)):
            game_point_link = game_links[i] + "?tab=" + player_point
            game_rebounds_link = game_links[i] + "?tab=" + player_rebounds
            game_assists_link = game_links[i] + "?tab=" + player_assists
            game_threes_link = game_links[i] + "?tab=" + player_threes

            #-------------------------player_points--------------------------------
            playtype = "Player Points"
            get_score(game_point_link, playtype)

            #-------------------------player_rebounds--------------------------------
            
            playtype = "Player Rebounds"
            get_score(game_rebounds_link, playtype)

            #-------------------------player_assists--------------------------------
            
            playtype = "Player Assists"
            get_score(game_assists_link, playtype)


            #-------------------------player_threes--------------------------------
            
            playtype = "Player Threes"
            get_score(game_threes_link, playtype)

    except:
        print("first element error")
    
    df = pd.DataFrame({'Player Name': playernames, 'Type': playtypes, 'Over/Under': playerscores})  # Create a DF with the lists

    with pd.ExcelWriter('result.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')


if __name__ == '__main__':
    main()

