import os

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    print(__name__)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/test')
    def test():
        service = ChromeService(
            executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get("https://www.naver.com")
        print("before find 오늘 읽을 만할 글")
        todayInterestingArticle = driver.find_element(
            By.XPATH, '//*[@id=\"themecast\"]/div[1]/div[1]/div[1]/strong').text

        print("todayInterestingArticle => ", todayInterestingArticle)
        print("before find search box")

        searchBox = driver.find_element_by_id(
            "query").send_keys("노써치" + Keys.ENTER)
        print('searchBox => ', searchBox)
        webdriver.ActionChains(driver).key_down(
            Keys.CONTROL).send_keys("a").perform()
        return '테스트 입니도'

    return app
