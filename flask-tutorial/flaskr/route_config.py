from flask import Flask


from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
app = Flask(__name__)


@app.before_request
def before_request():
    print('brefor_request_API')


@app.route('/api/selenium')
def selenium():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.naver.com")
    print("before find 오늘 읽을 만할 글")
    todayInterestingArticle = driver.find_element(
        By.XPATH, '//*[@id=\"themecast\"]/div[1]/div[1]/div[1]/strong').text

    print("todayInterestingArticle => ", todayInterestingArticle)
    # print("before find search box")

    # searchBox = driver.find_element_by_id(
    #     "query").send_keys("노써치" + Keys.ENTER)
    # print('searchBox => ', searchBox)
    # webdriver.ActionChains(driver).key_down(
    #     Keys.CONTROL).send_keys("a").perform()
    return todayInterestingArticle


@app.after_request
def after_request(response):
    return response
