#We work remotly basic scrapper
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

FILE = open('debug.txt' , "w")
TARGET_URL = 'https://weworkremotely.com/categories/remote-full-stack-programming-jobs'
HEADERS = {'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
RESPONSE = requests.get(TARGET_URL, headers=HEADERS)
PAGE_CONTENT = bs(RESPONSE.content, "html.parser")

    #HTML dage debug file
with open('debug.txt' , "w", encoding="utf-8") as FILE:
    FILE.write(PAGE_CONTENT.prettify())

JOBS = PAGE_CONTENT.find_all("li", class_="new-listing-container")
ALL_JOBS = []
for JOB in JOBS:
    #IMAGE = JOB.find("td", class_="image")
    TITLE = JOB.find("h3" , class_="new-listing__header__title").text.strip()
    COMPANY = JOB.find("p", class_="new-listing__company-name").text.strip()
    TAGS = JOB.find_all("p", class_="new-listing__categories__category")
    DATE = JOB.find("p", class_="new-listing__header__icons__date").text.strip()

    ALL_JOBS.append({"titre": TITLE, "entreprise": COMPANY, "tags": list(TAG.text.strip() for TAG in TAGS), "date": DATE})
    #print(f"-Poste: {TITLE} \n-Entreprise: {COMPANY} \n-Tags: {list(TAG.text.strip() for TAG in TAGS)} \n-Posté il y'a : {DATE}\n" )

print(ALL_JOBS)

DF = pd.DataFrame(ALL_JOBS)
DF.to_csv("jobs.csv", index = False)
#top hiring companies
DF["entreprise"].value_counts().head(10)