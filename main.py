import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ticket_producer_url = "https://tixcraft.com/"


def print_hi(name):
    print(f'Hi, {name}')


def test_selenium():
    xpath_by = "xpath"
    driver_option = Options()
    driver_option.add_argument("--disable-notifications")

    chrome = webdriver.Chrome("./chromedriver.exe", chrome_options=driver_option)
    chrome.get(ticket_producer_url)
    close_hint_btn_xpath = '//*[@id="board"]/img[3]'
    hint_btn = chrome.find_element(xpath_by, close_hint_btn_xpath)
    hint_btn.click()

    login_btn_xpath = '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div/ul/li[3]/a'
    login_btn = chrome.find_element(xpath_by, login_btn_xpath)
    login_btn.click()

    fb_login = "loginFacebook"
    WebDriverWait(chrome, 20).until(EC.element_to_be_clickable((By.ID, fb_login)))
    fb_login_btn = chrome.find_element("id", fb_login)
    fb_login_btn.click()

    email = chrome.find_element(By.ID, "email")
    email.send_keys("")
    passwd = chrome.find_element(By.ID, "pass")
    passwd.send_keys("")
    login_btn = chrome.find_element(By.ID, "loginbutton")
    login_btn.click()
    time.sleep(60)


if __name__ == '__main__':
    print_hi('PyCharm')
    test_selenium()
