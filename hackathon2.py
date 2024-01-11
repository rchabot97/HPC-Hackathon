from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from gmail import gmail_authenticate, search_messages, read_message
from twilio.rest import Client
from bs4 import BeautifulSoup as BS
from time import sleep
import sys


def read_twilio(phrase):

    account_sid = 'AC1adb6c861db51ed393f19bc0e7decfd6'
    auth_token = '4b3b31b4aee34dc934ab1f1265f0ce15'

    client = Client(account_sid, auth_token)

    pin = ''
    for sms in client.messages.list():
        if phrase in sms.body:
            pin = sms.body.split(phrase)[-1][:6]
            break

    return pin


def get_pin_from_email(phrase):

    service = gmail_authenticate()

    results = search_messages(service, phrase)

    pin = ''
    for msg in results:
        email = read_message(service, msg)
        if "body" in email.keys():
            soup = BS(email['body'], 'html.parser')
            code_container = soup.find(id="accessCodeBody").text
            pin = code_container.split('Your One-Time Access Code:')[-1].strip()[:7]
            break

    return pin


def evicore_login(username, password, auth_method):

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        service=Service(r"C:\Users\Riley Chabot\Downloads\chromedriver_win32 (2)\chromedriver.exe"), options=options)
    wait = WebDriverWait(driver, 5)

    driver.set_window_position(-2000, 0)

    try:

        driver.get('https://www.evicore.com/')

        frame = driver.find_elements(By.XPATH, '//div[@class="login-form"]/iframe')[1]
        driver.switch_to.frame(frame)

        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="txtUserEmail"]'))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="txtPassWord"]'))).send_keys(password)
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="agree"]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmUserLogin"]/div[6]/div/button'))).click()

    except Exception as e:
        print(e)
        print('error logging in')
        sys.exit()

    try:

        host = driver.find_element(By.XPATH, '//*[@id="eviuserauthenticate"]')
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', host)

        shadow_root.find_element(By.CSS_SELECTOR, f'div > div > evi-{auth_method}-authenticate > form > div:nth-child(1) > div.container > div > div > button').click()

        sleep(5)

        pin = read_twilio('Your PIN is: ')

        shadow_root.find_element(By.CSS_SELECTOR, f'div > div > evi-{auth_method}-authenticate > form > div:nth-child(2) > input').send_keys(pin)
        shadow_root.find_element(By.CSS_SELECTOR, f'div > div > evi-{auth_method}-authenticate > form > div:nth-child(2) > div > div > div > input[type=submit]').click()

    except:
        pass

    wait.until(EC.presence_of_element_located((By.ID, "ctl00_ucMainMenu_hlPendingCases"))).click()

    driver.maximize_window()

    return driver


def availity_login(user_id, password):

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        service=Service(r"C:\Users\Riley Chabot\Downloads\chromedriver_win32 (2)\chromedriver.exe"), options=options)
    wait = WebDriverWait(driver, 5)

    driver.set_window_position(-2000, 0)

    driver.get('https://apps.availity.com/availity/web/public.elegant.login?goto=https%3A%2F%2Fapps.availity.com%2Fpublic%2Fapps%2Fhome%2F%23!%2F')

    try:

        wait.until(EC.presence_of_element_located((By.ID, 'userId'))).send_keys(user_id)
        wait.until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
        wait.until(EC.presence_of_element_located((By.ID, 'loginFormSubmit'))).click()

    except Exception as e:
        print(e)
        print('error logging in')
        sys.exit()

    try:

        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="form-check"]/input'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//form/button'))).click()

        sleep(5)
        pin = read_twilio('Use verification code ')

        wait.until(EC.presence_of_element_located((By.ID, 'passCode'))).send_keys(pin)
        wait.until(EC.presence_of_element_located((By.ID, 'verify-code'))).click()

        wait.until(EC.presence_of_element_located((By.ID, 'complete-2fa-registration'))).click()

    except:
        pass

    driver.maximize_window()

    return driver


def one_healthcare_login(one_healthcare_id, password):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(
        service=Service(r"C:\Users\Riley Chabot\Downloads\chromedriver_win32 (2)\chromedriver.exe"))
    wait = WebDriverWait(driver, 5)

    driver.get('https://secure.uhcprovider.com')

    wait.until(EC.presence_of_element_located((By.ID, 'userNameId_input'))).send_keys(one_healthcare_id)
    wait.until(EC.presence_of_element_located((By.ID, 'passwdId_input'))).send_keys(password)
    sleep(5)
    wait.until(EC.presence_of_element_located((By.ID, 'SignIn'))).click()
    # sleep(5)
    # wait.until(EC.presence_of_element_located((By.ID, 'SignIn'))).click()

    try:
        sleep(10)
        pin = get_pin_from_email("Access Code Notification")

        wait.until(EC.presence_of_element_located((By.ID, "EmailText_input"))).send_keys(pin)
        wait.until(EC.presence_of_element_located((By.ID, "rememberDeviceCheckbox"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "EmailAccessCodeSubmitButton"))).click()

    except:
        pass

    return driver
