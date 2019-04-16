import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time
import pandas as pd


class Indeed:
    def __init__(self):
        self.job = None
        self.driver = webdriver.Chrome(executable_path='C:\\chromedriver\\chromedriver.exe')
        self.url = 'https://www.indeed.com'
        print('Type the location you want to search for( e.g. San Mateo, CA)')
        self.location = input()
        self.scraped_data = []
        self.done = False
        self.wait = WebDriverWait(self.driver, 10)

    def ElementDetec(self,element1,element2):
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

    def BrowerOp(self):
        self.driver.get(self.url)
        time.sleep(10)

    def SearchJob(self):

        searchField = self.driver.find_element_by_id(self.ElementDetec('text-input-what','what'))
        searchWhere = self.driver.find_element_by_id(self.ElementDetec('text-input-where','where'))

        searchField.send_keys(Keys.CONTROL + "a")
        searchField.send_keys(Keys.DELETE)
        searchWhere.send_keys(Keys.CONTROL + "a")
        searchWhere.send_keys(Keys.DELETE)

        searchWhere.send_keys(self.location)
        searchField.send_keys(self.job)

        searchField.submit()

    def ScrapePage(self):
        try:
            #containers = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")))
            #containers = self.driver.find_elements_by_xpath("//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")
            containers = self.driver.find_elements_by_xpath("//div[contains(@class,'jobsearch-SerpJobCard unifiedRow row result clickcard')]")
        except NoSuchElementException:
            print('A certain element cannot be found.')
        for title in containers:
            job_name = title.find_element_by_class_name('title').text
            job_link = title.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
            company = title.find_element_by_class_name('company').text
            location = title.find_element_by_class_name('location').text
            self.scraped_data.append({"Job": job_name, "Job Link": job_link, "Company": company, "Location": location})




    def SaveJobs(self):

        df = pd.DataFrame(self.scraped_data)

        print("data saved...")
        df.to_csv('indeedJobs.csv')
        self.driver.quit()

    def CloseD(self):

        return self.driver.quit()

    def RunLogic(self):

        self.BrowerOp()

        while not self.done:
            if self.job == "":
                self.done = True
                break
            else:
                print("Enter the job you want to search( or press enter to stop searching).")
                self.job = input()
                self.SearchJob()
                self.ScrapePage()

        self.SaveJobs()


if __name__ == "__main__":
    Srch = Indeed()
    Srch.RunLogic()
