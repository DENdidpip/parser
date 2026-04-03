# Job Scraper Web App

## Description
This web application scrapes job listings from **Profesia.sk** and **LinkedIn**, then displays them on your own site in a clean and organized interface.  
All results are stored in the database and can be viewed or filtered in real-time.

The interface is intuitive — users can browse and search job offers effortlessly.

## How to Use
- Open the website and navigate to the jobs section.
- Browse available offers or use filters to refine results.
- Click on any listing to see full details.

Everything is designed to be intuitive and straightforward — no tutorial required.

## Tech Stack
- **Python 3.12**
- **Flask 3.1.2**
- **Flask-SQLAlchemy 3.1.1**
- **Selenium 4.40.0**
- **Requests 2.32.5**
- **PostgreSQL / MySQL**
- **Beautifulsoup4 4.14.3**
- **SQLAlchemy 2.0.45**  
- **Webdriver-manager 4.0.2**  


## Project Structure
```text
.
├── parser_kitchen
│   ├── parse_linkedin.py
│   ├── parse_profesia_sk.py
│   ├── res.html
│   └── together.py
├── static
│   └── css
├── templates
│   ├── index.html
│   ├── out.html
│   ├── sign_up.html
│   └── verify.html
├── .env
├── .gitignore
├── a.txt
├── app.py
├── Dockerfile
├── README.md
├── requirements.txt
└── res.html