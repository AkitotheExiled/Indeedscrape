import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class Indeed:


    def __init__(self):

        self.driver = webdriver.Chrome()
        self.job = None
        print('Type the location you want to search for( e.g. San Mateo, CA)')
        self.location = input()
        self.scraped_data = []
        self.url = 'https://www.indeed.com'
        self.wait = WebDriverWait(self.driver, 10)

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

    def is_element_here(self, path, element):

        pass

    def browse_web(self):

        self.driver.get(self.url)
        time.sleep(10)

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

    def scrape_page(self):

        try:
            # containers = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")))
            # containers = self.driver.find_elements_by_xpath("//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")
            containers = self.driver.find_elements_by_xpath(
                "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]"
            )
        except NoSuchElementException:
            print('A certain element cannot be found.')
        else:
            for title in containers:
                job_name = title.find_element_by_class_name('title').text
                job_link = title.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
                company = title.find_element_by_class_name('company').text
                location = title.find_element_by_class_name('location').text
                self.scraped_data.append(
                    {"Job": job_name, "Job Link": job_link, "Company": company,
                     "Location": location}
                )

    def save_jobs(self):

        df = pd.DataFrame(self.scraped_data)
        print("data saved...")
        df.to_csv('indeedJobs.csv')
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
            if not self.job:
                break
            self.search_job()
            self.scrape_page()
        self.save_jobs()


if __name__ == "__main__":
    Srch = Indeed()
    Srch.run_logic()
