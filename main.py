from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import personal_data
import time
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import apiclient.discovery

#импорт логина и пароля из файла personal_data
username = personal_data.username
password = personal_data.password
spreadsheet = personal_data.spreadsheetId
def write_gt(vacancys):
    CREDENTIALS_FILE = 'parse-for-google-sheets.json'  # Имя файла с закрытым ключом, вы должны подставить свое
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    # Выбираем работу с таблицами и 4 версию API
    spreadsheetId = spreadsheet
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    results = service.spreadsheets().values().append(spreadsheetId=spreadsheetId,range="Лист1!A1", valueInputOption="RAW", body= {'values' :vacancys}).execute()
    service.close()

#bot,message
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
    serch_form = browser.find_element(By.CSS_SELECTOR , 'input[data-qa="search-input"').send_keys('python')
    serch_button = browser.find_element(By.CSS_SELECTOR , 'button[data-qa="search-button"').click()
    url_serch_form = browser.current_url
    #bot.reply_to(message, 'Откликаюсь на все вакансии по этой ссылке:' + url_serch_form)
    #находим элементы с кнопкой "отклинутся и через цикл на все нажимаем

    all_vacs = []
    for i in range(2):
        serch_blocs_vac = browser.find_elements(By.CSS_SELECTOR, 'div[class="vacancy-serp-item__layout"')
        print(serch_blocs_vac)
        for serch_bloc_vac in serch_blocs_vac:
            # serch_button_response= serch_bloc_vac.find_elements(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy_response"').click()
            vacancys = []

            vacancys.extend([
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[data-qa="serp-item__title"').text,
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[class="bloko-link bloko-link_kind-tertiary"').text,
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[class="serp-item__title"').get_attribute('href'),
                serch_bloc_vac.find_element(By.CSS_SELECTOR, 'a[class="bloko-link bloko-link_kind-tertiary"').get_attribute('href')
            ])
            all_vacs.append(vacancys)
        browser.find_element(By.CSS_SELECTOR, 'a[data-qa="pager-next"').click()
    print(len(all_vacs))

    time.sleep(3)

    browser.close()
    return all_vacs


