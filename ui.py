import logging
import time
import ctypes
import threading
import re
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from gologinprofile import GologinProfile
from datetime import date
from globaldata import thread_data_list, main_thread

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
from sms import Sms

import os

timeout = 10
sleep_affter_click = 5

if platform == "linux" or platform == "linux2":
    chrome_driver_path = "./chromedriver"
elif platform == "darwin":
    chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
    chrome_driver_path = "./chromedriver.exe"


logging.basicConfig(filename='log-'+str(date.today())+'.txt', format="%(asctime)s %(message)s")

screen=Tk()
# screen.withdraw()
screen.title('Reward Tool')
screen.geometry('980x620')


def handle_exception(exception, value, traceback):
    logging.error(str(exception)+str(value)+str(traceback))
    logging.fatal('')
    print(str(exception)+str(value)+str(traceback))
# screen.report_callback_exception = handle_exception

table = ttk.Treeview(screen)
table.place(x = 32, y = 32, relheight=.8, relwidth=.5)

table['columns']= ('id', 'mail','pass', 'status')
table.column("#0", width=0,  stretch=NO)
table.column("id",anchor=CENTER, width=10)
table.column("mail",anchor=CENTER, width=80)
table.column("pass",anchor=CENTER, width=80)
table.column("status",anchor=CENTER, width=80)

table.heading("#0",text="",anchor=CENTER)
table.heading("id",text="ID",anchor=CENTER)
table.heading("mail",text="Email",anchor=CENTER)
table.heading("pass",text="Password",anchor=CENTER)
table.heading("status",text="Status",anchor=CENTER)

#data
data  = [
    # [1,"Jack","gold"],
    # [2,"Tom","Bronze"]
]

global count
count=0
table_mails = []
    
for record in data:
    table.insert(parent='', index='end', iid = count, text='', values=(record[0], record[1], record[2]))
    count += 1

# frame input
Input_frame = Frame(screen, highlightbackground="white", highlightthickness=3)
Input_frame.place(relx=0.6, y=32, relheight=.8, relwidth=.36)

file_mail = Label(Input_frame, text="File mail: ")
file_mail.place(x=16, y=30)
file_mail_entry = Entry(Input_frame)
file_mail_entry.insert(0, r"")
file_mail_entry.place(x=16, y=50, relwidth=0.55)

link_reward= Label(Input_frame, text="Link reward: ")
link_reward.place(x=16, y=80)
link_reward_entry = Entry(Input_frame)
link_reward_entry.insert(0, r"https://rewards.microsoft.com/redeem/checkout?productId=000800000041")
link_reward_entry.place(x=16, y=100, relwidth=0.8)

gologin_token = Label(Input_frame, text="Gogin token: ")
gologin_token.place(x=16, y=130)
gologin_token_entry = Entry(Input_frame)
gologin_token_entry.insert(0, r"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2YwZjc2MDc1ZmE4OTc1OGM5NjZmNTMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2YwZjc5MDk1OWZiMDBmZDEyYjhhOWIifQ.R3jDcI0vVZD1yL-OC0RhbURc-4KCdrNw7kzG6g3ZOZk")
gologin_token_entry.place(x=16, y=150, relwidth=0.8)

five_sim_token = Label(Input_frame, text="5Sim token: ")
five_sim_token.place(x=16, y=180)
five_sim_token_entry = Entry(Input_frame)
five_sim_token_entry.insert(0, r"eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDgxODYxNzksImlhdCI6MTY3NjY1MDE3OSwicmF5IjoiYTBlNzM1YTNmOGE5ZGEzOWVhOTExNzVhZDBmYWFlMzIiLCJzdWIiOjQ0NTQ1M30.G5a5SSlFn6zFXXSX8avM0hxAQ-ZL7e_zyzjvEJ4m8OkJa6EsHf5a0OMRErEo-sgUhZy64JhlWDCjLsSWgJ4Nxec4Ni0ysnIYomWw9wYkelabCNaPlSGmrNL40K5n3mR1hUbsnJMMHubnhi5CzdqJ3N1xnzynbV1ayMLMal5X53ykiT-xJEJUB_siSJdYS7Sar80VueIOI2QGAS8GaBTc3rYrXeiHPg2qYhYUF9E1XO2KvADky9ZMCDRx8K3qtLBWHIG9GMAzx2mM7j6RFpQ3nQUXBmZECRJWPpyqSERAiPqaCiz5LnyFQccEavcHwi-AWbulbu13maWGYySsf1fJjA")
five_sim_token_entry.place(x=16, y=200, relwidth=0.8)

