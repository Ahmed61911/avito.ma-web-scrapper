# Avito.ma cars Scraper

This project contains **two complementary web scrapers** designed to collect car listings data from **Avito.ma** efficiently

The idea is simple:
- ⚡ **Light Scraper** → fast, broad, minimal data
- 🐢 **Standard Scraper** → slower, deep, full data

This architecture avoids unnecessary requests while still allowing full data extraction when needed.
---
## Project Architecture

### 1️⃣ Light Scraper (Listings Page Scraper)

**Purpose**
- Quickly scrape car listings from Avito listing pages
- Collects only essential information
- Used to discover links efficiently

**Features**
- Very fast (≈ 8–10 seconds per page *without the wait function*)
- Minimal HTTP requests
- Ideal for:
  - Pagination
  - Link collection
  - Market overview

**Data Collected**
- Listing link
- Listing type
- Title
- City
- District
- Year
- Date of listing
- Tags (year, fuel, transmission, etc.)

----

### 2️⃣ Standard Scraper (Detail Page Scraper)

**Purpose**
- Visit each listing page individually
- Extract all available information

**Features**
- Slower (one request per listing ≈ 30 seconds per page *without the wait function*)
- Much richer dataset

**Data Collected**
- Title
- Listing type
- Price
- City 
- District
- Publication date
- Owner
- Mileage
- Make
- Model
- Full technical tags
- All listing images
- Link

**🛠️ Tech Stack**

- Python 3.9+
- requests
- beautifulsoup4
- pandas
- numpy
- time (standard lib)
- re (standard lib)

**📦 Installation**

*Clone the repository:*
git clone https://github.com/ahmed61911/avito.ma-web-scrapper.git
cd avito-car-scraper


*Install dependencies:*
pip install -r requirements.txt

**▶️ Usage**
*Run the Light Scraper*
python light_scraper.py
    Outputs: CSV / DataFrame containing listing links + basic info

*Run the Standard Scraper*
python standard_scraper.py

**👤 Author**
*Ahmed Baba*

