import scraper

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

max_results_per_state = 10
state_set = ["California", "New York", "Washington", "Illinois", "Texas"]
data = {"job_title":[], "company":[], "location":[]}

#start scraping
for state in state_set:
    for start in range(0, max_results_per_state, 10):
        URL = "https://www.indeed.com/jobs?q=Software+intern&l=" + str(state) + "&start="  + str(start)
        page = requests.get(URL)
        time.sleep(1)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        listings = soup.find_all(name="div", attrs={"class":"row"})
        titles = scraper.extract_job_titles(soup, listings)
        companies = scraper.extract_job_companies(soup, listings)
        locations = scraper.extract_job_locations(soup, listings)
        data["job_title"].extend(titles)
        data["company"].extend(companies)
        data["location"].extend(locations)

sample_df = pd.DataFrame(data)
sample_df.to_csv("output.csv", encoding='utf-8')
