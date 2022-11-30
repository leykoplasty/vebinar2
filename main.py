from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import personal_data
import time

#импорт логина и пароля из файла personal_data
username = personal_data.username
password = personal_data.password

def parser():
    options = Options()
    options.add_argument("--headless")#открываем браузер в фоновом режиме
    browser = webdriver.Chrome("/chromedriver.exe", options=options)
    browser.maximize_window()
    browser.get("https://hh.ru/account/login")
    # находим элементы и кликаем на кнопку или вводим информацию
    serch_button_enter = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="expand-login-by-password"').click()
    serch_input_login = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="login-input-username"').send_keys(username)
    serch_input_password = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="login-input-password"').send_keys(password)
    serch_button_input = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="account-login-submit"').click()
    time.sleep(3)
    serch_form = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="search-input"').send_keys('python')
    serch_button = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="search-button"').click()
    url_serch_form = browser.current_url
    #находим элементы с кнопкой "отклинутся и через цикл на все нажимаем
    serch_buttons_response = browser.find_element(By.CSS_SELECTOR , 'a[data-qa="vacancy-serp__vacancy_response"')#.click()
    for serch_button_response in serch_buttons_response:
        serch_button_response.click()
    time.sleep(3)
    browser.close()
    return url_serch_form


