import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import numpy as np
from tqdm import tqdm
import time
import re
import os

# Some colors for the terminal
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m' # Resetting the orifinal color of the terminal

# Where we will store our scrapped links
links = []
#Number of pages we want to scrape
pages = 1 

# Clearing the terminal and showing progress
os.system('cls')
print(f"{YELLOW}\n[1/4] Scraping listing links...{RESET}")

# Itterating over the pages
for page in range(1, pages + 1):
    # Setting up the Target and accessing the website
    target_url = f'https://www.avito.ma/fr/maroc/voitures?o={page}'
    header = {'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
    response = requests.get(target_url, headers=header, timeout=15)
    response.raise_for_status()

    page_CONTENT = bs(response.content, "html.parser")
    listings = page_CONTENT.find_all("a", class_="sc-1jge648-0")
    # Getting the link of each listing and append it to out listings list
    for listing in listings:
        try:
            link = listing.get("href") if listing and listing.get("href") else "N/A"
            links = np.append(links, link)


        # Error handlers for timeout and failed requests
        except requests.ReadTimeout:
            requests.failed_links.append(link)
            tqdm.write(f"{RED}⚠️ Timeout, skipped: {link}{RESET}")

        except requests.RequestException as e:
            requests.failed_links.append(link)
            tqdm.write(f"{RED}❌ Request failed: {link} ({e}){RESET}")
    
    print(f"{GREEN}→ page {page} done, {len(listings)} listings found{RESET}")

# Dropping duplicat links
link_sr = pd.Series(links)
link_sr = link_sr.drop_duplicates().reset_index(drop=True)

# Array of links
print(f"\n{YELLOW}[2/4] Scraping listing details...{RESET}")
links = np.array(link_sr) 
listings = []
headers = {"user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36")}

#Itterating over the links we got
for link in tqdm(links, desc=f"{BLUE}Scraping listings{RESET}", unit="listing"):
    try:
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        page = bs(response.content, "html.parser")
        # Link
        listing = {"lien": link}

        # listing title
        title = page.find("h1", class_="sc-16573058-5 izVEJU")
        listing["titre_annonce"] = title.text.strip() if title else None

        # Price
        price = page.find("div", class_="sc-16573058-10 kRLGQQ")
        listing["prix"] = price.text.strip() if price else None

        # Address & date
        spans = page.find_all("span", class_="sc-16573058-17 gLkxLA")
        listing["spans"] = [span.text.strip() for span in spans] if spans else None

        # Owner
        owner = page.find("p",class_="sc-1x0vz2r-0 fUTtTl sc-1l0do2b-9 bJuYLD")
        listing["proprietere"] = owner.text.strip() if owner else None

        # Tags
        spans = page.find_all("span", class_="sc-1x0vz2r-0 fjZBup")
        listing["tags"] = [span.text.strip() for span in spans] if spans else None
        # Images
        listing["images"] = [img.get("src") for img in page.find_all("img", class_="sc-1gjavk-0 fpXQoT") if img.get("src")] if page.find_all("img", class_="sc-1gjavk-0 fpXQoT") else None
        
        # Append listing to listings array
        listings.append(listing)

        # Waiting a bit so we dont get banned (skiped, im willing to take the risk lol)
        #time.sleep(1.5)

    # Error handlers for timeout and failed requests
    except requests.ReadTimeout:
            requests.failed_links.append(link)
            tqdm.write(f"{RED}⚠️ Timeout, skipped: {link}{RESET}")

    except requests.RequestException as e:
        requests.failed_links.append(link)
        tqdm.write(f"{RED}❌ Request failed: {link} ({e}){RESET}")

print(f"{GREEN}✅ Scraping completed successfully!{RESET}")

# price cleaning
def clean_price(x):
    # Remove anything that is not a digit
    x = re.sub(r"[^\d]", "", x)
    return int(x) if x.isdigit() else None

# Mileage cleaning
def clean_mileage(tags):
    if not tags or len(tags) <= 4:
        return np.nan
    val = tags[4].strip().lower()
    val = re.sub(r"[^\d]", "", val)
    return int(val) if val.isdigit() else np.nan

# Setting up the dataFrame and feed it our listings list
df_raw = pd.DataFrame(listings)
df_clean = df_raw.copy()
print(f"\n{YELLOW}[3/4] Cleaning & structuring data...{RESET}")

# Dividing 'spans' column into 'ville', 'quartier', 'date'
df_clean["ville"] = df_clean["spans"].apply(lambda x: x[0].split(",")[1].strip().lower() if len(x) > 0 and len(x[0].split(",")) > 1 else None)
df_clean["quartier"] = df_clean["spans"].apply(lambda x: x[0].split(",")[0].strip().lower() if len(x) > 0 else None)
df_clean['date'] = df_clean['spans'].apply(lambda x : x[1].lstrip("il y a ").lower() if len(x) > 1 else None)

# cleaning price Column
df_clean['prix'] = df_clean['prix'].apply(clean_price)

# Dividing 'tags' column into 'category', 'annee', 'transsmission', 'carburant', 'kilometrage', 'marque', 'modele', 'equipements'
df_clean['category'] = df_clean['tags'].apply(lambda x : x[0].split(",")[0].strip().lower() if len(x) > 0 else None)
df_clean['type_annonce'] = df_clean['tags'].apply(lambda x : x[0].split(",")[1].strip().lower() if len(x) > 0 else None)
df_clean['annee'] = df_clean['tags'].apply(lambda x : int(x[1].strip()) if len(x) > 1 else None)
df_clean['transmission'] = df_clean['tags'].apply(lambda x : x[2].strip().lower() if len(x) > 2 else None)
df_clean['carburant'] = df_clean['tags'].apply(lambda x : x[3].strip().lower() if len(x) > 3 else None)
df_clean['kilometrage'] = df_clean['tags'].apply(clean_mileage)
df_clean['marque'] = df_clean['tags'].apply(lambda x : x[5].strip().lower() if len(x) > 5 else None)
df_clean['modele'] = df_clean['tags'].apply(lambda x : x[6].strip().lower() if len(x) > 6 else None)
df_clean['equipements'] = df_clean['tags'].apply(lambda x : [e.strip().lower() for e in x[7:]] if len(x) > 7 else None)

# Dropping 'tags' and 'spans' columns 
df_clean = df_clean.drop(columns=['tags', 'spans'])

# Organizing the columns
df_clean = df_clean.reset_index(drop=True)
df_clean = df_clean[['titre_annonce', 'type_annonce', 'ville' ,'quartier' , 'prix', 'marque', 'modele', 'annee', 'kilometrage', 'carburant', 'transmission', 'equipements', 'date', 'proprietere', 'images', 'lien']]
print(f"{GREEN}📦 Total listings collected: {len(df_clean)}{RESET}")

# Saving the fnale result
print(f"\n{YELLOW}[4/4] Saving CSV...{RESET}")

try:
    df_clean.to_csv("data/avito_listings.csv" , index= False)
    print(f"{GREEN}💾 Saved to: data/avito_listings.csv{RESET}")
except e:
    print(f"{RED}❌ Error occurued saving the data: {e}{RESET}")