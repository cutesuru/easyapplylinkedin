from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import json

class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.cap = DesiredCapabilities().FIREFOX
        self.cap["marionette"] = False
        self.driver = webdriver.Firefox(capabilities=self.cap, executable_path="F:\\automaate\\geckodriver.exe")

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element_by_name('session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element_by_name('session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
    
    def job_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""

        # go to Jobs
        self.driver.get("https://www.linkedin.com/jobs")

        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element_by_css_selector(".jobs-search-box__text-input[aria-label='Search by title, skill, or company']")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element_by_css_selector(".jobs-search-box__text-input[aria-label='City, state, or zip code']")
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)
        time.sleep(10)

    def filter(self):
        """This function filters all the job results by 'Easy Apply'"""

        # select all filters, click on Easy Apply and apply the filter
        all_filters_button = self.driver.find_element_by_xpath("//button[@aria-label='All filters']")
        all_filters_button.click()
        time.sleep(1)
        easy_apply_button = self.driver.find_element_by_xpath("//button[@aria-label='Easy Apply filter.']")
        easy_apply_button.click()
        time.sleep(1)
        #apply_filter_button = self.driver.find_element_by_xpath("//button[@data-control-name='all_filters_apply']")
        #apply_filter_button.click()

    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(total_results_int)

        time.sleep(2)
        # get results for the first page
        current_page = self.driver.current_url
        results=self.driver.find_elements_by_css_selector(".job-card-container--clickable")
        #results = self.driver.find_elements_by_class_name("jobs-search-results__list-item occludable-update p0 relative ember-view")
        print(results) 
        # for each job add, submits application if no questions asked
        i=0
        for result in results:
            try:
                print(f'called')
                result.click()
                time.sleep(2)
                in_apply = self.driver.find_element_by_css_selector(".jobs-apply-button")
                in_apply.click()
                time.sleep(2)
                print("Apply Section")
                next_button = self.driver.find_element_by_css_selector("footer button")
                time.sleep(2)
                review_button=self.driver.find_element_by_class_name("artdeco-button--primary")
                if review_button.get_attribute("data-control-name")=="continue_unify":
                	close_button=self.driver.find_element_by_class_name("artdeco-modal__dismiss")
                	close_button.click()
                	time.sleep(2)
                	discard_button=self.driver.find_element_by_xpath("//button[contains(@class,'artdeco-button')]//*[contains(.,'Discard')]/..")
                	discard_button.click()
                	print("Complex application, skipped..")
                	continue
                else:
                	review_button.click()
                	time.sleep(2)
                	submit_button=self.driver.find_element_by_class_name("artdeco-button--primary")
                	if submit_button.get_attribute("data-control-name")=="submit_unify":
                		submit_button.click()
                		time.sleep(2)
                		close_button=self.driver.find_element_by_class_name("artdeco-modal__dismiss")
                		close_button.click()

                	else:
                		close_button=self.driver.find_element_by_class_name("artdeco-modal__dismiss")
                		close_button.click()
                		time.sleep(2)
                		discard_button=self.driver.find_element_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
                		discard_button.click()
                		print("Complex application, skipped..")
                		continue

            except NoSuchElementException:
            		print(f"No application button for {i} ,skipped..")
            		continue
        self.close_session()    		

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()


if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)
    print(data)
    bot = EasyApplyLinkedin(data)
    bot.apply()