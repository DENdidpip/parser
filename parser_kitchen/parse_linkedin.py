from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class Info_linkedin:
    def __init__(self, link, email, password):
        self.link = link
        self.email = email
        self.password = password

    def pars_linkedin(self):
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        # ---------- LOGIN ----------
        driver.get(self.link)
        time.sleep(3)
        driver.find_element(By.ID, "username").send_keys(self.email)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        # ---------- SEARCH ----------
        job = "python"
        location = "Bratislava"
        driver.get(
            f"https://www.linkedin.com/jobs/search/?keywords={job}&location={location}"
        )
        time.sleep(7)
        # ---------- PARSE ----------
        cards = driver.find_elements(
            By.CSS_SELECTOR,
            "div.job-card-list__entity-lockup"
        )

        data = []

        for card in cards:
            try:
                title = card.find_element(
                    By.CSS_SELECTOR,
                    "a.job-card-list__title--link"
                ).text

                company = card.find_element(
                    By.CSS_SELECTOR,
                    ".artdeco-entity-lockup__subtitle"
                ).text

                location = card.find_element(
                    By.CSS_SELECTOR,
                    ".job-card-container__metadata-wrapper li"
                ).text

                link = card.find_element(
                    By.CSS_SELECTOR,
                    "a.job-card-list__title--link"
                ).get_attribute("href")

                real_title = ""
                for i in title:
                    real_title += i
                    if i == "\n":
                        break
                data.append({
                    "title": real_title,
                    "employer": company,
                    "location": location,
                    "salary": "in description",
                    "link": link
                })

            except Exception as e:
                continue
        driver.quit()
        return data

