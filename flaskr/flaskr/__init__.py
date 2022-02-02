import os

from flask import Flask, g
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/selenium')
    def selenium_execute():
        service = ChromeService(
            executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.naver.com")
        todayInterestingArticle = driver.find_element(
            By.XPATH, '//*[@id=\"themecast\"]/div[1]/div[1]/div[1]/strong').text

        print("before find search box")
        searchBox = driver.find_element_by_id(
            "query").send_keys("노써치" + Keys.ENTER)
        print('searchBox => ', searchBox)
        webdriver.ActionChains(driver).key_down(
            Keys.CONTROL).send_keys("a").perform()
        return todayInterestingArticle
    return app
