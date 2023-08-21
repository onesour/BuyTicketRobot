import configparser

import ddddocr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ticket_producer_url = "https://www.globalinterpark.com/detail/edetail?prdNo=23010177&dispNo=01003"

config = configparser.ConfigParser()
config.read("./config_interpark.ini")
user_email = config['user']['email']
user_pwd = config['user']['password']

driver_option = Options()
driver_option.add_argument("--disable-notifications")

driver_option.add_experimental_option("detach", True)  # Not close browser when code is done.
chrome_driver = webdriver.Chrome(options=driver_option)
chrome_driver.maximize_window()
chrome_driver.get(ticket_producer_url)


def login_interpark():
    login_btn_xpath = '/html/body/div[2]/div/div/ul/li[2]/a'
    hint_btn = chrome_driver.find_element(By.XPATH, login_btn_xpath)
    hint_btn.click()

    EMAIL_ID = 'memEmail'
    email_input = chrome_driver.find_element(By.ID, EMAIL_ID)
    email_input.send_keys(user_email)
    PASSWORD_ID = 'memPass'
    pwd_input = chrome_driver.find_element(By.ID, PASSWORD_ID)
    pwd_input.send_keys(user_pwd)

    LOGIN_ID = "sign_in"
    login_btn = chrome_driver.find_element(By.ID, LOGIN_ID)
    login_btn.click()


def check_element_located(xpath, try_time=1):
    try:
        WebDriverWait(chrome_driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        print(e)
    finally:
        if try_time >= 3:
            raise Exception("Try time max.")
        try_time += 1
        check_element_located(xpath, try_time)


def switch_to_booking():
    product_frame_id = 'product_detail_area'
    booking_btn = '/html/body/div/div/div[1]/div[2]/div[3]/div[2]/div[2]/img'
    WebDriverWait(chrome_driver, 5).until(EC.visibility_of_element_located((By.ID, product_frame_id)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.ID, product_frame_id))
    WebDriverWait(chrome_driver, 5).until(EC.visibility_of_element_located((By.XPATH, booking_btn)))
    booking_btn_elm = chrome_driver.find_element(By.XPATH, booking_btn)
    booking_btn_elm.click()
    original_window = chrome_driver.current_window_handle
    for window_handle in chrome_driver.window_handles:
        if window_handle != original_window:
            chrome_driver.switch_to.window(window_handle)
            break


def select_date_and_next():
    pick_date_xpath = 'ifrmBookStep'
    WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.ID, pick_date_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.ID, pick_date_xpath))
    date_table_xpath = '/html/body/div/div[1]/div[2]/table'
    date_table_elm = chrome_driver.find_element(By.XPATH, date_table_xpath)
    date_tds = date_table_elm.find_elements(By.TAG_NAME, "td")
    for td in date_tds:
        try:
            date_herf = td.find_element(By.TAG_NAME, "a")
            date_herf.click()
            break
        except Exception as e:
            print(type(e))
    chrome_driver.switch_to.default_content()
    next_btn_xpath = '//*[@id="LargeNextBtn"]'
    WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_btn_xpath)))
    next_btn_elm = chrome_driver.find_element(By.XPATH, next_btn_xpath)
    next_btn_elm.click()


def save_image():
    content_frame_xpath = '//*[@id="ifrmSeat"]'
    WebDriverWait(chrome_driver, 10).until(EC.visibility_of_element_located((By.XPATH, content_frame_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, content_frame_xpath))
    recognize_img_xpath = '//*[@id="imgCaptcha"]'
    img_item = chrome_driver.find_element(By.XPATH, recognize_img_xpath)
    src = img_item.get_attribute("src")
    ocr = ddddocr.DdddOcr()
    with open("s.jpg", "wb") as img_file:
        img_file.write(img_item.screenshot_as_png)
    res = ocr.classification(img_item.screenshot_as_png)
    input_recog_xpath = '//*[@id="txtCaptcha"]'
    WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_recog_xpath)))
    input_recog_elm = chrome_driver.find_element(By.XPATH, input_recog_xpath)
    input_recog_elm.click()
    input_recog_elm.send_keys(res)
    complete_btn_xpath = '//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]'
    complete_btn_elm = chrome_driver.find_element(By.XPATH, complete_btn_xpath)
    complete_btn_elm.click()


if __name__ == '__main__':
    login_interpark()
    switch_to_booking()
    select_date_and_next()
    save_image()
