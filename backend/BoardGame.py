class BoardGame:
    def __init__(self, title, link, objectid, minplayers, maxplayers, yearpublished, minplaytime, maxplaytime, ranking, amountOfRatings, averageRating, minage, categories, boardgamemechanic, boardgamesubdomain):
        self.title = title
        self.link = link
        self.objectid = objectid
        self.minplayers = minplayers
        self.maxplayers = maxplayers
        self.yearpublished = yearpublished
        self.minplaytime = minplaytime
        self.maxplaytime = maxplaytime
        self.ranking = ranking
        self.amountOfRatings = amountOfRatings
        self.averageRating = averageRating
        self.minage = minage
        self.categories = categories
        self.boardgamemechanic = boardgamemechanic
        self.boardgamesubdomain = boardgamesubdomain
        
    def __str__(self):
        return f"Title: {self.title}"