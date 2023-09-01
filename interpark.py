import configparser
import time

import ddddocr
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

ticket_producer_url = "https://www.globalinterpark.com/product/23011804?lang=zh"
default_timeout = 3600

config = configparser.ConfigParser()
config.read("./config_interpark.ini")
user_email = config['user']['email']
user_pwd = config['user']['password']
user_name = config['user']['name']
user_birth_year = config['user']['birth_year']
user_birth_month = config['user']['birth_month']
user_birth_day = config['user']['birth_day']
user_phone = config['user']['phone']
user_credit_card_type = config['user']['card_type']  # Visa Master JCB
user_credit_card_num1 = config['user']['card_num1']
user_credit_card_num2 = config['user']['card_num2']
user_credit_card_num3 = config['user']['card_num3']
user_credit_card_num4 = config['user']['card_num4']
user_credit_card_month = config['user']['card_month']
user_credit_card_year = config['user']['card_year']
want_ticket_number = 1

driver_option = Options()
driver_option.add_argument("--disable-notifications")

driver_option.add_experimental_option("detach", True)  # Not close browser when code is done.
chrome_driver = webdriver.Chrome(options=driver_option)
chrome_driver.maximize_window()
chrome_driver.get(ticket_producer_url)


def login_interpark():
    login_btn_xpath = '/html/body/main/nav/div/ul/li[1]/a'
    hint_btn = chrome_driver.find_element(By.XPATH, login_btn_xpath)
    hint_btn.click()

    email_xpath = "//input[@placeholder='Email address']"
    email_input = WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, email_xpath)))
    email_input.send_keys(user_email)

    password_xpath = '//input[@placeholder="Password"]'
    pwd_input = chrome_driver.find_element(By.XPATH, password_xpath)
    pwd_input.send_keys(user_pwd)

    login_btn_xpath = "/html/body/main/div[3]/div[1]/div[1]/form/button"
    login_btn = chrome_driver.find_element(By.XPATH, login_btn_xpath)
    login_btn.click()


def switch_to_booking():
    chrome_driver.switch_to.default_content()
    product_frame_id = 'product_detail_area'
    WebDriverWait(chrome_driver, default_timeout).until(EC.visibility_of_element_located((By.ID, product_frame_id)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.ID, product_frame_id))
    try:
        booking_btns_div_class = 'btn_Booking'
        WebDriverWait(chrome_driver, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, booking_btns_div_class)))
        booking_btn_elm = chrome_driver.find_element(By.CLASS_NAME, booking_btns_div_class)
    except:
        chrome_driver.refresh()
        switch_to_booking()
    else:
        book_img_btn = booking_btn_elm.find_elements(By.TAG_NAME, 'img')
        book_img_btn[0].click()
        original_window = chrome_driver.current_window_handle
        for window_handle in chrome_driver.window_handles:
            if window_handle != original_window:
                chrome_driver.switch_to.window(window_handle)
                chrome_driver.maximize_window()
                break


