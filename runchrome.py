import time
import re
from sys import platform
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from gologin import GoLogin
from gologinprofile import GologinProfile
from gologin import getRandomPort

from mail import get_code_from_mailnesia


delay_time = 2
sleep_affter_click = 1

if platform == "linux" or platform == "linux2":
    chrome_driver_path = "./chromedriver"
elif platform == "darwin":
    chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
    chrome_driver_path = "./chromedriver.exe"

drivers = []

# Code open link
def start_process(gp: GologinProfile, token: str, reward_link: str, mail_account_info = []):
    profile_id = gp.create_profile()
    gl = GoLogin({'token': token, 'profile_id': profile_id})
    debugger_address = gl.start()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    drivers.append(driver)

    driver.get(reward_link)
    try:
        print("Wait the page reward open!")
        signUpButton: WebElement = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.ID, 'start-earning-rewards-link')))
        print("Page is ready!")
        WebDriverWait(driver, delay_time).until(
            EC.element_to_be_clickable(signUpButton))
        print("Sign Up button is ready!")
        signUpButton.click()

        print("Entering email...")
        emailInput: WebElement = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
        time.sleep(sleep_affter_click)
        emailInput.send_keys(mail_account_info[0])
        time.sleep(sleep_affter_click)
        nextButton: WebElement = driver.find_element(
            By.CSS_SELECTOR, '[type="submit"]')
        nextButton.click()

        print("Entering password...")
        passwordInput: WebElement = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.NAME, 'passwd')))
        time.sleep(sleep_affter_click)
        passwordInput.send_keys(mail_account_info[1])
        time.sleep(sleep_affter_click)
        signInButton: WebElement = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
        signInButton.click()

        # Check passwork error
        time.sleep(5)

        retry_time = 0
        allow_continue = False
        step = ''
        while(retry_time < 10):
            if driver.find_elements(By.ID, 'passwordError').count != 0:
                # TODO: Xử lý sai pass
                print('Sai password')
                driver.close()
                raise 'Sai password'
            if driver.find_element(By.ID, 'iLandingViewAction'):
                allow_continue = True
                step = 'landingiew'
                break
            if driver.find_element(By.ID, 'iProof0'):
                allow_continue = True
                allow_continue = True
                step = 'chosemailverify'
                break
            time.sleep(6)
        if (allow_continue == False):
            print('false at allow_continue')
            raise('false at allow_continue')
        
        if (step == 'landingiew'):
            driver.find_element(By.ID, 'iLandingViewAction').click()
            time.sleep(3)
        
        driver.find_element(By.ID, 'iProof0')
        time.sleep(2)
        driver.find_element(By.ID, 'iProofEmail').send_keys(mail_account_info[2])
        time.sleep(2)
        start_verify_time = int(time.time())
        driver.find_element(By.ID, 'iSelectProofAction').click()
        code = get_verify_code(start_verify_time, mail_account_info[2], mail_account_info[3], mail_account_info[4])
        driver.find_element(By.ID, 'iOttText').send_keys(code)
        time.sleep(2)
        driver.find_element(By.ID, 'iVerifyCodeAction').click()
        # TODO: Xử lý reward

            
        # elif ()
        # elif():
        #     # TODO: Xử lý trường hợp mail lock
        # elif (driver.find_elements(By.CSS_SELECTOR, '.pull-left > .win-color-fg-alert').count != 0):
        #     print('Khong du diem')
        #     driver.close()
        #     raise 'Khong du diem'

        
        # get_verify_code()
    except TimeoutException:
        # TODO: Xử lý trường hợp proxy chậm
        print("Loading took too much time!")
    except:
        print("Error to login")

def get_verify_code(start_verify_time: int, mail: str, password: str, mail_verify: str):
        # hotmail login link: https://outlook.live.com/owa/?nlp=1
        profile_id = gp.create_profile()
        gl = GoLogin({'token': token, 'profile_id': profile_id})
        debugger_address = gl.start()
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", debugger_address)
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        driver.get('https://outlook.live.com/owa/?nlp=1')
        WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.ID, 'loginfmt')))

        driver.find_element(By.ID, 'loginfmt').send_keys(mail)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        time.sleep(2)
        driver.find_element(By.NAME, 'passwd').send_key(password)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        retry_time = 0
        allow_continue = False
        step = ''
        while(retry_time < 10):
            if driver.find_elements(By.ID, 'passwordError').count != 0:
                # TODO: Xử lý sai pass
                print('Sai password')
                driver.close()
                raise 'Sai password'
            if driver.find_element(By.ID, 'iLandingViewAction'):
                allow_continue = True
                step = 'landingiew'
                break
            if driver.find_element(By.ID, 'iProof0'):
                allow_continue = True
                allow_continue = True
                step = 'chosemailverify'
                break
            time.sleep(6)
        if (allow_continue == False):
            print('false at allow_continue')
            raise('false at allow_continue')
        
        if (step == 'landingiew'):
            driver.find_element(By.ID, 'iLandingViewAction').click()
            time.sleep(3)

        driver.find_element(By.ID, 'iProof0')
        time.sleep(2)
        driver.find_element(By.ID, 'iProofEmail').send_keys(mail_verify)
        time.sleep(2)
        start_verify_time = int(time.time())
        code = get_code_from_mailnesia(mail_verify, start_verify_time)
        time.sleep(2)
        driver.find_element(By.ID, 'iOttText').send_keys(code)
        time.sleep(2)
        driver.find_element(By.ID, 'iVerifyCodeAction').click()
            # Chờ cho đến khi có
        yButton: WebElement = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        time.sleep(1)
        yButton.click()
        WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="listbox"]')))
        driver.find_element(By.ID, 'Pivot84-Tab1').click()
        time.sleep(3)
        list_mail = driver.find_elements(By.CLASS_NAME, 'hcptT')
        retry_time = 0
        while(retry_time < 10):
            for mail in list_mail:
                result = re.findall(r'>[0-9]{7}<', mail.get_attribute('aria-label'))
                if (result):
                    code = result[0]
                    return code[1:8]
            time.sleep(6)
            retry_time = retry_time+1
        raise('Can not get code from mail hotmail')


# start_process(reward_link="https://rewards.microsoft.com/redeem/checkout?productId=000800000041",
#               username="CaydanceSatava@hotmail.com", password="i6tWzwpuNY")

def close_process():
    for driver_item in drivers: 
        driver_item.close()
# assert "Python" in driver.title
# time.sleep(3)
# driver.close()
# gl.stop()