from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import gspread

#импорт логина и пароля из файла personal_data
username = personal_data.username
password = personal_data.password

def write_gt(vacancys):
    spreadsheet = personal_data.spreadsheetId
    gs = gspread.service_account(filename='parse-for-google-sheets.json')
    spreadsheet = gs.open_by_key(spreadsheet)
    worksheet = spreadsheet.sheet1
    worksheet.append_row(vacancys)

def parser(bot,message):
    options = Options()
    #options.add_argument("--headless")#открываем браузер в фоновом режиме
    browser = webdriver.Chrome("/chromedriver.exe", options=options)
    browser.maximize_window()
    browser.get("https://hh.ru/account/login")
    # находим элементы и кликаем на кнопку или вводим информацию
    serch_button_enter = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="expand-login-by-password"').click()
    serch_input_login = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="login-input-username"').send_keys(username)
    serch_input_password = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="login-input-password"').send_keys(password)
    serch_button_input = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="account-login-submit"').click()
    time.sleep(3)
    serch_form = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="search-input"').send_keys('1С')
    serch_button = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="search-button"').click()
    url_serch_form = browser.current_url
    bot.reply_to(message, 'Откликаюсь на все вакансии по этой ссылке:' + url_serch_form)
    #находим элементы с кнопкой "отклинутся и через цикл на все нажимаем

    for i in range(2):
        serch_blocs_vac = browser.find_elements(By.CSS_SELECTOR, 'div[class="vacancy-serp-item__layout"')
        print(serch_blocs_vac)
        for serch_bloc_vac in serch_blocs_vac:
            try:
                serch_button_response= serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy_response"').click()
                print(browser.current_url)
            except StaleElementReferenceException:
                continue
            if 'vacancyId' in browser.current_url:
                browser.back()
                time.sleep(3)
                print('ff')
                continue
            print(browser.current_url)
            vacancys = []

            vacancys.extend([
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[data-qa="serp-item__title"').text,
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[class="bloko-link bloko-link_kind-tertiary"').text,
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[class="serp-item__title"').get_attribute('href'),
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[class="bloko-link bloko-link_kind-tertiary"').get_attribute('href')
            ])
            write_gt(vacancys)
        browser.find_element(By.CSS_SELECTOR, 'a[data-qa="pager-next"').click()

    time.sleep(3)
    browser.close()