proxy_api_link = Label(Input_frame, text="Proxy API link: ")
proxy_api_link.place(x=16, y=230)
proxy_api_link_entry = Entry(Input_frame)
proxy_api_link_entry.insert(0, r"https://tq.lunaproxy.com/getflowip?neek=1021070&num=10&type=2&sep=1&regions=us&ip_si=1&level=1&sb='")
proxy_api_link_entry.place(x=16, y=250, relwidth=0.8)

mail_on_ip = Label(Input_frame, text="Mail/1IP: ")
mail_on_ip.place(x=16, y=280)
variable_mail_on_ip = StringVar(Input_frame)
variable_mail_on_ip.set(1) # default value
mail_on_ip_entry = OptionMenu(Input_frame, variable_mail_on_ip, 1, 2, 3, 4, 5)
mail_on_ip_entry.place(x=16, y=300, relwidth=0.2)
# mail_on_ip_entry = Entry(Input_frame)
# mail_on_ip_entry.place(x=16, y=150, relwidth=0.4)

lb_run_mail_again = Label(Input_frame, text="S??? l???n ch???y l???i mail:")
lb_run_mail_again.place(x=120, y=280)

variable = StringVar(Input_frame)
variable.set(1) # default value
et_run_mail_again = OptionMenu(Input_frame, variable, 1, 2, 3)
et_run_mail_again.place(x=120, y=300, relwidth=0.2)
# et_run_mail_again = Entry(Input_frame)
# et_run_mail_again.place(x=16, y=200, relwidth=0.4)

