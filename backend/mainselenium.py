import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json
import csv

from termcolor import colored
from BoardGame import BoardGame
import time

BOARDGAMESLOGIN = "https://boardgamegeek.com/login?redirect_server=1"
BOARDGAMEGEEKBROWSE = "https://boardgamegeek.com/browse/boardgame/page/"
BOARDGAMEGEEK = "https://boardgamegeek.com/"

CSVFILE = "boardgames.csv"


def startBrowser():
    driver.get(BOARDGAMESLOGIN)
    
    with open('credentials.json') as f:
        f = json.load(f)
        username = f['username']
        password = f['password']

    webconsentData = driver.find_element(By.CLASS_NAME, "fc-cta-do-not-consent").click()
    webusername = driver.find_element(By.ID, "inputUsername")
    webpassword = driver.find_element(By.ID, "inputPassword")
    print(webusername.screenshot("username.png"))
    webusername.send_keys(username)
    webpassword.send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn-primary").click()
    
    wait = WebDriverWait(driver, 5)
    wait.until(lambda d : driver.current_url == "https://boardgamegeek.com/")
    
def getGamePageHtml(boardgameLink):
    response = requests.get(boardgameLink)
    if response.status_code == 200:
        #print("Successfully retrieved page ",  pageNumber)
        return response.text
    else:
        print(f"Failed to load page")
        return None

def analyzeGame(boardgameLink):
    
    soup = BeautifulSoup(getGamePageHtml(boardgameLink), 'html.parser')
    #print(soup.prettify())
    
    string_tag = soup.find_all("script")[2].string
    start_index = string_tag.find('GEEK.geekitemPreload = ') + len('GEEK.geekitemPreload = ')
    end_index = string_tag.find(';\n', start_index)
    geekitemPreload_str = string_tag[start_index:end_index]
    
    geekitemPreload = json.loads(geekitemPreload_str)
    
    title = geekitemPreload['item']['name']
    id = geekitemPreload['item']['objectid']
    amountOfRatings = geekitemPreload['item']['stats']['usersrated']
    averageRating = geekitemPreload['item']['stats']['average']
    minage = geekitemPreload['item']['minage']
    minplayers = geekitemPreload['item']['minplayers']
    maxplayers = geekitemPreload['item']['maxplayers']
    ranking = geekitemPreload['item']['rankinfo'][0]['rank']
    minplaytime = geekitemPreload['item']['minplaytime']
    maxplaytime = geekitemPreload['item']['maxplaytime']
    yearpublished = geekitemPreload['item']['yearpublished']
    categories = [category['name'] for category in geekitemPreload['item']['links']['boardgamecategory']]
    boardgamemechanic = [mechanic['name'] for mechanic in geekitemPreload['item']['links']['boardgamemechanic']]
    boardgamesubdomain = [subdomain['name'] for subdomain in geekitemPreload['item']['links']['boardgamesubdomain']]
    
    boardGame = BoardGame(
        title=title,
        link=boardgameLink,
        objectid=id,
        minplayers=minplayers,
        maxplayers=maxplayers,
        yearpublished=yearpublished,
        minplaytime=minplaytime,
        maxplaytime=maxplaytime,
        ranking=ranking,
        amountOfRatings=amountOfRatings,
        averageRating=averageRating,
        minage=minage,
        categories=categories,
        boardgamemechanic=boardgamemechanic,
        boardgamesubdomain=boardgamesubdomain
    )
    
    return boardGame

def createCSV(csvPath):

    # Write the BoardGame objects to the CSV file
    with open(csvPath, mode='a', newline='\n') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow([
            'Title', 'Link', 'Object ID', 'Min Players', 'Max Players', 'Year Published',
            'Min Playtime', 'Max Playtime', 'Ranking', 'Amount of Ratings', 'Average Rating',
            'Min Age', 'Categories', 'Board Game Mechanic', 'Board Game Subdomain'
        ])
    
    return
    
def analyzePage():
    boardgames:BoardGame = []
    tstart = time.time()

    index = 0
    for i in range(20, 100):
        
        driver.get(BOARDGAMEGEEKBROWSE + str(i))
        
        print(driver.current_url)
        htmlSource = driver.page_source
        #print(htmlSource)
        #analyzing page i
        soup = BeautifulSoup(htmlSource, 'html.parser')
        #print(soup.prettify())
        boardgameRows = soup.find_all(name="tr", id="row_")
        if not boardgameRows:
            file = open("error.html", "a")
            file.write(soup.prettify())
            print(f"No rows found for {i} page")
            return
        
        for boardgameBS in boardgameRows:
            boardgameLink = boardgameBS.find_all("a")[2].get("href")
            boardgames.append(analyzeGame(BOARDGAMEGEEK + boardgameLink))
            print(boardgames[index])
            printGameCSV(CSVFILE, boardgames[index])
            index += 1
        
        print(colored(f"Page {i} analyzed", "green"))
        
    tfinish = time.time()
    print(f"It took {float(tfinish - tstart).__round__(2)}s to exectue {i} pages" )
    
def printGameCSV(csvPath, game:BoardGame):

    # Write the BoardGame objects to the CSV file
    with open(csvPath, mode='a', newline="\n") as file:
        writer = csv.writer(file)
        
        # Write the data rows
        writer.writerow([
            game.title, game.link, game.objectid, game.minplayers, game.maxplayers,
            game.yearpublished, game.minplaytime, game.maxplaytime, game.ranking,
            game.amountOfRatings, game.averageRating, game.minage,
            ', '.join(game.categories), ', '.join(game.boardgamemechanic),
            ', '.join(game.boardgamesubdomain)
        ])
        
        
    return


driver = webdriver.Chrome()

createCSV(CSVFILE)
startBrowser()
analyzePage()