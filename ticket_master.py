import configparser
import time

# import pytesseract
# from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

ticket_producer_url = "https://tixcraft.com/activity/detail/22_WuBaiOPR"

# config_filepath = os.path.dirname()
config = configparser.ConfigParser()
config.read("./config.ini")
user_email = config['user']['email']
user_pwd = config['user']['password']


def test_selenium():
    xpath_by = "xpath"
    driver_option = Options()
    driver_option.add_argument("--disable-notifications")
    driver_option.add_experimental_option("detach", True)

    chrome = webdriver.Chrome("./chromedriver.exe", chrome_options=driver_option)
    chrome.get(ticket_producer_url)
    close_hint_btn_id = 'onetrust-accept-btn-handler'
    WebDriverWait(chrome, 60).until(EC.element_to_be_clickable((By.ID, close_hint_btn_id)))
    close_hint_btn_xpath = '//*[@id="board"]/img[3]'
    hint_btn = chrome.find_element(By.ID, close_hint_btn_id)
    hint_btn.click()

    login_btn_xpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/ul/li[3]/a'
    login_btn = chrome.find_element(xpath_by, login_btn_xpath)
    login_btn.click()

    fb_login = "loginFacebook"
    WebDriverWait(chrome, 60).until(EC.element_to_be_clickable((By.ID, fb_login)))
    fb_login_btn = chrome.find_element("id", fb_login)
    fb_login_btn.click()

    email = chrome.find_element(By.ID, "email")
    email.send_keys(user_email)
    passwd = chrome.find_element(By.ID, "pass")
    passwd.send_keys(user_pwd)
    login_btn = chrome.find_element(By.ID, "loginbutton")
    login_btn.click()

    till_time = False
    result = time.strptime("2022/11/09 23:17:00", "%Y/%m/%d %H:%M:%S")
    result_second = time.mktime(result)
    print(result_second)
    while till_time is False:
        now_time = time.time()
        print(f"now time: {now_time}")
        if now_time > result_second:
            till_time = True
    chrome.refresh()

    buy_ticket_xpath = '//*[@id="content"]/div/div/ul/li[1]/a'
    WebDriverWait(chrome, 60).until(EC.presence_of_element_located((By.XPATH, buy_ticket_xpath)))
    WebDriverWait(chrome, 60).until(EC.element_to_be_clickable((By.XPATH, buy_ticket_xpath)))
    buy_ticket_btn = chrome.find_element(By.XPATH, buy_ticket_xpath)
    buy_ticket_btn.click()

    buy_now_xpath = '//*[@id="gameList"]/table/tbody/tr/td[4]/input'
    WebDriverWait(chrome, 60).until(EC.element_to_be_clickable((By.XPATH, buy_now_xpath)))
    buy_now_btn = chrome.find_element(By.XPATH, buy_now_xpath)
    buy_now_btn.click()

    section_xpath = '//*[@id="group_0"]/li[1]'
    WebDriverWait(chrome, 60).until(EC.element_to_be_clickable((By.XPATH, section_xpath)))
    buy_now_btn = chrome.find_element(By.XPATH, section_xpath)
    buy_now_btn.click()

    select_num_xpath = '/html/body/div[1]/div[2]/div[2]/div/form/div[1]/table/tbody/tr/td[2]/select'
    select_num = Select(chrome.find_element(By.XPATH, select_num_xpath))
    select_num.select_by_visible_text("2")

    agree_btn_id = 'TicketForm_agree'
    chrome.find_element(By.ID, agree_btn_id).click()

    # recognize_img_id = 'yw0'
    # img_item = chrome.find_element(By.ID, recognize_img_id)
    # src = img_item.get_attribute("src")
    # print(f"image source:{src}")
    # with open("s.png", "wb") as img_file:
    #     img_file.write(img_item.screenshot_as_png)
    # # urllib.urlretrieve(src, "captcha.png")
    # img = Image.open("./s.png")
    # gg = img.convert("L")
    # text = pytesseract.image_to_string(gg, lang='eng')
    # print("test:", text)
    # gg.save("gg.png")

    verify_text_input_id = "TicketForm_verifyCode"
    input_item = chrome.find_element(By.ID, verify_text_input_id)
    input_item.click()

    time.sleep(5)


if __name__ == '__main__':
    test_selenium()
