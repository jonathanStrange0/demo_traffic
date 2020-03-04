from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from faker import Faker

class BrowserBot():
    def __init__(self, url=None):
        self.url = url
        self.opts = Options()
        self.opts.headless = True
        self.profile = FirefoxProfile()
        self.user_agent = Faker().firefox()
        self.profile.set_preference("general.useragent.override", self.user_agent)

        self.browser = Firefox(keep_alive=False, options=self.opts,firefox_profile=self.profile)#,\
                                # executable_path='../vendor/geckodriver/geckodriver')

        self.browser.get(self.url)
        self.browser.quit()
