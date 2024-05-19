import time
import threading
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from app.config import TestConfig
from app.models import User, StudyGroup

localHost = "http://localhost:5000/"

class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testApp = create_app(TestConfig)
        cls.app_context = cls.testApp.app_context()
        cls.app_context.push()
        cls.db = db
        cls.db.create_all()

        cls.server_thread = threading.Thread(target=cls.testApp.run)
        cls.server_thread.start()
        time.sleep(1)  # Ensure the server has time to start

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(localHost)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.db.session.remove()
        cls.db.drop_all()
        cls.app_context.pop()

        cls.server_thread.join()

    def test_signup(self):
        self.driver.get(f"{localHost}signup")
        
        emailElement = self.driver.find_element(By.ID, "email")
        emailElement.send_keys("test@example.com")

        studentNumberElement = self.driver.find_element(By.ID, "studentnumber")
        studentNumberElement.send_keys("12345678")

        usernameElement = self.driver.find_element(By.ID, "username")
        usernameElement.send_keys("testuser")

        passwordElement = self.driver.find_element(By.ID, "password")
        passwordElement.send_keys("password")

        confirmPasswordElement = self.driver.find_element(By.ID, "confirmpassword")
        confirmPasswordElement.send_keys("password")

        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()

        successMessage = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )
        self.assertIn("Account created successfully!", successMessage.text)

    