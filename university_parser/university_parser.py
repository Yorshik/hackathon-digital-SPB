from bs4 import BeautifulSoup
import requests
import re

# Пример использования:
# directions = get_directions()
# code = input()                    <-- 09.03.01, допустим
# direction = None
# for i in directions:
#     if i.code == code:
#         direction = i
#         break
# vuzes = get_universities_by_direction(nap, 10)
# for vuz in vuzes:
#     print(vuz.dir_name, vuz.univ_name, vuz.pass_score)

url = 'https://tabiturient.ru/'

# направление подготовки
class Direction:
    def __init__(self, link, code, name):
        self.link = link
        self.code = code
        self.name = name
        self.incode = re.search(r'(\d+)/?$', link).group(1)
class DirectionInUniversity:
    def __init__(self, dir_name, dir_code, univ_name, univ_link, pass_score):
        self.dir_name = dir_name
        self.dir_code = dir_code
        self.univ_name = univ_name
        self.univ_link = univ_link
        self.pass_score = pass_score

def get_directions():
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
        naps.append(Direction(link, code, name))
    return naps

def parse_university_pass_score(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    subposes = soup.select('.headnap > div')[1:]
    pass_score = None
    for s in subposes:
        t = s.select('.napravleniedop')[0].get_text(strip=True)
        t = re.search(r'Проходной балл(\d+)', t)
        if t is None:
            continue
        t = t.group(1)
        score = int(t)
        if pass_score is None or score < pass_score:
            pass_score = score
    all_links = soup.select('.headercontent a')
    external_link = None
    for a in all_links:
        images = a.select('img[src="https://tabiturient.ru/img/external-link-symbol.png"]')
        if len(images) > 0:
            external_link = a['href']
            break

    return pass_score, external_link

def get_universities_by_direction(nap, limit):
    result = []
    form = { 'limit': limit, 'page1': 'np', 'page2': nap.incode,
            'math': 1, 'obsh': 1, 'foreg': 1, 'inform': 1,
            'biolog': 1, 'geog': 1, 'xim': 1, 'fiz': 1, 'lit': 1, 'hist': 1, 'dop':0}
    page = requests.post(url + '/ajax/ajvuz2.php', data=form)
    soup = BeautifulSoup(page.text, "html.parser")
    all_universities = soup.find_all('div', recursive=False)
    for u in all_universities:
        name = u.select('.vuzlist .table-cell-2 > span')
        if len(name) == 0:
            continue
        name = name[0].get_text(strip=True)
        additional_link = u.select('.dopvuzlist a')[1]["href"]
        pass_score, external_link = parse_university_pass_score(additional_link)
        result.append(DirectionInUniversity(nap.name, nap.incode,
                                            name, external_link, pass_score))
    return result

