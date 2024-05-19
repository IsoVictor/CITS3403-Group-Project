import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from unittest import TestCase
from selenium.webdriver.support import expected_conditions as EC

from app import create_app, db
from app.config import TestConfig


localHost = "http://localhost:5000/"
multiprocessing.set_start_method("fork")

class SeleniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.close()

    def test_a_signup(self):
        self.driver.get(f"{localHost}signup")
        
        loginelement = self.driver.find_element(By.ID, "email")
        loginelement.send_keys("test@example.com")

        loginelement = self.driver.find_element(By.ID, "studentnumber")
        loginelement.send_keys("12345678")

        loginelement = self.driver.find_element(By.ID, "username")
        loginelement.send_keys("testuser")

        passwologinelementrdElement = self.driver.find_element(By.ID, "password")
        passwologinelementrdElement.send_keys("password")

        loginelement = self.driver.find_element(By.ID, "confirmpassword")
        loginelement.send_keys("password")

        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        successMessage = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.assertIn("Account created successfully!", successMessage.text)

    def test_b_login(self):
        self.driver.get(f"{localHost}login")

        # Wait for the login form elements to be visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )

        loginelement = self.driver.find_element(By.ID, "username")
        loginelement.send_keys("testuser")

        loginelement = self.driver.find_element(By.ID, "password")
        loginelement.send_keys("wrongpassword")

        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        errorMessage = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        self.assertIn("No account found with username testuser", errorMessage.text)