lb_thread = Label(Input_frame, text="S??? lu???ng: ")
lb_thread.place(x=16, y=330)
# et_thread = Entry(Input_frame)
# et_thread.place(x=16, y=400, relwidth=0.4)
variable_thread = StringVar(Input_frame)
variable_thread.set(1) # default value
et_thread = OptionMenu(Input_frame, variable_thread, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
et_thread.place(x=16, y=350, relwidth=0.2)

link_xuat_file = Label(Input_frame, text="T??n file: " + 'result-'+str(date.today())+'.txt')
link_xuat_file.place(x=120, y=350)


enter_new_password = Label(Input_frame, text="Nh???p m???t kh???u m???i n???u c???n: ")
enter_new_password.place(x=16, y=380)
enter_new_password_entry = Entry(Input_frame)
enter_new_password_entry.insert(0, r"Beta123ona.")
enter_new_password_entry.place(x=16, y=400, relwidth=0.8)

# ===========RESULT===================
lb_tong_cong = Label(screen, text="T???ng c???ng: ")
lb_tong_cong.place(x=32, rely=0.86)
lb_tong_cong_value = Label(screen, text="0 ", foreground='green', background='white')
lb_tong_cong_value.place(x=95, rely=0.86)

lb_da_chay = Label(screen, text="???? ch???y: ")
lb_da_chay.place(x=200, rely=0.86)
lb_da_chay_value = Label(screen, text="0 ", foreground='green', background='white')
lb_da_chay_value.place(x=250, rely=0.86)

lb_send = Label(screen, text="Send: ")
lb_send.place(x=350, rely=0.86)
lb_send_value = Label(screen, text="0 ", foreground='green', background='white')
lb_send_value.place(x=385, rely=0.86)

lb_inpro = Label(screen, text="Inpro: ")
lb_inpro.place(x=490, rely=0.86)
lb_inpro_value = Label(screen, text="0 ", foreground='yellow', background='white')
lb_inpro_value.place(x=525, rely=0.86)

lb_declined = Label(screen, text="Declined: ")
lb_declined.place(x=625, rely=0.86)
lb_declined_value = Label(screen, text="0 ", foreground='red', background='white')
lb_declined_value.place(x=680, rely=0.86)

lb_con_lai = Label(screen, text="C??n l???i: ")
lb_con_lai.place(x=780, rely=0.86)
lb_con_lai_value = Label(screen, text="0 ", foreground='green', background='white')
lb_con_lai_value.place(x=825, rely=0.86)
# ===========END RESULT===================

def input_record():
    global count
    table.insert(parent='',index='end',iid = count,text='',values=(file_mail_entry.get(),link_reward_entry.get(),mail_on_ip_entry.get()))
    count += 1

    file_mail_entry.delete(0,END)
    link_reward_entry.delete(0,END)
    mail_on_ip_entry.delete(0,END)

def read_file_email():
    global count
    file = open(file_mail_entry.get())
    try:
        count = 0
        for line in file:
            try:
                mail_read_list = line.split('|')
                mail_read_list[0] = mail_read_list[0].lower()
                mail_read_list[2] = mail_read_list[2].lower()
                mail_read_list[4] = mail_read_list[4].lower()

                # mail_read_list: [mail: 0, pass: 1, mail: 2, pass: 3, mail: 4, status: 5, count: 6, retry: 7]
                table_mails.append([mail_read_list[0],mail_read_list[1],mail_read_list[2],mail_read_list[3],mail_read_list[4], '', count, 0])

                table.insert(parent='',index='end',iid = count, text='', values=(count + 1, mail_read_list[0], mail_read_list[1]))
                
                count += 1
            except Exception as e:
                messagebox.showerror('?????c file l???i:', 'l???i t???i: ' + line)
                raise e
    except Exception as e:
        raise e


def update_start_button(state):
    if state == 'disabled':
        start_button.configure(state='disabled', bg='#c4c4c4', activeforeground='black')
    else:
        start_button.configure(state='normal', bg='green', activeforeground='white')

def update_stop_button(state):
    if state == 'disabled':
        stop_button.configure(state='disabled', bg='#c4c4c4', activeforeground='black')
    else:
        stop_button.configure(state='normal', bg='red', activeforeground='white')



def start(gp:GologinProfile, thread_data_index: int, mail):
    try:
        update_record(mail[6], "Ch???y l???n "+str(mail[7]))
        start_process(gp, token=gologin_token_entry.get(), reward_link=link_reward_entry.get(), sms_token=five_sim_token_entry.get(), thread_data_index=thread_data_index, mail_account_info=mail)
        if thread_data_list[thread_data_index]['thread']:
            try:
                thread_data_list[thread_data_index]['thread'].raise_exception()
            except:
                print('stop')
        thread_data_list[thread_data_index] = None
    except Exception as e:
        if not mail[5]:
            update_record(mail[6], "Ch??? th??? l???i")
            mail[5] = ''
        thread_data_list[thread_data_index]
        if thread_data_list[thread_data_index]['thread']:
            try:
                thread_data_list[thread_data_index]['thread'].raise_exception()
            except:
                print('stop')
        thread_data_list[thread_data_index] = None
        raise e

class StartThreadWithException(threading.Thread):
    def __init__(self, gp, thread_data_index, mail):
        threading.Thread.__init__(self)
        self.gp = gp
        self.thread_data_index = thread_data_index
        self.mail = mail

    def run(self):
        start(self.gp, self.thread_data_index, self.mail)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
            
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
            ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)


