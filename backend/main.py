from bs4 import BeautifulSoup
from BoardGame import BoardGame

BOARDGAMEGEEK = "https://boardgamegeek.com/"

boardgames:BoardGame = []

f = open("page.html", "r")
html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')

for boardgameBS in soup.find_all(name="tr", id="row_")[1:]:
    boardgameLink = boardgameBS.find_all("a")[2].get("href")
    boardgameName = boardgameBS.find_all("a")[2].get_text()
    
    
    boardgames.append(BoardGame(boardgameName, BOARDGAMEGEEK + boardgameLink))
    for bg in boardgames:
        print(bg.title, bg.link)
    
    
#print(boardgameLink.get('href'))