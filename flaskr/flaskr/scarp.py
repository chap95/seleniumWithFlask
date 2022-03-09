from flask import Blueprint
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from typing import List
scrapBluePrint = Blueprint('scarp', __name__, url_prefix='/scrap')


PPOMPPU = 'https://www.ppomppu.co.kr/'


def getLegacy():
    from flaskr import Result
    from flaskr import db
    resultDescription = db.session.query(Result.description).all()
    descriptionList = []
    for row in resultDescription:
        text = str(row)
        text = text.replace('(', '')
        text = text.replace(')', '')
        text = text.replace('\'', '')
        text = text.replace(',', '')
        if(len(text) > 0):
            descriptionList.append({'description': text})

    return descriptionList


@scrapBluePrint.route('/ppomppu')
def ppomppu():
    from flaskr import Result
    from flaskr import db
    service = ChromeService(
        executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(PPOMPPU)
    result = {}
    textList = []
    linkList = []
    sum = 0
    filterList = ['[', ']', '/']
    descriptionList = getLegacy()
    print('### descriptionList => ', descriptionList)
    shoppingTabList = driver.find_elements(By.ID, 'shopping-tab1_list')
    try:
        for shoppingTab in shoppingTabList:
            coupons: List[WebElement] = shoppingTab.find_elements(
                By.CLASS_NAME, 'ppom_coupon')
            hrefList = []

            for coupon in coupons:
                aTag: WebElement = coupon.find_element(By.XPATH, '..')
                text = aTag.text
                for filterIndex in range(len(filterList)):
                    text = text.replace(filterList[filterIndex], '')

                if (text not in descriptionList):
                    textList.append(text)
                    href = aTag.get_attribute('href')
                    hrefList.append(href)

            print('hrefList => ', hrefList)
            for href in hrefList:
                driver.get(href)
                try:
                    link = driver.find_element(By.CLASS_NAME, 'wordfix')
                    if(link):
                        print('### append link => ', link.text)
                        linkList.append(link.text)
                except NoSuchElementException:
                    pass

    except NoSuchElementException:
        print('error => NoSuchElementException')
        pass
    except(RuntimeError):
        print('error => ', RuntimeError)
        driver.quit()

    for index in range(len(textList)):
        if(textList[index]):
            data = Result(description=textList[index])
            data = Result(link=linkList[index])
            print('data => ', data)
            db.session.add(data)
            db.session.commit()

    driver.quit()
    return '/'.join(result)
