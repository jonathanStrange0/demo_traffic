from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class BrowserBot():
    def __init__(self, url=None):
        self.url = url
        self.opts = Options()
        self.opts.headless = True
        self.browser = Firefox(keep_alive=False, options=self.opts)#,\
                                # executable_path='../vendor/geckodriver/geckodriver')
        self.browser.get(self.url)
        self.browser.close()
