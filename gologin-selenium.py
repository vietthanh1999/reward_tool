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


delay_time = 3
sleep_affter_click = 2

gl = GoLogin({
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2UzYTkyNjdhNWI5ZjY5NTkzMGFiM2EiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2UzZDQ4Y2U3YWYyN2Y5ZDc2NDE5M2EifQ.2DBLkB0ir5fR7pZyXTaFHYvJCXz8LryaXvTap4d8rkg",
    "profile_id": "63e649cc351ae6cc4bc8fe77"
})

if platform == "linux" or platform == "linux2":
    chrome_driver_path = "./chromedriver"
elif platform == "darwin":
    chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
    chrome_driver_path = "chromedriver.exe"

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
# driver.get("https://iphey.com")

# Code open link
def start_process(driver: webdriver.Chrome, reward_link: str, username: str, password: str):
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
        emailInput: WebElement = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.NAME, 'loginfmt')))
        emailInput.send_keys(username)
        time.sleep(sleep_affter_click)
        nextButton: WebElement = driver.find_element(
            By.CSS_SELECTOR, '[type="submit"]')
        nextButton.click()

        time.sleep(sleep_affter_click)
        print("Entering password...")
        passwordInput: WebElement = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.NAME, 'passwd')))
        passwordInput.send_keys(password)
        time.sleep(sleep_affter_click)
        signInButton: WebElement = driver.find_element(
            By.CSS_SELECTOR, '[type="submit"]')
        signInButton.click()

        # Check passwork error
        time.sleep(5)
        if driver.find_elements(By.ID, 'passwordError').count != 0:
            print('Sai password')
            # driver.close()
            # raise 'Sai password'
        elif (driver.find_elements(By.CSS_SELECTOR, '.pull-left > .win-color-fg-alert').count != 0):
            print('Khong du diem')
            # driver.close()
            # raise 'Khong du diem'
        elif driver.find_elements(By.ID, 'iLandingViewAction').count != 0:
            verifyEmail(driver=driver, verifyEmail='FrazzanoAddlie00@hotmail.com', password='z45t7qHV')
    except TimeoutException:
        print("Loading took too much time!")
    except:
        print("Error to login")

def verifyEmail(driver: webdriver.Chrome, verifyMail: str, password: str):
    verifyButton = driver.find_elements(By.ID, 'iLandingViewAction')[0]
    verifyButton.click()
    time.sleep(5)

    listRadio = driver.find_elements(By.ID, 'iProof0')
    radio = listRadio[0]
    radio.click()
    time.sleep(5)

    verifyDriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    verifyDriver.get('https://outlook.live.com/owa/')
    mailnesiaDriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    verifyDriver.get('https://mailnesia.com/mailbox/amandaangeline')
    try:
        print("Wait the page reward open!")
        signInButton: WebElement = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-task="signin"]')))
        print("Page is ready!")
        WebDriverWait(driver, delay_time).until(
            EC.element_to_be_clickable(signInButton))
        print("Sign Up button is ready!")
        signInButton.click()

        # code id iOttText
        # code element:
        # <input type="tel" id="iOttText" name="iOttText" class="form-control input-max-width form-group" maxlength="16" placeholder="Code" aria-label="Enter your security code" aria-describedby="iEnterSubhead" aria-required="true">
        # Next: <input type="submit" id="iVerifyCodeAction" class="btn btn-block btn-primary" value="Next">

        # New pass: <input type="password" class="form-control email-input-max-width" id="iPassword" name="Password" aria-required="true" aria-describedby="pNewPwdErrorArea UpdatePasswordTitle iPassHint" placeholder="New password" aria-label="New password" data-bind="value: password, hasFocus: password.focused, moveOffScreen: showPassword, event: { keypress: onPasswordKeyPress }, css: { 'has-error': showError(password) }" maxlength="127" tabindex="0">
        # Next: <input type="submit" id="iPasswordViewAction" class="btn btn-block win-button btn-primary" role="button" aria-describedby="UpdatePasswordTitle" tabindex="0" value="Next">
        
        # Not now:<a id="iCollectProofsViewAlternate" class="secondary-text" tabindex="0" href="#">Not now</a>
        # Sign in: <input type="submit" role="button" aria-describedby="iPageTitle" tabindex="0" class="btn btn-block btn-primary" id="iFinishViewAction" value="Sign in">

        # code: <span style="font-family: &quot;Segoe UI Bold&quot;, &quot;Segoe UI Semibold&quot;, &quot;Segoe UI&quot;, &quot;Helvetica Neue Medium&quot;, Arial, sans-serif; font-size: 14px; font-weight: bold; color: rgb(42, 42, 42) !important;">5043887</span>
        print("Entering verify email...")
        time.sleep(sleep_affter_click)
        emailInput: WebElement = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[type="email"]')))
        emailInput.send_keys(verifyEmail)
        time.sleep(sleep_affter_click)
        nextButton: WebElement = driver.find_element(
            By.CSS_SELECTOR, '[type="submit"]')
        nextButton.click()

        time.sleep(sleep_affter_click)
        print("Entering password...")
        passwordInput: WebElement = WebDriverWait(driver, delay_time).until(
            EC.presence_of_element_located((By.NAME, 'passwd')))
        passwordInput.send_keys(password)
        time.sleep(sleep_affter_click)
        signInButton: WebElement = driver.find_element(
            By.CSS_SELECTOR, '[type="submit"]')
        signInButton.click()

        time.sleep(5)
        driver.find_elements(By.ID, 'iProof0')
        radio = driver.find_elements(By.ID, 'iProof0')[0]
        radio.click()
        time.sleep(sleep_affter_click)
        emailKPInput = driver.find_element(By.NAME, 'iProofEmail')
        emailKPInput.send_keys('amandaangeline')

    except TimeoutException:
        print("Loading took too much time!")
    except:
        print("Error to login")


start_process(driver=driver, reward_link="https://rewards.microsoft.com/redeem/checkout?productId=000800000041",
              username="CaiazzoTrinten01@outlook.com", password="dXnXdh23o")


# assert "Python" in driver.title
# time.sleep(3)
# driver.close()
# gl.stop()