def update_threading():
    gp = GologinProfile({'token': gologin_token_entry.get(),
                'proxy_api_link': proxy_api_link_entry.get(),
                'max_mail_used': int(variable_mail_on_ip.get())
                })
    # Ki???m tra xem s??? l?????ng thread ??ang ch???y c?? ????? ch??a, n???u ch??a ????? th?? start ti???p, n???u ????? r???i th?? ch???
    while (True):
        print(thread_data_list)
        threadNumber = int(variable_thread.get())
        running = 0
        for t in thread_data_list:
            if t:
                running = running + 1
        mail_data = None
        if running < threadNumber:
            # T??m mail c???n ch???y
            for mail in table_mails:
                if (mail[5] == '' or mail[5] == None):
                    if mail[7] < int(variable.get()):
                        mail_data = mail
                        mail[7] = mail[7] + 1
                        break
                    else:
                        mail[5] = 'L???i'
                        update_record(mail[6], 'L???i')
            print(mail_data)
            if mail_data:
                for thread_data_index in range(10):
                    # L???y ra v??? tr?? ch??a ch???y thread ????? ch???y m???i 1 thread
                    if thread_data_list[thread_data_index] == None:
                        print('================== RUN MAIL ====================')
                        mail_data[5] = 'starting'
                        update_record(mail_data[6], 'starting')
                        new_thread = StartThreadWithException(gp, thread_data_index, mail_data)
                        # new_thread = Thread(target=start,args=[gp, thread_data_index, mail_data])
                        new_thread.start()
                        thread_data_list[thread_data_index] = {'thread': new_thread, 'driver': None, 'row': mail_data[6]}
                        break
        if running == 0 and mail_data == None:
            break
        time.sleep(3)
    messagebox.showinfo("Xong")
    if main_thread:
        main_thread.raise_exception()
class UpdateThreadWithException(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            update_threading()

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
            
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
def threading1():
    try:
        update_start_button('disabled')
        update_stop_button('active')
        global main_thread
        main_thread=UpdateThreadWithException()
        main_thread.start()
    except:
        if main_thread:
            main_thread.raise_exception()


def open_email_file():
    filename  = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('txt file', '*.txt')])
    file_mail_entry.delete(0, END)
    file_mail_entry.insert(0, filename)
    read_file_email()

def stop():
    for i in range(10):
        if thread_data_list[i]:
            try:
                # if thread_data_list[i]['driver']:
                #     # thread_data_list[i]['driver'].close()
                #     thread_data_list[i]['driver'].quit()
                if thread_data_list[i]['thread']:
                    thread_data_list[i]['thread'].raise_exception()
            except:
                print('Stop thread')
            update_record(thread_data_list[i]['row'], 'stop')
            thread_data_list[i] = None
    if main_thread:
        print('stop main thread')
        main_thread.raise_exception()
            
    update_start_button('active')
    # update_stop_button('disabled')
    

def export_result():
    print("RESULT")
    osCommandString = 'result-'+str(date.today())+'.txt'
    os.system(osCommandString)
    # update_record()

def update_record(index: int, status: str):
   table.set(index, column='3', value=status)

# Result string:
# Kind string: Send, Declined, Inpro, Loi
def write_file(result, kind):
    logging.basicConfig(filename=kind+'-'+str(date.today())+'.txt', format="%(message)s")
    logging.fatal(result)

# ============BUTTON===============
open_file = Button(Input_frame, text = "M??? file email", bg='#f2f2f2', activeforeground='white', command= open_email_file)
open_file.place(relx=.605, y=46, relwidth=.23)

start_button = Button(Input_frame, text = "Start", bg='green', activeforeground='white', command= threading1)
start_button.place(relx=.1, rely=0.9, relwidth=.2)

stop_button = Button(Input_frame, text = "Stop", bg='#c4c4c4', activeforeground='black', state='disabled',command= stop)
stop_button.place(relx=.4, rely=0.9, relwidth=.2)

