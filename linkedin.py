from selenium import webdriver
from bs4 import BeautifulSoup
from add_funcs import random_sleep, extract_company, extract_people
import re

desired_urls = re.compile('(.*\/company.*|.*\/in\/.*)')


class LinkedInBot(object):

    def __init__(self,username,password,db_name='linked.db'):
        self.user = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.linkedIn = 'https://www.linkedin.com'
        self.urls = []
        self.crawled_urls = []
        self.db_name = db_name

    def login(self):
        self.make_request(self.linkedIn)
        email_field = self.driver.find_element_by_id('login-email')
        password_field = self.driver.find_element_by_id('login-password')
        login_button = self.driver.find_element_by_id('login-submit')
        email_field.send_keys(self.user)
        password_field.send_keys(self.password)
        random_sleep(2,5)
        login_button.click()

    def extract_data_person_page(self):
        url, soup = self.make_soup()
        extract_people(soup)


    def make_request(self,url):
        try:
            self.driver.get(url)
            self.crawled_urls.append(url)
        except:
            self.crawled_urls.append(url)

    def make_soup(self):
        try:
            url = self.driver.current_url
            html = self.driver.page_source
            soup = BeautifulSoup(html,'lxml')
            return url, soup
        except:
            return None, None

    def extract_company_info(self):
        url, soup = self.make_soup()
        extract_company(soup)


    def extract_links(self):
        url, soup = self.make_soup()
        if soup != None:
            links = soup.find_all('a',href=True)
            for link in links:
                link = link['href']
                if link.startswith('https://www.linkedin.com'):
                    if link not in self.urls:
                        if link not in self.crawled_urls:
                            if desired_urls.match(link):
                                self.urls.append(link)
                elif link.startswith('/'):
                    link = '{}{}'.format(self.linkedIn,link)
                    if link not in self.urls:
                        if link not in self.crawled_urls:
                            if desired_urls.match(link):
                                self.urls.append(link)
                else:
                    pass

    def crawler(self):
        self.login()
        random_sleep(10,20)
        self.extract_links()
        while len(self.urls) > 0:
            try:
                url = self.urls.pop()
                self.make_request(url)
                random_sleep(20,30)
                if '/company' in self.driver.current_url:
                    try:
                        self.extract_company_info()
                    except:
                        pass
                if '/in/' in self.driver.current_url:
                    try:
                        self.extract_data_person_page()
                    except:
                        pass
                self.extract_links()
            except:
                continue
