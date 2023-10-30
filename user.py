import sched
import time

from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from misc.logger import log, alert
from models import Player
from butler import error

class Client:
    def __init__(self, name, email, password):
        self.name = name

        self.player = None

        self.email = email
        self.password = password

        self.driveroptions = {'headless': True, 'binary_location': None}
        self.s = None
        self.driver = None
        self.wait = None

        self.perkoptions = {'goldperks': None, 'eduweight':0, 'goldweight':0, 'minlvl4gold':999}

        self.statedept = None

    def set_driveroptions(self, element, value):
        self.driveroptions[element] = value

    def set_perkoptions(self, element, value):
        self.perkoptions[element] = value

    def set_statedept(self, value):
        self.statedept = value

    def boot_browser(self):
        try:
            print(f"Booting browser for {self.name}...")
            options = FirefoxOptions()
            if self.driveroptions['headless'] or not self.driveroptions['binary_location']:
                options.add_argument('--headless')
            else:
                options.binary_location = self.driveroptions['binary_location']
            self.driver = Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        except Exception as e:
            error(self, e, 'Error setting up Firefox driver')
            return False

        try:
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.get('https://rivalregions.com')

            email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='mail']")))
            email_input.send_keys(self.email)
            log(self, 'Logging in...')

            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='p']")
            password_input.send_keys(self.password)

            submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[name='s']")
            submit_button.click()

            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#chat_send")))
            time.sleep(1)
            return True
        except Exception as e:
            error(self, e, 'Error logging in, check your credentials')
            self.driver.quit()
            time.sleep(2)
            self.wait = None
            self.driver = None
            return False
    
    def initiate_session(self):
        self.s = sched.scheduler(time.time, time.sleep)
        if self.boot_browser():
            self.id = self.driver.execute_script("return id;")
            self.player = Player(self.id)
            return True

    def __del__(self):
        if self.driver:
            self.driver.quit()
        self.s = None
        self.driver = None