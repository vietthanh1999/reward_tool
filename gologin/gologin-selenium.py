import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from gologin import getRandomPort

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2UzYjM0Yzk4MTk1OTI0ZmFmNGFlNmEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2UzYjU1MzBmODEzMWZmZTdmNzA0ZTQifQ.mb7Tq8aH39irU2WCqT90Pbvdfrd9MXbNbJ3uqqP5wLc",
	"profile_id": "63e6513eea0a3ddc4ef8fbdd"
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
# driver.get("https://www.google.com/")
# print( driver)
# assert "Google" in driver.title
# time.sleep(3)
# driver.close()
# gl.stop()

driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
