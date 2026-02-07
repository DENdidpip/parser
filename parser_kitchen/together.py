# together.py
import requests
from parser_kitchen.parse_profesia_sk import Info_profesia_sk
from parser_kitchen.parse_linkedin import Info_linkedin
from parser_kitchen.login_linkedin import LOGIN_LINKEDIN as ll, PASSWORD_LINKEDIN as pl

class Our_result:
    def __init__(self, where, job):
        self.where = where
        self.job = job
        self.link_prof_sk = f"https://www.profesia.sk/praca/{self.where}/{self.job}/?radius=radius0"
        self.link_likedin = f"https://www.linkedin.com/jobs/search/?keywords={self.job}&location={self.where}"

        #________profesia.sk_______
        resp = requests.get(self.link_prof_sk)
        html = resp.text
        with open("res.html", "w", encoding="utf-8") as f:
            f.write(html)
        parser = Info_profesia_sk("res.html")
        ################################
        #________linkedin_____________
        parser1 = Info_linkedin(f"https://www.linkedin.com/login", ll, pl)
        self.data = parser.pars() + parser1.pars_linkedin()

    def get_data(self):
        return self.data
