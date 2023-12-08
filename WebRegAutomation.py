import time
import datetime
import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

class WebRegAutomation:
    def __init__(self, headless):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--log-level=3")
        if headless:
            self.chrome_options.add_argument("--headless")  # Ensure GUI is off
            self.chrome_options.add_argument("--no-sandbox")
            self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = selenium.webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def click_button_by_xpath(self, xpath):
        try:
            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
            return True
        except NoSuchElementException:
            print("Button not found.")
            return False
        except ElementClickInterceptedException:
            print("Button could not be clicked.")
            return False

    def wait_for_url(self, url, timeout=2):
        try:
            self.wait.until(EC.url_to_be(url))
            return True
        except TimeoutException:
            return False

    @staticmethod
    def print_with_timestamp(message):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"{time_str} {message}")

    def find_text_on_page(self, search_text):
        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '{}')]".format(search_text))
        return len(elements) > 0

    def login(self, username, password, login_url):
        self.driver.get(login_url)
        username_element = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_element = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div[2]/div[1]/div[2]/form/input[4]')))
        username_element.send_keys(username)
        password_element.send_keys(password)
        self.print_with_timestamp('Logging into WebReg')
        login_button.click()
        if(self.find_text_on_page('Invalid credentials.')):
            self.print_with_timestamp('Invalid Web Reg Credentials')
            return False
        return True
    
    def get_duo(self):
        self.print_with_timestamp('Complete Duo 2fa')
        while(not self.check_exists_by_xpath('//*[@id="trust-browser-button"]')):
            time.sleep(0.5)

        self.print_with_timestamp('Duo Accepted')
        self.click_button_by_xpath('//*[@id="trust-browser-button"]')
    
    def webreg_loading(self):
        desired_url = "https://sims.rutgers.edu/webreg/chooseSemester.htm?login=cas"
        while not self.wait_for_url(desired_url):
            self.print_with_timestamp("Waiting for Web Reg")

        self.print_with_timestamp("Web Reg Loaded")
    
    def timeout_activity(self):
        self.driver.get("https://sims.rutgers.edu/webreg/chooseSemester.htm?login=cas")
    
    def class_registration(self,semesterID, classIndex):
        registrationLink = f'https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection={semesterID}&indexList={classIndex}'

        self.driver.get(registrationLink)
        self.print_with_timestamp("Class Code Loaded")

        self.print_with_timestamp("Trying to Register: " + classIndex)
        self.click_button_by_xpath('//*[@id="submit"]')

        if(self.find_text_on_page('Your request is being processed')):
            while(not self.find_text_on_page("Registered Courses")):
                self.print_with_timestamp("Waiting for Request to be Processed")
                time.sleep(1.5)

        if(self.find_text_on_page("Input a special permission number if you have it")):
            self.print_with_timestamp("SPN Required To Register")
            self.print_with_timestamp("Stopping Registration")
        else:
            css_selector = ".info ul"

            # Find the <ul> element within the specified class
            ul_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            # Now you can interact with the ul_element or retrieve its content
            # For example, getting text from each <li> element inside the <ul>

            list_items = ul_element.find_elements(By.TAG_NAME, "li")
            for item in list_items:
                self.print_with_timestamp(f"Registration Result: {item.get_attribute('class')}")
                if(item.get_attribute('class') == 'error'):
                    self.print_with_timestamp(f"Reason for Failure: {item.text}")
                    return False
                elif(item.get_attribute('class') == 'ok'):
                    self.print_with_timestamp(f"{item.text}")
                    return True

