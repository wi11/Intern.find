import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

URL = "https://www.indeed.com/jobs?q=Software+intern&start=10"

#request the URL above
page = requests.get(URL)

#use html parser so that python can read the compnents of the page
soup = BeautifulSoup(page.text, "html.parser")

def extract_job_title(soup):
    """ Looks through every div tag with attribute class='row' and then every anchor
    tag within those divs with attribute data-tn-element='jobTitle' because these
    are the html elements with the job title for each job. We want to take these
    titles for each job so we can see what jobs we're scraping"""
    jobs = []
    for div_tag in soup.find_all(name="div", attrs={"class":"row"}):
        for a_tag in div_tag.find_all(name="a", attrs={"data-tn-element" : "jobTitle"}):
            jobs.append(a_tag["title"])
    return jobs

def extract_job_companies(soup):
    companies = []
    for div_tag in soup.find_all(name="div", attrs={"class":"row"}):
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

def extract_job_locations(soup):
    locations = []
    location_spans = soup.findAll(name="span", attrs={"class":"location"})
    for location_span in location_spans:
        locations.append(location_span.text.strip())
    return locations
