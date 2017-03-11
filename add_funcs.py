from time import sleep
from random import randint

def random_sleep(mini,maxi):
    sleep(randint(mini,maxi))

def extract_company(soup):
    try:
        company_name = soup.find('h1').get_text()
        company_name = company_name.strip()
    except:
        company_name = None
    try:
        employees = soup.find('p',attrs={'class':'company-main-info-company-descriptions'}).get_text()
        employees = employees.strip('\n')
    except:
        employees = None
    try:
        about_us = soup.find('p',attrs={'class':'org-about-us-organization-description__text'}).get_text()
        about_us = about_us.strip()
    except:
        about_us = None
    print(company_name,employees, about_us)
    return company_name, employees, about_us

def extract_people(soup):
    try:
        person_name = soup.find('h1').get_text()
        print(person_name)
    except:
        pass
    try:
        person_pos = soup.find('h2').get_text()
        print(person_pos)
    except:
        pass
    try:
        person_exp = soup.find('div',attrs={'class':'pv-top-card-section__experience'}).get_text()
        print(person_exp)
    except:
        pass
