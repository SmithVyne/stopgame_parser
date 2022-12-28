import requests
from bs4 import BeautifulSoup as BS

domain = "https://stopgame.ru"

def dump_json(dict_, from_year = None, to_year = None):
    import json
    result_name = ""
    result_name += "" if from_year is None else f'{from_year}-'
    result_name += "" if to_year is None else f'{to_year}'
    result_name += "Games" if result_name == "" else ""
    result_name = result_name.strip()
    with open(f'{result_name}.json', 'w') as j:
        json.dump(dict_, j)

def parse(from_year = 1980, to_year = 2024, return_years = False):
    link = f"{domain}/games/pc/izumitelno/best?year_start={from_year}&year_end={to_year}&p="
    response = requests.get(link + '1')
    soup = BS(response.content, "lxml")
    last_page = soup.find(class_ = "_container_1mcqg_1").find_all(class_= 'item')[-1].text.strip()
    games = dict()
    for i in range(1, int(last_page)+1):
        r = requests.get(link + str(i))
        new_games = parse_soup(BS(r.content, "lxml"))
        games.update(new_games)
    return games if return_years == False else games, from_year, to_year


def parse_soup(soup):
    games = dict()
    for game in soup.find('div', class_ = '_games-grid_v95ji_304').find_all('a'):
        title = game.get('title')
        href = domain + game.get('href')
        picture = game.find('img').get('src')
        rating = game.find(class_ = '_rating_67304_39').text
        games[title] = {
            "link" : href,
            "picture_link" : picture,
            "rating" : rating
        }
    return games

if __name__ == "__main__":
    dump_json(*parse(return_years=True))
