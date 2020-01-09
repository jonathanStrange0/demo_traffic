from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class BrowserBot():
    def __init__(self, url=None):
        self.url = url
        self.opts = Options()
        self.opts.headless = True
        self.browser = Firefox(options=self.opts)
        self.browser.get(self.url)