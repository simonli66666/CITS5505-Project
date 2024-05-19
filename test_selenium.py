import unittest
import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask
from app import create_app, db
from app.setting import TestingConfig

localHost = "http://localhost:5000/"

def run_app():
    app = create_app(TestingConfig)
    app.run(use_reloader=False)

class StaticPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app_context = create_app(TestingConfig).app_context()
        cls.app_context.push()
        db.create_all()
        
        cls.server_process = multiprocessing.Process(target=run_app)
        cls.server_process.start()
        time.sleep(5)  # 增加等待时间确保服务器启动

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(localHost)
        cls.base_url = "http://localhost:5000"
        print("Server and browser setup complete")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server_process.terminate()
        cls.server_process.join()
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    def test_home_page_load(self):
        self.driver.get(self.base_url)
        self.assertIn("Tasty", self.driver.title)
        logo = self.driver.find_element(By.CSS_SELECTOR, "div.logo-image a img")
        self.assertTrue(logo.is_displayed())

    

    def test_login_popup(self):
        self.driver.get(self.base_url)
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "show_login"))
        )
        login_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login"))
        )
        username_field = self.driver.find_element(By.NAME, "username")
        self.assertTrue(username_field.is_displayed())

    def test_search_function(self):
        self.driver.get(self.base_url)
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_button = self.driver.find_element(By.CLASS_NAME, "recipe-search-btn")
        self.assertTrue(search_input.is_displayed())
        self.assertTrue(search_button.is_displayed())
    def test_search_box(self):
        self.driver.get(localHost)
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_button = self.driver.find_element(By.CLASS_NAME, "recipe-search-btn")
        self.assertTrue(search_input.is_displayed())
        self.assertTrue(search_button.is_displayed())

    def test_footer_copyright(self):
        self.driver.get(localHost)
        footer = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "copy"))
        )
        self.assertIn("© 2024 Liz. All Rights Reserved", footer.text)

    

if __name__ == "__main__":
    unittest.main()