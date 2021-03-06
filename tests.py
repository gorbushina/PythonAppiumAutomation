from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait



class Tests:
    driver = None

    def setup(self):
        capabilities = {
            "platformName": "Android",
            "deviceName": "AndroidTestDevice",
            "platformVersion": "8.1",
            "automationName": "Appium",
            "appPackage": "org.wikipedia",
            "appActivity": ".main.MainActivity",
            "app": "/Users/ekaterinagorbusina/PycharmProjects/PythonAppiumAutomation/apks/org.wikipedia.apk",
            "newCommandTimeout": "300"}

        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)

    def teardown(self):
        self.driver.quit()

    def wait_for_element_present(self, by, error_message, timeout_in_seconds=5):
        wait = WebDriverWait(driver=self.driver, timeout=timeout_in_seconds)
        return wait.until(method=ec.presence_of_element_located(by), message=error_message)

    def wait_for_elements_present(self, by, error_message, timeout_in_seconds=5):
        wait = WebDriverWait(driver=self.driver, timeout=timeout_in_seconds)
        return wait.until(method=ec.presence_of_all_elements_located(by), message=error_message)

    def wait_for_element_not_present(self, by, error_message, timeout_in_seconds=5):
        wait = WebDriverWait(driver=self.driver, timeout=timeout_in_seconds)
        return wait.until(method=ec.invisibility_of_element_located(by), message=error_message)

    def wait_for_element_and_click(self, by, error_message, timeout_in_seconds=5):
        element = self.wait_for_element_present(by, error_message, timeout_in_seconds)
        element.click()
        return element

    def wait_for_element_and_send_keys(self, by, value, error_message, timeout_in_seconds=5):
        element = self.wait_for_element_present(by, error_message, timeout_in_seconds)
        element.send_keys(value)
        return element

    def wait_for_element_and_clear(self, by, error_message, timeout_in_seconds=5):
        element = self.wait_for_element_present(by, error_message, timeout_in_seconds)
        element.clear()
        return element

    def assert_element_has_text(self, by, error_message, text, error_text, timeout_in_seconds=5):
        element = self.wait_for_element_present(by, error_message, timeout_in_seconds)
        assert element.get_attribute('text') == text, error_text

    def swipe_up(self, time_of_swipe):
        actions = TouchAction(self.driver)
        size = self.driver.get_window_size()
        x = int(size["width"] / 2)
        start_y = int(size["height"] * 0.8)
        end_y = int(size["height"] * 0.2)
        actions.press(x=x, y=start_y).wait(time_of_swipe).move_to(x=x, y=end_y).release()
        actions.perform()

    def swipe_up_quick(self):
        self.swipe_up(200)

    def swipe_up_to_find_element(self, by, error_message):
        while len(self.driver.find_elements(by=by[0], value=by[1])) == 0:
            self.swipe_up_quick()


    def test_first(self):
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'Search Wikipedia')]"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value='Java',
            error_message='Cannot find element search')

        self.wait_for_element_present(
            by=[AppiumBy.XPATH,
                "//*[@resource-id='org.wikipedia:id/page_list_item_description' and @text='Object-oriented programming language']"],
            error_message='Cannot find General-purpose programming language searching by Python',
            timeout_in_seconds=15)

    def test_cancel(self):
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.ID, "org.wikipedia:id/search_container"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value='Java',
            error_message='Cannot find element search')

        self.wait_for_element_and_clear(by=[AppiumBy.ID, "org.wikipedia:id/search_src_text"],
                                        error_message="Cannot find search field")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[@resource-id='org.wikipedia:id/search_toolbar']"
                                                            "/*[@class='android.widget.ImageButton']"],
                                        error_message="Cannot find ARROW to go back")

        self.wait_for_element_not_present(by=[AppiumBy.XPATH, "//*[@resource-id='org.wikipedia:id/search_toolbar']"
                                                              "/*[@class='android.widget.ImageButton']"],
                                          error_message="ARROW is still on page")

    def test_compare_article_title(self):
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'Search Wikipedia')]"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value='Java',
            error_message='Cannot find element search')

        self.wait_for_element_and_click(
            by=[AppiumBy.XPATH,
                "//*[@resource-id='org.wikipedia:id/page_list_item_description' and @text='Object-oriented programming language']"],
            error_message="Cannot find element skip button")

        element = self.wait_for_element_present(
            by=[AppiumBy.XPATH, "//android.view.View[@content-desc='Java (programming language)']"],
            error_message="Cannot find element Java definition")
        assert element.get_attribute('content-desc') == 'Search Wikipedia', "We see unexpected text"

    def test_check_placeholder_text(self):
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.assert_element_has_text(
            by=[AppiumBy.XPATH, "//*[@resource-id='org.wikipedia:id/search_container']/*[@index=1]"],
            error_message="Cannot find element search input",
            text='Search Wikipedia',
            error_text="We see unexpected text")

    def test_cancel_search(self):
        find_article = "Mozart"
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'Search Wikipedia')]"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value=find_article,
            error_message='Cannot find element search')

        elements = self.wait_for_elements_present(by=[AppiumBy.XPATH, f"//*[contains(@text, '{find_article}')]"],
                                                  error_message="No results")

        assert len(elements) > 1, "Less than 1"


    def test_check_words(self):
        find_article = "Java"
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'Search Wikipedia')]"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value=find_article,
            error_message='Cannot find element search')

        elements = self.wait_for_elements_present(by=[AppiumBy.XPATH, f"//*[contains(@text, '{find_article}')]"],
                                                  error_message="No results")

        for i in elements:
            assert i.get_attribute('text').startswith("Java"), "No Java in article"

    def test_swipe_article(self):
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'Search Wikipedia')]"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value='Appium',
            error_message='Cannot find Search Wikipedia input')

        self.wait_for_element_and_click(
            by=[AppiumBy.XPATH,
                "//*[@resource-id='org.wikipedia:id/page_list_item_title' and @text='Appium']"],
            error_message="Cannot find Appium article")

        self.wait_for_element_present(
            by=[AppiumBy.XPATH, "//android.view.View[@content-desc='Automation for Apps']"],
            error_message="Cannot find element Appium definition")

        self.swipe_up_to_find_element(
            by=[AppiumBy.XPATH, "//*[contains(@content-desc,'View article in browser')]"],
            error_message="Test error message")

    def test_save_first_article_to_my_list(self):
        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'SKIP')]"],
                                        error_message="Cannot find element skip button")

        self.wait_for_element_and_click(by=[AppiumBy.XPATH, "//*[contains(@text, 'Search Wikipedia')]"],
                                        error_message="Cannot find element search input")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.XPATH, "//*[contains(@resource-id, 'org.wikipedia:id/search_src_text')]"],
            value='Java',
            error_message='Cannot find element search')

        self.wait_for_element_and_click(
            by=[AppiumBy.XPATH,
                "//*[@resource-id='org.wikipedia:id/page_list_item_description' and @text='Object-oriented programming language']"],
            error_message="Cannot find element skip button")

        self.wait_for_element_and_click(
            by=[AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.LinearLayout[2]/android.widget.TextView[1]"],
            error_message="Cannot find element SAVE ARTICLE")

        self.wait_for_element_and_click(
            by=[AppiumBy.ID, "org.wikipedia:id/snackbar_action"],
            error_message="Cannot find element to add to the list")

        self.wait_for_element_and_send_keys(
            by=[AppiumBy.ID, "org.wikipedia:id/text_input"],
            value='Learning programming',
            error_message='Cannot put text into articles folder input')

        self.wait_for_element_and_click(
            by=[AppiumBy.XPATH, "//*[contains(@text, 'OK')]"],
            error_message='Cannot find OK button')

        self.wait_for_element_and_click(
            by=[AppiumBy.XPATH, "//*[@resource-id='org.wikipedia:id/search_toolbar']"
                                "/*[@class='android.widget.ImageButton']"],
            error_message="Cannot find ARROW to go back")
