import requests
import pandas as pd
import time
import bs4
from bs4 import BeautifulSoup

def extract_job_titles(soup, listings):
    """ Looks through every div tag with attribute class='row' and then every anchor
    tag within those divs with attribute data-tn-element='jobTitle' because these
    are the html elements with the job title for each job. We want to take these
    titles for each job so we can see what jobs we're scraping"""
    jobs = []
    for div_tag in listings:
        for a_tag in div_tag.find_all(name="a", attrs={"data-tn-element" : "jobTitle"}):
            jobs.append(a_tag["title"])
    return jobs

def extract_job_companies(soup, listings):
    """ Looks through ever div tag with attribute class='row' and then searches for 
    spans with class company or spans with class result-link-source because these spans 
    contain the job company names."""
    companies = []
    for div_tag in listings:
        spans_with_company_class = div_tag.find_all(name="span", attrs={"class":"company"})
        if len(spans_with_company_class) > 0:
            for company_name_span in spans_with_company_class:
                companies.append(company_name_span.text.strip())
        else:
            #try spans with class='result-link-source' since company names are sometimes stored there
            try_RLS = div_tag.find_all(name="span", attrs={"class": "result-link-source"})
            for company_name_span in try_RLS:
                companies.append(company_name_span.text.strip())
    return companies

def extract_job_locations(soup, listings):
    """ Looks through every div tag (a job listing) and finds the span tag with class
    location and extracts the location of the job listing """
    locations = []
    for div_tag in listings:
        for location_span in div_tag.find_all(name="span", attrs={"class":"location"}):
            locations.append(location_span.text.strip())
    return locations

def scrape(max_results_per_state, state_set, data):
    for state in state_set:
        for start in range(0, max_results_per_state, 10):
            URL = "https://www.indeed.com/jobs?q=Software+intern&l=" + str(state) + "&start="  + str(start)
            page = requests.get(URL)
            time.sleep(1)
            soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
            listings = soup.find_all(name="div", attrs={"class":"row"})
            titles = extract_job_titles(soup, listings)
            companies = extract_job_companies(soup, listings)
            locations = extract_job_locations(soup, listings)
            data["Job Title"].extend(titles)
            data["Company"].extend(companies)
            data["Location"].extend(locations)

    sample_df = pd.DataFrame(data)
    return sample_df