def select_date_and_next():
    pick_date_xpath = 'ifrmBookStep'
    WebDriverWait(chrome_driver, default_timeout).until(EC.visibility_of_element_located((By.ID, pick_date_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.ID, pick_date_xpath))
    date_table_xpath = '/html/body/div/div[1]/div[2]/table'
    date_table_elm = chrome_driver.find_element(By.XPATH, date_table_xpath)
    date_tds = date_table_elm.find_elements(By.TAG_NAME, "td")
    date_tds.reverse()
    for td in date_tds:
        try:
            date_herf = td.find_element(By.TAG_NAME, "a")
            date_herf.click()
            break
        except Exception as e:
            print(type(e))
    # Select time
    time_span_xpath = '//*[@id="TagPlaySeq"]'
    time_span_elm = chrome_driver.find_element(By.XPATH, time_span_xpath)
    WebDriverWait(time_span_elm, default_timeout).until(EC.element_to_be_clickable((By.TAG_NAME, "ul")))
    time_ul = time_span_elm.find_element(By.TAG_NAME, "ul")
    time_li = time_ul.find_elements(By.TAG_NAME, "li")
    for li in time_li:
        try:
            print(f"li: {li.text}")
            li_herf = li.find_element(By.TAG_NAME, "a")
            li_herf.click()
            break
        except Exception as e:
            print(type(e))
    chrome_driver.switch_to.default_content()
    next_btn_xpath = "LargeNextBtn"
    WebDriverWait(chrome_driver, default_timeout).until(EC.element_to_be_clickable((By.ID, next_btn_xpath)))
    next_btn_elm = chrome_driver.find_element(By.ID, next_btn_xpath)
    next_btn_elm.click()


def recognize_code():
    content_frame_xpath = '//*[@id="ifrmSeat"]'
    WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, content_frame_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, content_frame_xpath))
    recognize_img_xpath = '//*[@id="imgCaptcha"]'
    img_item = chrome_driver.find_element(By.XPATH, recognize_img_xpath)
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(img_item.screenshot_as_png)
    input_div_xpath = '//*[@id="divRecaptcha"]/div[1]/div[3]'
    input_div_elm = chrome_driver.find_element(By.XPATH, input_div_xpath)
    input_div_elm.click()
    input_recog_xpath = '//*[@id="txtCaptcha"]'
    WebDriverWait(chrome_driver, default_timeout).until(EC.element_to_be_clickable((By.XPATH, input_recog_xpath)))
    input_recog_elm = chrome_driver.find_element(By.XPATH, input_recog_xpath)
    input_recog_elm.click()
    input_recog_elm.send_keys(res)
    complete_btn_xpath = '//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]'
    complete_btn_elm = chrome_driver.find_element(By.XPATH, complete_btn_xpath)
    complete_btn_elm.click()
    click_time = 0
    for i in range(60):
        print(input_div_elm.is_displayed())
        if not input_div_elm.is_displayed():
            break
        elif click_time == 0:
            input_div_elm.click()
            WebDriverWait(chrome_driver, default_timeout).until(
                EC.element_to_be_clickable((By.XPATH, input_recog_xpath)))
            input_recog_elm.click()
            click_time += 1
        time.sleep(1)
    if input_div_elm.is_displayed():
        raise Exception("Auto recognize Recaptcha failed. Please enter correct code in 1 min.")


def select_seat():
    seat_frame_xpath = '//*[@id="ifrmSeatDetail"]'
    WebDriverWait(chrome_driver, default_timeout).until(EC.visibility_of_element_located((By.XPATH, seat_frame_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, seat_frame_xpath))
    seat_table_xpath = '//*[@id="TmgsTable"]'
    table_elm = WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, seat_table_xpath)))

    td_elm = table_elm.find_elements(By.TAG_NAME, 'td')
    selected_seat = 0
    for td in td_elm:
        # img_elms = td.find_elements(By.TAG_NAME, 'img')
        img_elms = td.find_elements(By.TAG_NAME, 'span')
        print(f"td: {td}")
        print(f"This area total seats: {len(img_elms)}")
        for img_elm in img_elms:
            try:
                # Click available seat.
                if selected_seat == want_ticket_number:
                    break
                # if 'stySeat' == img_elm.get_attribute("class"):
                #     img_elm.click()
                #     selected_seat += 1
                if img_elm.get_attribute("class") == "SeatN":
                    img_elm.click()
                    selected_seat += 1
            except Exception as e:
                print(f"Select seat Exception: {e}")
    if selected_seat == want_ticket_number:
        is_selected = True
        chrome_driver.switch_to.default_content()
        chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))
        selected_seat_complete_xpath = '//*[@id="NextStepImage"]'
        selected_seat_complete_btn = chrome_driver.find_element(By.XPATH, selected_seat_complete_xpath)
        selected_seat_complete_btn.click()
        return is_selected
    else:
        print("No tickets avaliable in this area!!!!!!!!")
        is_selected = False
        return is_selected


