# Use BS4 to parse html for the page and extract data for csv ( Running into issues where soup.select, [ ]
# soup.find, soup.findAll will only write to the first cell in the column.  Then no other descriptions are found for the rest of the rows in that same column.
# I can bring up the soup and confirm that the description can be pulled up on its own..
# Need to delete additional column headers when appending to already existing csv [X]
# Fix issue where appending additional jobs, there is an extra row after every appended job. [ ]
# Open each link and extract information pertaining to the job for the csv [ ]
# Develop function to check if file exists before writing the data to it, if exists [x]
# then append the data that is not already in the csv. [x]
# Allow script to go through the pages if they exist to scrape further than the first page [ ]
# Create GUI and EXE for script [ ]

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import os, sys
import numpy as np


class Indeed:

    def __init__(self):

        self.driver = webdriver.Firefox()
        self.job = None
        print('Type the location you want to search for( e.g. San Mateo, CA)')
        self.location = input()
        self.scraped_data = []
        self.url = 'https://www.indeed.com'
        self.wait_time = 10
        self.wait = WebDriverWait(self.driver, self.wait_time)
        self.soup = None
        self.filename = 'indeedJobs.csv'
        self.links = []
        self.sources = []
        self.soups = []
    def element_detect(self, element1, element2):
        ''' This method is to be used when you know the name of an input and its ID changes on a different page but that input function remains the same.'''
        try:
            self.driver.find_element_by_id(element1)
        except NoSuchElementException:
            try:
                self.driver.find_element_by_id(element2)
            except NoSuchElementException:
                return []
            return element2
        return element1

    def is_element_visible(self, element):
        ''' Checks if element is visible and returns boolean value.'''
        try:
            self.driver.find_element_by_xpath(element)
            return True
        except NoSuchElementException:
            return False

    def browse_web(self):

        self.driver.get(self.url)
        time.sleep(5)

    def search_job(self):

        search_field = self.driver.find_element_by_id(
            self.element_detect('text-input-what', 'what')
        )
        search_where = self.driver.find_element_by_id(
            self.element_detect('text-input-where', 'where')
        )

        search_field.send_keys(Keys.CONTROL + "a")
        search_field.send_keys(Keys.DELETE)
        search_where.send_keys(Keys.CONTROL + "a")
        search_where.send_keys(Keys.DELETE)
        search_where.send_keys(self.location)
        search_field.send_keys(self.job)
        search_field.submit()
        WebDriverWait(self.driver, self.wait_time)

    def pre_check(self):
        ''' Does exactly what webdriverwait().until(ec.blahblah) except with print statements and will wait indefinitely.'''
        while True:
            if self.is_element_visible(
                    "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]"):
                print('Visible...')
                break
            else:
                print('Not Visible...')
                WebDriverWait(self.driver, self.wait_time)
                continue
        return True

    def frame_active(self):
        ''' If the frame is not visible switch to default content'''
        frame = None
        frame_vis = False
        if not frame:
            frame = self.driver.current_window_handle
        if frame != self.driver.current_window_handle:
            self.driver.switch_to.default_content()
            frame_vis = True
        if frame_vis:
            return True
        else:
            return False

    def reg_default(self, regex, strg):
        compiled = re.compile(regex).search(strg)
        if compiled == None:
            return ""
        else:
            return compiled.group()
    def check_tags(self):
        pass
    def scrape_page(self):
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")))
        try:
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath("//body").click()
            # containers = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")))
            # containers = self.driver.find_elements_by_xpath("//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")
            containers = self.driver.find_elements_by_xpath(
                "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]"
            )
        except NoSuchElementException:
            raise
        except UnexpectedAlertPresentException:
            Alert(self.driver).dismiss()
        except StaleElementReferenceException:
            self.driver.switch_to.default_content()
            pass
        else:
            for title in containers:
                job_name = title.find_element_by_class_name('title').text
                job_link = title.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute(
                    'href')
                company = title.find_element_by_class_name('company').text
                location = title.find_element_by_class_name('location').text
                self.links.append(job_link)
                self.scraped_data.append(
                    {"Job": job_name, "Job Link": job_link, "Company": company,
                     "Location": location, "Desc": None, "Salary": None, 'Applied': None, 'Interview': None}
                )
            for source in self.links:
                self.driver.get(source)
                self.scraped_data[0]['Job Link'] = self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'icl-u-xs-hide icl-u-lg-block icl-u-lg-textCenter')]").find_element_by_tag_name(
                    'a').get_attribute('href')

                '''self.scraped_data[0]['Salary'] = self.reg_default(
                    r'[$]\d[\d|\W]{1,3}(\d*)', self.driver.find_element_by_xpath(
                        "//div[contains(@class, 'jobsearch-jobDescriptionText')]").text
                )
                '''
                self.sources.append(self.driver.page_source)
            for source in self.sources:
                self.soups.append(BeautifulSoup(source, 'html.parser'))
            for soup in self.soups:
                try:
                    #for item in soup.findAll('div', {'class': "jobsearch-jobDescriptionText"}):
                        #desc = item.text
                    self.scraped_data[0]['Desc'] = soup.select('#jobDescriptionText')
                    #self.scraped_data[0]['Salary'] = soup.find('div', {"class": 'icl-JobResult-salary'}).text
                    #self.scraped_data[0]['Company'] = soup.find('span', {'class': 'icl-JobResult-companyName'}).text
                    #self.scraped_data[0]['Location'] = soup.find('span', {'class': 'icl-JobResult-jobLocation'}).text
                    #self.scraped_data[0]['Job'] = soup.find('a', {'class', 'icl-JobResult-jobLink'}).text
                except AttributeError:
                    pass




    def save_jobs(self):
        df = pd.DataFrame(self.scraped_data, columns=['Company', 'Job', 'Desc', 'Job Link', 'Location', 'Salary', 'Applied', 'Interview'])
        if self.filename in os.listdir(os.path.dirname(sys.argv[0])):
            with open(self.filename, 'a', encoding='utf-8') as f:
                df.to_csv(f, encoding='utf-8')
                f.close()
            print("Scraped jobs appended to " + self.filename + '.')
        else:
            print("Scraped jobs saved to generated file " + self.filename + '.')
            df.to_csv(self.filename, encoding='utf-8')
            self.driver.quit()

    def clean_file(self):
        col_names = ['Company', 'Job', 'Desc', 'Job Link', 'Location', 'Salary', 'Applied', 'Interview']
        df1 = pd.read_csv(os.path.abspath(self.filename), names=col_names, encoding='utf-8')
        df2 = pd.DataFrame(df1)
        df2.reindex()
        #df = pd.DataFrame(np.sort(df1[['Company', 'Job', 'Desc', 'Job Link', 'Location', 'Salary']].values, 1)).drop_duplicates()

        df2.drop_duplicates(subset=['Company', 'Job'], keep='first', inplace=True)
        with open(self.filename, 'w', encoding='utf-8') as f:
            df2.to_csv(f, encoding='utf-8')
            f.close()
        print(self.filename + ' ' + 'has now been cleaned of duplicates.')


    def close_prog(self):

        return self.driver.quit()

    def run_logic(self):

        self.browse_web()
        while True:
            print(
                "Enter the job you want to search( or press enter to stop searching)."
            )
            self.job = input()
            WebDriverWait(self.driver, self.wait_time)
            if not self.job:
                break
            self.search_job()
            self.scrape_page()
        self.save_jobs()
        self.clean_file()
        self.close_prog()


if __name__ == "__main__":
    Srch = Indeed()
    Srch.run_logic()
