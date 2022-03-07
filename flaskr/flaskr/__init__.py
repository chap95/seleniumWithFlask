from logging import error
import os
import re
from threading import Thread
import time
from typing import List

from flask import Flask, g, jsonify
from flask_sqlalchemy import SQLAlchemy

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.orm.session import Session
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from flask_migrate import Migrate
from flaskr.api import bp

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

app.register_blueprint(bp, url_prefix='/api')

PPOMPPU = 'https://www.ppomppu.co.kr/'


class Result(db.Model):
    __tablename__ = 'Result'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    def __init__(self, description=None):
        self.description = description

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
    try:
        for shoppingTab in shoppingTabList:
            coupons: List[WebElement] = shoppingTab.find_elements(
                By.CLASS_NAME, 'ppom_coupon')
            hrefList = []
            for coupon in coupons:
                # coupon.find_element(By.XPATH, '..')
                # coupon: WebElement = WebDriverWait(driver, 3).until(
                #     EC.presence_of_element_located(coupon))
                aTag: WebElement = coupon.find_element(By.XPATH, '..')
                text = aTag.text
                for filterIndex in range(len(filterList)):
                    text = text.replace(filterList[filterIndex], '')
                result.append(text)
                href = aTag.get_attribute('href')
                hrefList.append(href)
                # driver.get(href)
                # try:
                #     link = driver.find_element(By.CLASS_NAME, 'wordfix')
                #     if(link):
                #         print('link => ', link.text)
                # except NoSuchElementException:
                #     pass
                # print('link => ', link)

                # driver.back()

            print('hrefList => ', hrefList)
            for href in hrefList:
                driver.get(href)
                try:
                    link = driver.find_element(By.CLASS_NAME, 'wordfix')
                    if(link):
                        print('link => ', link.text)
                except NoSuchElementException:
                    pass

    except NoSuchElementException:
        print('error => NoSuchElementException')
        pass
    except(RuntimeError):
        print('error => ', RuntimeError)
        driver.quit()

    for resultTextIndex in range(len(result)):
        data = Result(description=result[resultTextIndex])
        print('data => ', data)
        db.session.add(data)
        db.session.commit()

    driver.quit()
    return '/'.join(result)


@app.route('/getResult')
def get_result():
    data = []
    getQuery = db.session.query(Result.description)
    result = getQuery.all()
    for row in result:
        text = str(row)
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('\'', '')
        text = text.replace(',', '')
        if(len(text) > 0):
            data.append({'text': text})

    print('data -> ', jsonify(data))
    return jsonify(data)

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
