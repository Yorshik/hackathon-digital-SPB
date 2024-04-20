import requests

url = "https://digital.etu.ru/api/mobile/schedule?groupNumber=2181"

page = requests.get(url)
print(page.status_code)
print(page.text)
with open("result1.json", "w", encoding="utf8") as file:
    file.write(page.text)