result_button = Button(Input_frame, text = "K???t qu???", bg='#f2f2f2', activeforeground='white', command= export_result)
result_button.place(relx=.7, rely=0.9, relwidth=.2)
# ============END BUTTON===============

# screen.mainloop()

def get_element(driver, by, data, raise_error=True):
    retry_time = 0
    while retry_time < 20:
        if len(driver.find_elements(by, data)) != 0:
            return driver.find_element(by, data)
        time.sleep(1)
        retry_time=retry_time+1
    if raise_error:
        raise TimeoutException('Timeout')
    return False
        

# Code open link
def start_process(gp: GologinProfile, token: str, reward_link: str, sms_token: str, thread_data_index: int,mail_account_info = []):
    gl = None
    try:
        update_record(mail_account_info[6], 'T???o profile')
        mail_account_info[5] = 'T???o profile'
        profile_id = gp.create_profile()
        if profile_id == False:
            mail_account_info[5] = ''
            update_record(mail_account_info[6], 'Khong tao duoc profile')
        gl = GoLogin({'token': token, 'profile_id': profile_id, 'port': getRandomPort()})
        
        debugger_address = gl.start()
        print('main address: ' + str(debugger_address))
        update_record(mail_account_info[6], 'M??? Gologin')
        mail_account_info[5] = 'M??? Gologin'
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", debugger_address)
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

        thread_data_list[thread_data_index]['driver'] = driver

        driver.get(reward_link)
        print("Wait the page reward open!")
        update_record(mail_account_info[6], 'M??? trang reward')
        mail_account_info[5] = 'M??? trang reward'
        signUpButton: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'start-earning-rewards-link')))
        print("Page is ready!")
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(signUpButton))
        print("Sign Up button is ready!")
        time.sleep(2)
        signUpButton.click()

        update_record(mail_account_info[6], 'Nh???p mail ch??nh')
        mail_account_info[5] = 'Nh???p mail ch??nh'
        print("Entering email...")
        emailInput: WebElement = get_element(driver=driver, by=By.NAME, data='loginfmt')
        emailInput.send_keys(mail_account_info[0])
        time.sleep(3)
        nextButton = get_element(driver=driver, by=By.CSS_SELECTOR, data='[type="submit"]')
        nextButton.click()

        update_record(mail_account_info[6], 'Nh???p pass mail ch??nh')
        mail_account_info[5] = 'Nh???p pass mail ch??nh'
        print("Entering password...")
        passwordInput: WebElement = get_element(driver=driver, by=By.NAME, data='passwd')
        passwordInput.send_keys(mail_account_info[1])
        time.sleep(3)
        signInButton: WebElement = get_element(driver=driver, by=By.CSS_SELECTOR, data='[type="submit"]')
        signInButton.click()

        if get_element(driver=driver, by=By.CSS_SELECTOR, data='.pull-left > .win-color-fg-alert', raise_error=False):
            write_file('|'.join(mail_account_info[0:5])+'|'+'Kh??ng ????? ??i???m', 'Loi')
            update_record(mail_account_info[6], "kh??ng ????? ??i???m")
            mail_account_info[5] = 'kh??ng ????? ??i???m'
            driver.close()
            driver.quit()
            if gl:
                gl.delete_profile_folder()
            return

        if get_element(driver=driver, by=By.ID, data='redeem-checkout-review-confirm', raise_error=False) == False:
            tmp_button = get_element(driver=driver, by=By.ID, data='iLandingViewAction', raise_error=False)
            if tmp_button:
                tmp_button.click()
            tmp_button = get_element(driver=driver, by=By.ID, data='iProof0', raise_error=False)
            if tmp_button:
                tmp_button.click()
            tmp_button = get_element(driver=driver, by=By.ID, data='idSIButton9', raise_error=False)
            if tmp_button:
                tmp_button.click()
            tmp_button = get_element(driver=driver, by=By.ID, data='passwordError', raise_error=False)
            if tmp_button:
                update_record(mail_account_info[6], 'Sai password')
                mail_account_info[5] = 'Sai password'
                write_file('|'.join(mail_account_info[0:5])+'|'+'Sai password', 'Loi')
                raise 'Sai password'

            if get_element(driver=driver, by=By.CSS_SELECTOR, data='.pull-left > .win-color-fg-alert', raise_error=False):
                write_file('|'.join(mail_account_info[0:5])+'|'+'Kh??ng ????? ??i???m', 'Loi')
                update_record(mail_account_info[6], "kh??ng ????? ??i???m")
                mail_account_info[5] = 'kh??ng ????? ??i???m'
                driver.close()
                driver.quit()
                if gl:
                    gl.delete_profile_folder()
                return
            
            if get_element(driver=driver, by=By.ID, data='redeem-checkout-review-confirm', raise_error=False) == False:
                update_record(mail_account_info[6], 'L???y code t??? mail ph???')
                mail_account_info[5] = 'L???y code t??? mail ph???'
                get_element(driver=driver, by=By.ID, data='iProofEmail').send_keys(mail_account_info[2])
                time.sleep(2)
                get_element(driver=driver, by=By.ID, data='iSelectProofAction').click()
                time.sleep(2)
                tmp = get_element(driver=driver, by=By.ID, data='iSelectProofError', raise_error=False)
                time.sleep(2)
                if tmp:
                    tmp.click()
                    return

                update_record(mail_account_info[6], 'Get code t??? mail ph???')
                mail_account_info[5] = 'Get code t??? mail ph???'
                code = get_verify_code(gp, token, mail_account_info[2], mail_account_info[3], mail_account_info[4], mail_account_info)
                get_element(driver=driver, by=By.ID, data='iOttText').send_keys(code)
                time.sleep(1)
                get_element(driver=driver, by=By.ID, data='iVerifyCodeAction').click()
                time.sleep(10)
                
                if len(driver.find_elements(By.ID, 'iVerifyCodeError')) != 0:
                    update_record(mail_account_info[6], 'Get code t??? mail ph??? l???n 2')
                    mail_account_info[5] = 'Get code t??? mail ph??? l???n 2'
                    code = get_verify_code(gp, token, mail_account_info[2], mail_account_info[3], mail_account_info[4], mail_account_info)
                    temp = get_element(driver=driver, by=By.ID, data='iOttText')
                    temp.clear()
                    temp.send_keys(code)
                    time.sleep(1)
                    get_element(driver=driver, by=By.ID, data='iVerifyCodeAction').click()
                    time.sleep(10)
                            
                if len(driver.find_elements(By.ID, 'iVerifyCodeError')) != 0:
                    temp = get_element(driver=driver, by=By.ID, data='iOttText')
                    temp.clear()
                    temp.send_keys(code)
                    time.sleep(1)
                    get_element(driver=driver, by=By.ID, data='iVerifyCodeAction').click()
                    time.sleep(10)

                if len(driver.find_elements(By.ID, 'iVerifyCodeError')) != 0:
                    update_record(mail_account_info[6], 'L???i')
                    mail_account_info[5] = 'L???i'
                    write_file('|'.join(mail_account_info[0:5])+'|'+'L???i l???y code t??? mail ph???', 'Loi')
                    raise 'L???i l???y code t??? mail ph???'
    
                if get_element(driver=driver, by=By.ID, data='iPassword', raise_error=False):
                    update_record(mail_account_info[6], 'Nh???p m???t kh???u m???i')
                    mail_account_info[5] = 'Nh???p m???t kh???u m???i'
                    new_pass = enter_new_password_entry.get()
                    print(new_pass)
                    pass_new_input = driver.find_element(By.ID, 'iPassword')
                    pass_new_input.send_keys(new_pass)
                    mail_account_info[1] = new_pass
                    time.sleep(3)
                    driver.find_element(By.ID, 'iPasswordViewAction').click()
                    

        if get_element(driver=driver, by=By.CSS_SELECTOR, data='.pull-left > .win-color-fg-alert', raise_error=False):
            print('Khong du diem')
            update_record(mail_account_info[6], 'Kh??ng ????? ??i???m')
            mail_account_info[5] = 'Kh??ng ????? ??i???m'
            write_file('|'.join(mail_account_info[0:5])+'|'+'Kh??ng ????? ??i???m', 'Loi')
            raise 'Kh??ng ????? ??i???m'

        print('=======reward=======')
        update_record(mail_account_info[6], 'Ch??? reward')
        mail_account_info[5] = 'Ch??? reward'
        confirmRewardButton: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'redeem-checkout-review-confirm')))
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(confirmRewardButton))
        print("Reward button is ready!")
        confirmRewardButton.click()
        sms = Sms({'token': sms_token})
        update_record(mail_account_info[6], 'Ch??? l???y sim 5sim')
        mail_account_info[5] = 'Ch??? l???y sim 5sim'
        phoneRes = sms.order_5sim()
        update_record(mail_account_info[6], 'reward')
        phoneInput: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'redeem-checkout-challenge-fullnumber')))
        print("Phone input is ready!")
        phoneInput.send_keys(phoneRes.get('phone', '').replace('+1', ''))

        sendButton: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'redeem-checkout-challenge-validate')))
        print("Send OTP button is ready!")
        sendButton.click()
        update_record(mail_account_info[6], 'Ch??? l???y code 5sim')
        mail_account_info[5] = 'Ch??? l???y code 5sim'
        code = sms.get_code_5sim(phoneRes.get('id', ''))

        codeInput: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'redeem-checkout-challenge-code')))
        print("Enter your 6-digit code:")
        codeInput.send_keys(code)
        completeMyOrderBtn: WebElement = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'redeem-checkout-challenge-confirm')))
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(completeMyOrderBtn))
        print("completeMyOrderBtn is ready!")
        update_record(mail_account_info[6], 'Reward...')
        mail_account_info[5] = 'Reward...'
        completeMyOrderBtn.click()
    except TimeoutException:
        mail_account_info[5] = ''
        update_record(mail_account_info[6], 'Ch??? th??? l???i')
        driver.close()
        driver.quit()
        gl.delete_profile_folder()
    except Exception as e:
        mail_account_info[5] = ''
        update_record(mail_account_info[6], 'Ch??? th??? l???i')
        driver.close()
        driver.quit()
        if gl:
            gl.delete_profile_folder()
        raise e

