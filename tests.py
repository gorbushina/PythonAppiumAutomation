from appium import webdriver


class TestsFirst:

    driver=None


    def setup(self):
        capabilities ={
        "platformName": "Android",
        "deviceName": "AndroidTestDevice",
        "platformVersion": "8.1",
        "automationName": "Appium",
        "appPackage": "org.wikipedia",
        "appActivity": ".main.MainActivity",
        "app": "/Users/ekaterinagorbusina/PycharmProjects/PythonAppiumAutomation/apks/org.wikipedia.apk"}

        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", capabilities)

    def teardown(self):
        self.driver.quit()

    def test(self):
        print("First test run")

