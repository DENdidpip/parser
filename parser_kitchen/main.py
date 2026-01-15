import requests
from parse_profesia_sk import Info_profesia_sk

kde = input("Kde: ")
kto = input("Kto: ")
radius = int(input("Radius: "))
link = f"https://www.profesia.sk/praca/{kde}/{kto}/?radius=radius{radius}"
print(link)
resp = requests.get(link)
print(resp.status_code)  # Код ответа, например 200

# Use 'utf-8' encoding
with open("res.html", 'w', encoding='utf-8') as f:
    f.write(resp.text)

try:
    print(resp.json())  # Если ответ в JSON
except:
    print("no json")

parser = Info_profesia_sk("res.html")
parser.pars()
