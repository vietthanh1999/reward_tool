import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from gologin import GoLogin
from gologin import getRandomPort

from mail import get_code_from_mailnesia


delay_time = 3
sleep_affter_click = 3

gl = GoLogin({
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2UzYjM0Yzk4MTk1OTI0ZmFmNGFlNmEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2UzYjU1MzBmODEzMWZmZTdmNzA0ZTQifQ.mb7Tq8aH39irU2WCqT90Pbvdfrd9MXbNbJ3uqqP5wLc",
    "profile_id": "63e668f64cc7e1357989fef7"
})

gl2 = GoLogin({
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2UzYTkyNjdhNWI5ZjY5NTkzMGFiM2EiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2UzZDQ4Y2U3YWYyN2Y5ZDc2NDE5M2EifQ.2DBLkB0ir5fR7pZyXTaFHYvJCXz8LryaXvTap4d8rkg",
    "profile_id": "63e6513eea0a3ddc4ef8fbdd"
})

if platform == "linux" or platform == "linux2":
    chrome_driver_path = "./chromedriver"
elif platform == "darwin":
    chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
    chrome_driver_path = "./chromedriver.exe"


# driver.get("https://iphey.com")

drivers =[]

# Code open link
def start_process(reward_link: str, mail_account_info = []):
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
        time.sleep(sleep_affter_click)
        # emailInput = driver.find_element(By.NAME, 'loginfmt')
        emailInput: WebElement = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
        emailInput.send_keys(mail_account_info[0])
        time.sleep(sleep_affter_click)
        nextButton: WebElement = driver.find_element(
            By.CSS_SELECTOR, '[type="submit"]')
        nextButton.click()

        # time.sleep(sleep_affter_click)
        # print("Entering password...")
        # passwordInput: WebElement = WebDriverWait(driver, delay_time).until(EC.presence_of_element_located((By.NAME, 'passwd')))
        # print(mail_account_info[1])
        # passwordInput.send_keys(mail_account_info[1])
        # time.sleep(sleep_affter_click)
        # signInButton: WebElement = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
        # signInButton.click()

        # # Check passwork error
        # # time.sleep(5)
        # # if driver.find_elements(By.ID, 'passwordError').count != 0:
        # #     print('Sai password')
        # #     driver.close()
        # #     raise 'Sai password'
        # # elif (driver.find_elements(By.CSS_SELECTOR, '.pull-left > .win-color-fg-alert').count != 0):
        # #     print('Khong du diem')
        # #     driver.close()
        # #     raise 'Khong du diem'

        # # time.sleep(5)
        # # noButton: WebElement = driver.find_element(By.ID, 'idBtn_Back')
        # # print(noButton)
        # # if noButton: 
        # #     noButton.click()

        # time.sleep(5)
        # checkboxEmail: WebElement = driver.find_element(By.ID, 'iProof0')
        # checkboxEmail.click()

        # time.sleep(5)
        # emailVerifyInput: WebElement = driver.find_element(By.ID, 'iProofEmail')
        # emailVerifyInput.send_keys(mail_account_info[2])

        # time.sleep(5)
        # iSelectProofActionButton: WebElement = driver.find_element(By.ID, 'iSelectProofAction')
        # iSelectProofActionButton.click()
        
        time.sleep(5)
        new_debugger_address = gl2.start()
        new_chrome_options = Options()
        new_chrome_options.add_experimental_option("debuggerAddress", new_debugger_address)
        new_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=new_chrome_options)
        drivers.append(new_driver)

        time.sleep(15)
        print(mail_account_info[4])
        code = get_code_from_mailnesia(mail_account_info[4])
        print(code)

    except TimeoutException:
        print("Loading took too much time!")
    except:
        print("Error to login")

# start_process(reward_link="https://rewards.microsoft.com/redeem/checkout?productId=000800000041",
#               username="CaydanceSatava@hotmail.com", password="i6tWzwpuNY")

def close_process():
    for driver_item in drivers: 
        driver_item.close()
# assert "Python" in driver.title
# time.sleep(3)
# driver.close()
# gl.stop()