from bs4 import BeautifulSoup

class Info_profesia_sk:

    def __init__(self, file="res.html"):
        self.__file = file
        self.link = f"https://www.profesia.sk"
        self.vacancies = []

    def pars(self):
        with open(self.__file, "r", encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        for vac in soup.find_all("li", class_="list-row"):
            try:
                title = vac.find("h2").text.strip()
            except:
                employer = "None"
            try:
                employer = vac.find("span", class_="employer").text.strip()
            except:
                employer= "None"
            try:
                location = vac.find("span", class_= "job-location").text.strip()
            except:
                location = "None"
            try:
                salary_tag = vac.find("span", class_="label-group")
                if salary_tag:
                    salary_clean = salary_tag.text.strip().split("\n")[0].strip()
                else:
                    salary_clean = "None"
            except:
                salary_clean = "None"
            try:
                link_tag = vac.find("a", id=lambda x: x and x.startswith("offer"))
                if link_tag and link_tag.has_attr("href"):
                    link = self.link + link_tag["href"]
                else:
                    link = "None"
            except:
                link = "None"

            self.vacancies.append({
                "title": title,
                "employer": employer,
                "location": location,
                "salary": salary_clean,
                "link": link
            })
        return self.vacancies

