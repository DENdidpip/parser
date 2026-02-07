from bs4 import BeautifulSoup

class Info_profesia_sk:
    BASE_URL = "https://www.profesia.sk"

    def __init__(self, file="res.html"):
        self.file = file
        self.vacancies = []

    def _get_text(self, parent, tag, class_=None):
        el = parent.find(tag, class_=class_)
        return el.text.strip() if el else None

    def pars(self):
        with open(self.file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        for vac in soup.find_all("li", class_="list-row"):
            title = self._get_text(vac, "h2")
            employer = self._get_text(vac, "span", "employer")
            location = self._get_text(vac, "span", "job-location")

            salary_tag = vac.find("span", class_="label-group")
            salary = salary_tag.text.strip().split("\n")[0] if salary_tag else None

            link_tag = vac.find("a", id=lambda x: x and x.startswith("offer"))
            link = self.BASE_URL + link_tag["href"] if link_tag else None

            if link:
                self.vacancies.append({
                    "title": title,
                    "employer": employer,
                    "location": location,
                    "salary": salary,
                    "link": link
                })

        return self.vacancies