def get_verify_code(gp: GologinProfile, token: str, mail: str, password: str, mail_verify: str,mail_account_info = []):
    # hotmail login link: https://outlook.live.com/owa/?nlp=1
    gl = None
    try:
        update_record(mail_account_info[6], 'T???o profile cho mail ph???')
        mail_account_info[5] = 'T???o profile cho mail ph???'
        profile_id = gp.create_profile()
        gl = GoLogin({'token': token, 'profile_id': profile_id,  'port': getRandomPort()})
        debugger_address = gl.start()
        print(debugger_address)
        update_record(mail_account_info[6], 'M??? tr??nh duy???t cho mail ph???')
        mail_account_info[5] = 'M??? tr??nh duy???t cho mail ph???'
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", debugger_address)
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        driver.get('https://outlook.live.com/owa/?nlp=1')
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
        update_record(mail_account_info[6], 'Login mail ph???')
        mail_account_info[5] = 'Login mail ph???'
        driver.find_element(By.NAME, 'loginfmt').send_keys(mail)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        time.sleep(3)
        driver.find_element(By.NAME, 'passwd').send_keys(password)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        retry_time = 0
        allow_continue = False
        step = ''
        while(retry_time < 10):
            if len(driver.find_elements(By.ID, 'iLandingViewAction')) != 0:
                allow_continue = True
                print(driver.find_elements(By.ID, 'iLandingViewAction').count)
                step = 'landingiew'
                break
            elif len(driver.find_elements(By.ID, 'iProof0')) != 0:
                allow_continue = True
                step = 'chosemailverify'
                break
            elif len(driver.find_elements(By.ID, 'idSIButton9')) != 0:
                allow_continue = True
                step = 'staysigned'
                break
            elif len(driver.find_elements(By.ID, 'passwordError')) != 0:
                # TODO: X??? l?? sai pass
                print('Sai password')
                update_record(mail_account_info[6], 'L???i: Sai pass mail ph???')
                mail_account_info[5] = 'L???i: Sai pass mail ph???'
                # driver.close()
                raise 'Sai password'
            time.sleep(6)
            retry_time = retry_time + 1

        if (allow_continue == False):
            print('false at allow_continue')
            raise('false at allow_continue')
        
        if (step == 'landingiew'):
            print('Landing View V2')
            driver.find_elements(By.ID, 'iLandingViewAction')[0].click()
            time.sleep(3)

        if (step == 'staysigned'):
            print(len(driver.find_elements(By.ID, 'idSIButton9')))
            driver.find_elements(By.ID, 'idSIButton9')[0].click()
        
        if len(driver.find_elements(By.ID, 'iProof0')):
            driver.find_element(By.ID, 'iProof0').click()
            time.sleep(3)
        if len(driver.find_elements(By.ID, 'iProofEmail')):
            driver.find_element(By.ID, 'iProofEmail').send_keys(mail_verify)
            time.sleep(3)
        if len(driver.find_elements(By.ID, 'iSelectProofAction')):
            driver.find_element(By.ID, 'iSelectProofAction').click()
            time.sleep(3)
        start_verify_time = int(time.time())
        update_record(mail_account_info[6], 'Ch??? l???y code t??? mailnesia')
        mail_account_info[5] = 'Ch??? l???y code t??? mailnesia'
        code = get_code_from_mailnesia(mail_verify, 0)
        update_record(mail_account_info[6], 'Code mailnesia: ' + str(code))
        mail_account_info[5] = 'Code mailnesia: ' + str(code)
        if  len(driver.find_elements(By.ID, 'iOttText')):
            time.sleep(3)
            driver.find_element(By.ID, 'iOttText').send_keys(code)
            time.sleep(3)
            driver.find_element(By.ID, 'iVerifyCodeAction').click()
            # Ch??? cho ?????n khi c??
        if(len(driver.find_elements(By.ID, 'idSIButton9'))):
            yButton: WebElement = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
            time.sleep(3)
            yButton.click()
        update_record(mail_account_info[6], 'Ch??? l???y code t??? mail ph???')
        mail_account_info[5] = 'Ch??? l???y code t??? mail ph???'
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="listbox"]')))
        driver.find_element(By.ID, 'Pivot84-Tab1').click()
        time.sleep(3)
        
        retry_time = 0
        while(retry_time < 15):
            list_mail = driver.find_elements(By.CLASS_NAME, 'hcptT')
            print(list_mail)
            for mail in list_mail:
                result = re.findall(r'[0-9]{7}', mail.get_attribute('aria-label'))
                if (result):
                    code = result[0]
                    print(code)
                    driver.close()
                    driver.quit()
                    gl.delete_profile_folder()
                    return code
            time.sleep(6)
            retry_time = retry_time+1
        update_record(mail_account_info[6], 'L???i: kh??ng l???y ???????c code t??? mail ph???')
        mail_account_info[5] = 'L???i: kh??ng l???y ???????c code t??? mail ph???'
        driver.close()
        driver.quit()
        gl.delete_profile_folder()
        raise('Can not get code from mail hotmail')
    except Exception as e:
        if gl:
            driver.close()
            driver.quit()
            gl.delete_profile_folder()
        raise e

