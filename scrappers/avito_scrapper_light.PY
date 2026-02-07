import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# where we gonna store the listings
ALL_LISTINGS = []

# Number of pages we want to scrape
PAGES = 10

# Iterating over each page from the website within our desired range
for PAGE in range(1, PAGES + 1):
    TARGET_URL = f'https://www.avito.ma/fr/maroc/voitures?o={PAGE}'
    HEADERS = {'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
    RESPONSE = requests.get(TARGET_URL, headers=HEADERS)
    PAGE_CONTENT = bs(RESPONSE.content, "html.parser")
    LISTINGS = PAGE_CONTENT.find_all("a", class_="sc-1jge648-0")

    # iterating over each listing car in the page
    for LISTING in LISTINGS:

        # Title
        TITLE = LISTING.find("p" , class_="sc-1x0vz2r-0 iHApav")
        TITLE = TITLE.text.strip() if TITLE else "N/A"

        # Listing type and the location
        TYPE_LOCATION = LISTING.find("div", class_="sc-b57yxx-10 fHMeoC")
        TYPE_LOCATION = TYPE_LOCATION.text.strip() if TYPE_LOCATION else "N/A"
        TYPE_LOCATION = TYPE_LOCATION.split(" dans ")
        TYPE = TYPE_LOCATION[0]
        LOCATION = TYPE_LOCATION[1]

        # Date of the listing
        DATE = LISTING.find("p", class_="sc-1x0vz2r-0 layWaX")
        DATE = DATE.text.strip() if DATE else "N/A"

        # Tags
        TAGS = LISTING.find_all("span", class_="sc-1s278lr-0 cAiIZZ")
        TAGS = [TAG.text.strip() for TAG in TAGS] if TAGS else []

        # Separating the tags to transmission, year, fuel
        try :
            YEAR = TAGS[0]
            TRANSMISSION = TAGS[1]
            FUEL = TAGS[2]
        except IndexError:
            YEAR = "N/A"
            TRANSMISSION = "N/A"
            FUEL = "N/A"

        # Owner
        OWNER = LISTING.find("p", class_="sc-1x0vz2r-0 hNCqYw sc-5rosa-7 hHZQmC")
        OWNER = OWNER.text.strip() if OWNER else "-"

        # link of the listing
        LINK = LISTING.get("href") if LISTING and LISTING.get("href") else "N/A"
        
        # Appending all the data to our listings list
        ALL_LISTINGS.append({
            "type_annonce" : TYPE,
            "titre" : TITLE,
            "location" : LOCATION,
            "date" : DATE,
            "annee" : YEAR,
            "transmission" : TRANSMISSION,
            "carburant" : FUEL,
            "proprietere" : OWNER,
            "lien" : LINK
        })
    # Waiting a bit (skipped)
    #time.sleep(1.5)

# Coverting list to dataFrame
df = pd.DataFrame(ALL_LISTINGS)

# Cleaning the data 
df['titre'] = df['titre'].str.lower()
df['location'] = df['location'].str.lower()
df["ville"] = df["location"].str.split(",").str[0]
df["quartier"] = df["location"].str.split(",").str[1]
df["quartier"] = df["quartier"].str.lstrip(" ")
df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
df['annee'] = df['annee'].astype('Int64') 

# Droping 'location' column
df = df.drop(columns='location')

# Organizing the columns
df = df.reset_index(drop=True)
df = df[['titre', 'type_annonce','ville' ,'quartier', 'annee', 'carburant', 'transmission', 'date', 'proprietere', 'lien']]

# Saving the final result
df.to_csv("../data/avito_listings_light.csv", index=0)