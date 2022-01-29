from api.api_selenium import *
from db.db_config import *

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def before_request():
    print('brefor_request_API')
    g.db = get_db()


def selenium_execute():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.naver.com")
    todayInterestingArticle = driver.find_element(
        By.XPATH, '//*[@id=\"themecast\"]/div[1]/div[1]/div[1]/strong').text

    # print("before find search box")
    # searchBox = driver.find_element_by_id(
    #     "query").send_keys("노써치" + Keys.ENTER)
    # print('searchBox => ', searchBox)
    # webdriver.ActionChains(driver).key_down(
    #     Keys.CONTROL).send_keys("a").perform()
    return store_selenium_result(todayInterestingArticle)


def after_request(response):
    return response
