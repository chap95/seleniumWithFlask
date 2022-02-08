import os
from typing import List

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

PPOMPPU = 'https://www.ppomppu.co.kr/'


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    def __repr__(self) -> str:
        return '<Result %r>' % self.description


@app.route('/hello')
def hello():
    return 'Hello, World!'


def printList(value):
    print('value => ', value)


@app.route('/selenium')
def selenium_execute():
    service = ChromeService(
        executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(PPOMPPU)
    result = []
    filterList = ['[', ']', '/']
    shoppingTabList = driver.find_elements(By.ID, 'shopping-tab1_list')
    for shoppingTab in shoppingTabList:
        coupons: List[WebElement] = shoppingTab.find_elements(
            By.CLASS_NAME, 'ppom_coupon')
        for coupon in coupons:
            aTag: WebElement = coupon.find_element(By.XPATH, '..')
            text = aTag.text
            for filterIndex in range(len(filterList)):
                text = text.replace(filterList[filterIndex], '')
            result.append(text)

    return '/'.join(result)

# def create_app(test_config=None):
#     db.create_all()
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )

#     if test_config is None:
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         app.config.from_mapping(test_config)

#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     @app.route('/hello')
#     def hello():
#         return 'Hello, World!'

#     @app.route('/selenium')
#     def selenium_execute():
#         service = ChromeService(
#             executable_path=ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service)
#         driver.get("https://www.naver.com")
#         todayInterestingArticle = driver.find_element(
#             By.XPATH, '//*[@id=\"themecast\"]/div[1]/div[1]/div[1]/strong').text
#         result1 = Result(description=todayInterestingArticle)
#         print('result1 => ', result1)
#         print("before find search box")
#         searchBox = driver.find_element_by_id(
#             "query").send_keys("노써치" + Keys.ENTER)
#         print('searchBox => ', searchBox)
#         webdriver.ActionChains(driver).key_down(
#             Keys.CONTROL).send_keys("a").perform()
#         return todayInterestingArticle
#     return app
