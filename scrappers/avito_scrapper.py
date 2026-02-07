import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

ALL_LISTINGS = []
TOTAL = 0
PAGES = 3

for PAGE in range(1, PAGES):
    TARGET_URL = f'https://www.avito.ma/fr/maroc/voitures?o={PAGE}'
    HEADERS = {'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
    RESPONSE = requests.get(TARGET_URL, headers=HEADERS)
    PAGE_CONTENT = bs(RESPONSE.content, "html.parser")
    LISTINGS = PAGE_CONTENT.find_all("a", class_="sc-1jge648-0")

    for LISTING in LISTINGS:

        TITLE = LISTING.find("p" , class_="sc-1x0vz2r-0 iHApav")
        TITLE = TITLE.text.strip() if TITLE else "N/A"

        TYPE_LOCATION = LISTING.find("div", class_="sc-b57yxx-10 fHMeoC")
        TYPE_LOCATION = TYPE_LOCATION.text.strip() if TYPE_LOCATION else "N/A"
        TYPE_LOCATION = TYPE_LOCATION.split(" dans ")
        TYPE = TYPE_LOCATION[0]
        LOCATION = TYPE_LOCATION[1]

        DATE = LISTING.find("p", class_="sc-1x0vz2r-0 layWaX")
        DATE = DATE.text.strip() if DATE else "N/A"
        
        TAGS = LISTING.find_all("span", class_="sc-1s278lr-0 cAiIZZ")
        TAGS = [TAG.text.strip() for TAG in TAGS] if TAGS else []
        try :
            YEAR = TAGS[0]
            TRANSMISSION = TAGS[1]
            FUEL = TAGS[2]
        except IndexError:
            YEAR = "N/A"
            TRANSMISSION = "N/A"
            FUEL = "N/A"

        IMAGE_TAG = LISTING.find("img", class_="sc-1lb3x1r-3")
        if IMAGE_TAG:
            if IMAGE_TAG.get("data-src"):
                IMAGE = IMAGE_TAG["data-src"]
            elif IMAGE_TAG.get("data-srcset"):
                IMAGE = IMAGE_TAG["data-srcset"].split(" ")[0]
            elif IMAGE_TAG.get("src"):
                IMAGE = IMAGE_TAG["src"]
            else:
                IMAGE = "N/A"

        OWNER = LISTING.find("p", class_="sc-1x0vz2r-0 hNCqYw sc-5rosa-7 hHZQmC")
        OWNER = OWNER.text.strip() if OWNER else "-"

        LINK = LISTING.get("href") if LISTING and LISTING.get("href") else "N/A"
        
        ALL_LISTINGS.append({
            "type_annonce" : TYPE,
            "titre" : TITLE,
            "location" : LOCATION,
            "date" : DATE,
            "tags": TAGS,
            "modele" : YEAR,
            "transsmission" : TRANSMISSION,
            "carburant" : FUEL,
            "image" : IMAGE,
            "propriétere" : OWNER,
            "link" : LINK
        })

        TOTAL += 1
        
print(TOTAL)
DF = pd.DataFrame(ALL_LISTINGS)
DF.to_csv("Listings.csv", index = False)