import json
from bs4 import BeautifulSoup
import requests
from BoardGame import BoardGame
import time
BOARDGAMEGEEK = "https://boardgamegeek.com/"
BOARDGAMEGEEKBROWSE = "https://boardgamegeek.com/browse/boardgame/page/"



def getGameListPageHtml(pageNumber):
    url = BOARDGAMEGEEKBROWSE + str(pageNumber)
    
    response = requests.get(url)
    if response.status_code == 200:
        #print("Successfully retrieved page ",  pageNumber)
        return response.text
    else:
        print(f"Failed to load page")
    return None

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
    categories = geekitemPreload['item']['links']['boardgamecategory']
    boardgamemechanic = geekitemPreload['item']['links']['boardgamemechanic']
    boardgamesubdomain = geekitemPreload['item']['links']['boardgamesubdomain']
    
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
    
    
    

def analyzePage():
    boardgames:BoardGame = []
    tstart = time.time()

    index = 0
    for i in range(1, 2):
        
        #analyzing page i
        soup = BeautifulSoup(getGameListPageHtml(i), 'html.parser')

        
        for boardgameBS in soup.find_all(name="tr", id="row_")[0:]:
            boardgameLink = boardgameBS.find_all("a")[2].get("href")
            boardgames.append(analyzeGame(BOARDGAMEGEEK + boardgameLink))
            print(boardgames[index])
            index += 1
        
    tfinish = time.time()
    print(f"It took {float(tfinish - tstart).__round__(2)}s to exectue {i} pages" )
    
analyzePage()