def seat_table(is_already_click_area=False):
    is_selected = False
    chrome_driver.switch_to.default_content()
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))
    seat_menu_table_xpath = '//*[@id="SeatGradeInfo"]/div'
    table_elm = WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, seat_menu_table_xpath)))
    tr_elms = table_elm.find_elements(By.TAG_NAME, 'tr')
    for tr in tr_elms:
        chrome_driver.switch_to.default_content()
        chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))
        print(f"tr: {tr}")
        tr_id = tr.get_attribute("id")
        if tr_id == "GradeRow":
            area_elms = tr.find_elements(By.CLASS_NAME, 'select')
            for area in area_elms:
                print(f"area: {area.text}")
                # if area.text == "A座":
                #     print(f"Click {area.text}")
                #     if is_already_click_area is False:
                area.click()
                # else:
                #     continue
                box_elm = WebDriverWait(chrome_driver, default_timeout).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="GradeDetail" and @style=""]')))
                WebDriverWait(box_elm, default_timeout).until(EC.visibility_of_element_located((By.TAG_NAME, 'li')))
                li_elm = box_elm.find_elements(By.TAG_NAME, 'li')
                for li in li_elm:
                    chrome_driver.switch_to.default_content()
                    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))
                    time.sleep(0.3)
                    try:
                        small_area_a = li.find_element(By.TAG_NAME, 'a')
                        print(f"Scaning area: {small_area_a.text} ...")
                        small_area_a.click()
                        is_selected = select_seat()
                    except Exception as e:
                        print(f"Try area Exception: {e}")
                        break
    return is_selected


def select_seat_count():
    seat_count_frame = '//*[@id="ifrmBookStep"]'
    chrome_driver.switch_to.default_content()
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, seat_count_frame))
    seat_count_selector_xpath = '//*[@id="PriceRow001"]/td[3]/select'
    seat_count_name = "SeatCount"
    try:
        WebDriverWait(chrome_driver, 1).until(
            EC.visibility_of_element_located((By.NAME, seat_count_name)))
    except:
        print("excpettt")
        select_seat_count()
    else:
        seat_count_selector = Select(chrome_driver.find_element(By.NAME, seat_count_name))
        seat_count_selector.select_by_index(2)
        chrome_driver.switch_to.default_content()
        next_btn_xpath = '//*[@id="SmallNextBtnImage"]'
        next_btn_elm = chrome_driver.find_element(By.XPATH, next_btn_xpath)
        next_btn_elm.click()


def fill_personal_info():
    info_frame_xpath = '//*[@id="ifrmBookStep"]'
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, info_frame_xpath))
    name_xpath = '//*[@id="MemberName"]'
    birth_year_xpath = '//*[@id="BirYear"]'
    birth_month_xpath = '//*[@id="BirMonth"]'
    birth_day_xpath = '//*[@id="BirDay"]'
    connected_phone_xpath = '//*[@id="PhoneNo"]'
    phone_xpath = '//*[@id="HpNo"]'
    WebDriverWait(chrome_driver, default_timeout).until(EC.visibility_of_element_located((By.XPATH, name_xpath)))
    name_elm = chrome_driver.find_element(By.XPATH, name_xpath)
    birth_year_selector = Select(chrome_driver.find_element(By.XPATH, birth_year_xpath))
    birth_month_selector = Select(chrome_driver.find_element(By.XPATH, birth_month_xpath))
    birth_day_selector = Select(chrome_driver.find_element(By.XPATH, birth_day_xpath))
    connected_phone_elm = chrome_driver.find_element(By.XPATH, connected_phone_xpath)
    phone_elm = chrome_driver.find_element(By.XPATH, phone_xpath)
    name_elm.send_keys(user_name)
    birth_year_selector.select_by_value(user_birth_year)
    birth_month_selector.select_by_value(user_birth_month)
    birth_day_selector.select_by_value(user_birth_day)
    connected_phone_elm.send_keys(user_phone)
    phone_elm.send_keys(user_phone)
    chrome_driver.switch_to.default_content()
    next_btn_xpath = '//*[@id="SmallNextBtnImage"]'
    next_btn_elm = chrome_driver.find_element(By.XPATH, next_btn_xpath)
    next_btn_elm.click()


