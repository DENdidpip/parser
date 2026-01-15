import requests
import json
from parse_profesia_sk import Info_profesia_sk
class Our_result:
    def __init__(self, where, job):
        self.__where = where
        self.__job = job
        link = f"https://www.profesia.sk/praca/{self.__where}/{self.__job}/?radius=radius0"
        resp = requests.get(link)

        # Use 'utf-8' encoding
        with open("res.html", 'w', encoding='utf-8') as f:
            f.write(resp.text)

        try:
            print(resp.json())  # Если ответ в JSON
        except:
            print("no json")

        parser = Info_profesia_sk("res.html")
        data = parser.pars()
        with open("vacancies.json", "w", encoding = "utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)