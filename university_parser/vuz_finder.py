from bs4 import BeautifulSoup
import requests
import re

url = 'https://tabiturient.ru/'

# направление подготовки
class Nap:
    def __init__(self, link, code, name):
        self.link = link
        self.code = code
        self.name = name
        self.incode = re.search(r'(\d+)/?$', link).group(1)

def get_naps():
    page = requests.post(url + '/ajax/ajnap.php', data={'page1':'',
                                                        'page2': '',
                                                        'page3': '',
                                                        'nap': ''})
    soup = BeautifulSoup(page.text, "html.parser")
    all_links = soup.div.find_all('a')
    all_links = filter(lambda a: a["href"] != "https://tabiturient.ru", all_links)

    naps = []
    
    for l in all_links:
        link = l["href"].strip()
        values = l.select('table > tbody > tr > td')
        code = values[0].span.get_text(strip=True)
        name = values[1].span.b.get_text(strip=True)
        naps.append(Nap(link, code, name))
    return naps

def get_vuzes(nap, limit):
    form = { 'limit': limit, 'page1': 'np', 'page2': nap.incode,
            'math': 1, 'obsh': 1, 'foreg': 1, 'inform': 1,
            'biolog': 1, 'geog': 1, 'xim': 1, 'fiz': 1, 'lit': 1, 'hist': 1, 'dop':0}
    print(form)
    page = requests.post(url + '/ajax/ajvuz2.php', data=form)
    soup = BeautifulSoup(page.text, "html.parser")
    els = soup.select('.vuzlistcontent')
    print(len(els))
    for e in els:
        print(e.select('.table-cell-2 > span')[0].get_text())

naps = get_naps()
code = input()
nap = None
for i in naps:
    if i.code == code:
        nap = i
        break
get_vuzes(nap, 50)
