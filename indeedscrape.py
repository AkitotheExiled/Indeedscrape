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
            self.soup = self.driver.page_source
            for title in containers:
                job_name = title.find_element_by_class_name('title').text
                job_link = title.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute(
                    'href')
                company = title.find_element_by_class_name('company').text
                location = title.find_element_by_class_name('location').text
                self.scraped_data.append(
                    {"Job": job_name, "Job Link": job_link, "Company": company,
                     "Location": location}
                )

        #else:
         ##  'The element you are looking for is not available.  Pre-Check is returning false. Please confirm your element is visible.')
        print(self.driver.current_url)
        print(BeautifulSoup(self.driver.page_source, 'html.parser').prettify())

    def save_jobs(self):

        df = pd.DataFrame(self.scraped_data)
        print("Scraped jobs saved to " + self.filename + '.')
        df.to_csv(self.filename)
        self.driver.quit()

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


if __name__ == "__main__":
    Srch = Indeed()
    Srch.run_logic()
