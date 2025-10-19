class BasePage:
    url = None

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        self.driver.get(self.url)

    def get_current_url(self):
        get_url = self.driver.current_url

    def assert_word(self, word, result):
        value_word = word.text
        assert value_word == result

    def assert_url(self, result):
        get_url = self.driver.current_url
        assert get_url == result
