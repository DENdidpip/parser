import os
import requests
from dotenv import load_dotenv

from parser_kitchen.parse_profesia_sk import Info_profesia_sk
from parser_kitchen.parse_linkedin import Info_linkedin

load_dotenv()

LOGIN_LINKEDIN = os.getenv("LOGIN_LINKEDIN")
PASSWORD_LINKEDIN = os.getenv("PASSWORD_LINKEDIN")


class Our_result:
    def __init__(self, where, job):
        self.where = where
        self.job = job

        self.link_prof_sk = f"https://www.profesia.sk/praca/{self.where}/{self.job}/?radius=radius0"
        self.link_linkedin = f"https://www.linkedin.com/jobs/search/?keywords={self.job}&location={self.where}"

        # =========================
        # PROFESIA.SK
        # =========================
        resp = requests.get(self.link_prof_sk)
        html = resp.text

        with open("res.html", "w", encoding="utf-8") as f:
            f.write(html)

        parser = Info_profesia_sk("res.html")

        # =========================
        # LINKEDIN
        # =========================
        parser1 = Info_linkedin(
            "https://www.linkedin.com/login",
            LOGIN_LINKEDIN,
            PASSWORD_LINKEDIN
        )

        self.data = parser.pars() + parser1.pars_linkedin()

    def get_data(self):
        return self.data