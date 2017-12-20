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
    locations = []
    for div_tag in listings:
        for location_span in div_tag.find_all(name="span", attrs={"class":"location"}):
            locations.append(location_span.text.strip())
    return locations