def input_payment():
    payment_frame_xpath = '//*[@id="ifrmBookStep"]'
    chrome_driver.switch_to.default_content()
    WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, payment_frame_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, payment_frame_xpath))
    payment_xpath = '//*[@id="Input_22003"]'
    WebDriverWait(chrome_driver, default_timeout).until(EC.visibility_of_element_located((By.XPATH, payment_xpath)))
    aa_elm = chrome_driver.find_element(By.XPATH, payment_xpath)
    korea_card_xpath = '//*[@id="PaymentSelect" and @value="C1"]'
    not_korea_card_xpath = '//*[@id="PaymentSelect" and @value="G1"]'
    korea_card_raido_elm = chrome_driver.find_element(By.XPATH, korea_card_xpath)
    not_korea_card_raido_elm = chrome_driver.find_element(By.XPATH, not_korea_card_xpath)
    not_korea_card_raido_elm.click()
    card_type_selector_xpath = '//*[@id="DiscountCardGlobal"]'
    card_type_selector = Select(chrome_driver.find_element(By.XPATH, card_type_selector_xpath))
    card_type_selector.select_by_visible_text(user_credit_card_type)  # Visa Master JCB
    card_num_p1_xpath = '//*[@id="CardNo1"]'
    card_num_p2_xpath = '//*[@id="CardNo2"]'
    card_num_p3_xpath = '//*[@id="CardNo3"]'
    card_num_p4_xpath = '//*[@id="CardNo4"]'
    card_vaild_month_xpath = '//*[@id="ValidMonth"]'
    card_vaild_year_xpath = '//*[@id="ValidYear"]'
    card_num_p1_elm = WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, card_num_p1_xpath)))
    card_num_p2_elm = chrome_driver.find_element(By.XPATH, card_num_p2_xpath)
    card_num_p3_elm = chrome_driver.find_element(By.XPATH, card_num_p3_xpath)
    card_num_p4_elm = chrome_driver.find_element(By.XPATH, card_num_p4_xpath)
    card_num_p1_elm.send_keys(user_credit_card_num1)
    card_num_p2_elm.send_keys(user_credit_card_num2)
    card_num_p3_elm.send_keys(user_credit_card_num3)
    card_num_p4_elm.send_keys(user_credit_card_num4)
    card_vaild_year_selector = Select(chrome_driver.find_element(By.XPATH, card_vaild_year_xpath))
    card_vaild_month_selector = Select(chrome_driver.find_element(By.XPATH, card_vaild_month_xpath))
    card_vaild_month_selector.select_by_value(user_credit_card_month)
    card_vaild_year_selector.select_by_value(user_credit_card_year)
    chrome_driver.switch_to.default_content()
    # next_btn_xpath = '//*[@id="SmallNextBtnImage"]'
    # next_btn_elm = chrome_driver.find_element(By.XPATH, next_btn_xpath)
    # next_btn_elm.click()


def check_payment():
    payment_frame_xpath = '//*[@id="ifrmBookStep"]'
    chrome_driver.switch_to.default_content()
    WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, payment_frame_xpath)))
    chrome_driver.switch_to.frame(chrome_driver.find_element(By.XPATH, payment_frame_xpath))
    agree_cancle_xpath = '//*[@id="CancelAgree"]'
    agree_third_party_xpath = '//*[@id="CancelAgree2"]'
    agree_cancle_elm = WebDriverWait(chrome_driver, default_timeout).until(
        EC.visibility_of_element_located((By.XPATH, agree_cancle_xpath)))
    agree_third_party_elm = chrome_driver.find_element(By.XPATH, agree_third_party_xpath)
    agree_cancle_elm.click()
    agree_third_party_elm.click()


if __name__ == '__main__':
    playsound('./Alarm02.wav')
    login_interpark()
    switch_to_booking()
    select_date_and_next()
    recognize_code()
    is_selected = seat_table()
    while is_selected is False:
        is_selected = seat_table(is_already_click_area=True)
    playsound('./Alarm02.wav')
    # select_seat_count()
    # fill_personal_info()
    # input_payment()
    # check_payment()
