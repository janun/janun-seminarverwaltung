from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from backend.users.models import User


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_signup(self):
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/signup/"))
        self.assertIn("Neues Konto anlegen", self.selenium.title)
        name_input = self.selenium.find_element_by_name("name")
        name_input.send_keys("Max Mustermann")
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys("max@mustermann.com")
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("max")
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys("ohtugh3P")
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys("ohtugh3P")
        checkbox1_input = self.selenium.find_element_by_name("data_protection_read")
        checkbox1_input.click()
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.assertIn("Übersicht", self.selenium.title)

    def test_login(self):
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/login/"))
        self.assertIn("Anmelden", self.selenium.title)
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys("testuser")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("secret")
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.assertIn("Übersicht", self.selenium.title)
