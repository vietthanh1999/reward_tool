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

timeout = 50
sleep_affter_click = 3

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
gologin_token_entry.insert(0, r"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2U4ZTE1ZmVhMGEzZGU2Y2FiMTJiMDQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2U4ZTFiMTkyYjg1OWFhNWNkNjhiODUifQ.qJGQvR_SnNJN6NUQPc9XdLBVlQrDg27f88u7akj1jVg")
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

lb_run_mail_again = Label(Input_frame, text="Số lần chạy lại mail:")
lb_run_mail_again.place(x=120, y=280)

variable = StringVar(Input_frame)
variable.set(1) # default value
et_run_mail_again = OptionMenu(Input_frame, variable, 1, 2, 3)
et_run_mail_again.place(x=120, y=300, relwidth=0.2)
# et_run_mail_again = Entry(Input_frame)
# et_run_mail_again.place(x=16, y=200, relwidth=0.4)

lb_thread = Label(Input_frame, text="Số luồng: ")
lb_thread.place(x=16, y=330)
# et_thread = Entry(Input_frame)
# et_thread.place(x=16, y=400, relwidth=0.4)
variable_thread = StringVar(Input_frame)
variable_thread.set(1) # default value
et_thread = OptionMenu(Input_frame, variable_thread, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
et_thread.place(x=16, y=350, relwidth=0.2)

link_xuat_file = Label(Input_frame, text="Tên file: " + 'result-'+str(date.today())+'.txt')
link_xuat_file.place(x=120, y=350)


enter_new_password = Label(Input_frame, text="Nhập mật khẩu mới nếu cần: ")
enter_new_password.place(x=16, y=380)
enter_new_password_entry = Entry(Input_frame)
enter_new_password_entry.insert(0, r"Beta123ona.")
enter_new_password_entry.place(x=16, y=400, relwidth=0.8)

# ===========RESULT===================
lb_tong_cong = Label(screen, text="Tổng cộng: ")
lb_tong_cong.place(x=32, rely=0.86)
lb_tong_cong_value = Label(screen, text="0 ", foreground='green', background='white')
lb_tong_cong_value.place(x=95, rely=0.86)

lb_da_chay = Label(screen, text="Đã chạy: ")
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

lb_con_lai = Label(screen, text="Còn lại: ")
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
                # mail_read_list: [mail, pass, mail, pass, mail, status, count]
                mail_read_list = line.split('|')
                mail_read_list[0] = mail_read_list[0].lower()
                mail_read_list[2] = mail_read_list[2].lower()
                mail_read_list[4] = mail_read_list[4].lower()

                table_mails.append([mail_read_list[0],mail_read_list[1],mail_read_list[2],mail_read_list[3],mail_read_list[4], '', count])

                table.insert(parent='',index='end',iid = count, text='', values=(count + 1, mail_read_list[0], mail_read_list[1]))
                
                count += 1
            except Exception as e:
                messagebox.showerror('Đọc file lỗi:', 'lỗi tại: ' + line)
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
        start_process(gp, token=gologin_token_entry.get(), reward_link=link_reward_entry.get(), sms_token=five_sim_token_entry.get(), thread_data_index=thread_data_index, mail_account_info=mail)
        # set trang thai cho row
    except Exception as e:
        # set trang thai cho row
        update_record(mail[6], "Lỗi")
        raise e
    # finally:
    #     if thread_data_list[thread_data_index]:
    #         if thread_data_list[thread_data_index]['driver']:
    #             thread_data_list[thread_data_index]['driver'].close()
    #         if thread_data_list[thread_data_index]['thread']:
    #             thread_data_list[thread_data_index]['thread'].join()
    #         thread_data_list[thread_data_index] = None

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
    # Kiểm tra xem số lượng thread đang chạy có đủ chưa, nếu chưa đủ thì start tiếp, nếu đủ rồi thì chờ
    while (True):
        print(thread_data_list)
        threadNumber = int(variable_thread.get())
        running = 0
        for t in thread_data_list:
            if t:
                running = running + 1
        mail_data = None
        if running < threadNumber:
            # Tìm mail cần chạy
            for mail in table_mails:
                if mail[5] == '' or mail[5] == None:
                    mail_data = mail
                    break
            print(mail_data)
            if mail_data:
                for thread_data_index in range(10):
                    # Lấy ra vị trí chưa chạy thread để chạy mới 1 thread
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

def write_file(result):
    logging.basicConfig(filename='result-'+str(date.today())+'.txt', format="%(message)s")
    logging.fatal(result)

# ============BUTTON===============
open_file = Button(Input_frame, text = "Mở file email", bg='#f2f2f2', activeforeground='white', command= open_email_file)
open_file.place(relx=.605, y=46, relwidth=.23)

start_button = Button(Input_frame, text = "Start", bg='green', activeforeground='white', command= threading1)
start_button.place(relx=.1, rely=0.9, relwidth=.2)

stop_button = Button(Input_frame, text = "Stop", bg='#c4c4c4', activeforeground='black', state='disabled',command= stop)
stop_button.place(relx=.4, rely=0.9, relwidth=.2)

result_button = Button(Input_frame, text = "Kết quả", bg='#f2f2f2', activeforeground='white', command= export_result)
result_button.place(relx=.7, rely=0.9, relwidth=.2)
# ============END BUTTON===============

# screen.mainloop()

# Code open link
def start_process(gp: GologinProfile, token: str, reward_link: str, sms_token: str, thread_data_index: int,mail_account_info = []):
    update_record(mail_account_info[6], 'Tạo profile')
    profile_id = gp.create_profile()
    gl = GoLogin({'token': token, 'profile_id': profile_id, 'port': getRandomPort()})
    debugger_address = gl.start()
    print('main address: ' + str(debugger_address))
    update_record(mail_account_info[6], 'Mở Gologin')
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    thread_data_list[thread_data_index]['driver'] = driver

    driver.get(reward_link)
    # try:
    print("Wait the page reward open!")
    update_record(mail_account_info[6], 'Mở trang reward')
    signUpButton: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'start-earning-rewards-link')))
    print("Page is ready!")
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(signUpButton))
    print("Sign Up button is ready!")
    signUpButton.click()

    update_record(mail_account_info[6], 'Nhập mail chính')
    print("Entering email...")
    emailInput: WebElement = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
    time.sleep(3)
    emailInput.send_keys(mail_account_info[0])
    time.sleep(sleep_affter_click)
    nextButton: WebElement = driver.find_element(
        By.CSS_SELECTOR, '[type="submit"]')
    nextButton.click()

    time.sleep(sleep_affter_click)
    update_record(mail_account_info[6], 'Nhập pass mail chính')
    print("Entering password...")
    passwordInput: WebElement = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.NAME, 'passwd')))
    time.sleep(sleep_affter_click)
    passwordInput.send_keys(mail_account_info[1])
    time.sleep(sleep_affter_click)
    signInButton: WebElement = driver.find_element(By.CSS_SELECTOR, '[type="submit"]')
    signInButton.click()

    # Check passwork error

    if len(driver.find_elements(By.ID, 'redeem-checkout-review-confirm')) == 0:
        time.sleep(5)
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
                # TODO: Xử lý sai pass
                print('Sai password')
                update_record(mail_account_info[6], 'Sai password')
                raise 'Sai password'
            time.sleep(6)
            retry_time = retry_time + 1

        if (allow_continue == False):
            update_record(mail_account_info[6], 'Lỗi: Không xác định được phần tử tiếp theo')
            logging.error('Lỗi: Không xác định được phần tử tiếp theo' + str(mail_account_info))
            print('false at allow_continue')
            raise('false at allow_continue')
            
        if (step == 'landingiew'):
            print('Landing View V2')
            driver.find_elements(By.ID, 'iLandingViewAction')[0].click()
            time.sleep(3)

        update_record(mail_account_info[6], 'Chờ lấy code từ mail phụ')
        if (step == 'staysigned'):
            print(len(driver.find_elements(By.ID, 'idSIButton9')))
            driver.find_elements(By.ID, 'idSIButton9')[0].click()
        
        if len(driver.find_elements(By.ID, 'iProof0')):
            driver.find_element(By.ID, 'iProof0').click()
            time.sleep(3)
        if len(driver.find_elements(By.ID, 'iProofEmail')):
            driver.find_element(By.ID, 'iProofEmail').send_keys(mail_account_info[2])
            time.sleep(3)
        if len(driver.find_elements(By.ID, 'iSelectProofAction')):
            driver.find_element(By.ID, 'iSelectProofAction').click()
            time.sleep(3)

        if len(driver.find_elements(By.ID, 'iSelectProofError')):
            # driver.find_element(By.ID, 'iSelectProofAction').click()
            update_record(mail_account_info[6],  'Requested too many codes today')
            thread_data_list[thread_data_index]['thread'].raise_exception()
            driver.quit()

        start_verify_time = int(time.time())
        print('=======GET CODE=======')
        if len(driver.find_elements(By.ID, 'redeem-checkout-review-confirm')) == 0:
            update_record(mail_account_info[6], 'Get code từ mail phụ')
            code = get_verify_code(gp, token, mail_account_info[2], mail_account_info[3], mail_account_info[4], mail_account_info)
            driver.find_element(By.ID, 'iOttText').send_keys(code)
            time.sleep(3)
            driver.find_element(By.ID, 'iVerifyCodeAction').click()

        if len(driver.find_elements(By.ID, 'iPasswordText')) != 0:
            update_record(mail_account_info[6], 'Nhập mật khẩu mới')
            new_pass = enter_new_password_entry.get()
            print(new_pass)
            pass_new_input = driver.find_element(By.ID, 'iPasswordText')
            pass_new_input.send_keys(new_pass)
            time.sleep(3)
            driver.find_element(By.ID, 'iPasswordViewAction').click()

    # TODO: Xử lý reward
    if len(driver.find_elements(By.CSS_SELECTOR, '.pull-left > .win-color-fg-alert')) != 0: 
        print('Khong du diem')
        update_record(mail_account_info[6], 'Không đủ điểm')
        # TODO: xuất giá trị ra file
        # driver.quit()

    print('=======reward=======')
    update_record(mail_account_info[6], 'Chờ reward')
    confirmRewardButton: WebElement = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'redeem-checkout-review-confirm')))
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(confirmRewardButton))
    print("Reward button is ready!")
    confirmRewardButton.click()
    sms = Sms({'token': sms_token})
    update_record(mail_account_info[6], 'Chờ lấy sim 5sim')
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
    update_record(mail_account_info[6], 'Chờ lấy code 5sim')
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
    completeMyOrderBtn.click()

        # elif ()
        # elif():
        #     # TODO: Xử lý trường hợp mail lock
        # elif (driver.find_elements(By.CSS_SELECTOR, '.pull-left > .win-color-fg-alert').count != 0):
        #     print('Khong du diem')
        #     driver.close()
        #     raise 'Khong du diem'

        
        # get_verify_code()
    # except TimeoutException:
    #     # TODO: Xử lý trường hợp proxy chậm
    #     print("Loading took too much time!")
    # except:
    #     print("Error to login")

def get_verify_code(gp: GologinProfile, token: str, mail: str, password: str, mail_verify: str,mail_account_info = []):
    # hotmail login link: https://outlook.live.com/owa/?nlp=1
    update_record(mail_account_info[6], 'Tạo profile cho mail phụ')
    profile_id = gp.create_profile()
    gl = GoLogin({'token': token, 'profile_id': profile_id,  'port': getRandomPort()})
    debugger_address = gl.start()
    print(debugger_address)
    update_record(mail_account_info[6], 'Mở trình duyệt cho mail phụ')
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.get('https://outlook.live.com/owa/?nlp=1')
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
    update_record(mail_account_info[6], 'Login mail phụ')
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
            # TODO: Xử lý sai pass
            print('Sai password')
            update_record(mail_account_info[6], 'Lỗi: Sai pass mail phụ')
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
    update_record(mail_account_info[6], 'Chờ lấy code từ mailnesia')
    code = get_code_from_mailnesia(mail_verify, 0)
    update_record(mail_account_info[6], 'Code mailnesia: ' + str(code))
    if  len(driver.find_elements(By.ID, 'iOttText')):
        time.sleep(3)
        driver.find_element(By.ID, 'iOttText').send_keys(code)
        time.sleep(3)
        driver.find_element(By.ID, 'iVerifyCodeAction').click()
        # Chờ cho đến khi có
    if(len(driver.find_elements(By.ID, 'idSIButton9'))):
        yButton: WebElement = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'idSIButton9')))
        time.sleep(3)
        yButton.click()
    update_record(mail_account_info[6], 'Chờ lấy code từ mail phụ')
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
                # driver.close()
                return code
        time.sleep(6)
        retry_time = retry_time+1
    update_record(mail_account_info[6], 'Lỗi: không lấy được code từ mail phụ')
    driver.quit()
    gl.delete_profile_folder()
    raise('Can not get code from mail hotmail')

# DomekIvyanne@outlook.com|P7C0vUrEfAn|JamesHarrison175@hotmail.com|TXdqs19oy13WZ|jamesharrison175@mailnesia.com
# start_process(gp, token, reward_link="https://rewards.microsoft.com/redeem/checkout?productId=000800000041", 
# mail_account_info=['allemandHaasini@outlook.com', 'Beta123ona.', 'busterFraise154@hotmail.com', 'NIfgd15k19YB', 'busterfraise154@mailnesia.com'])

# start_process(gp, token, reward_link="https://rewards.microsoft.com/redeem/checkout?productId=000800000041", 
# mail_account_info=['domekIvyanne@outlook.com', 'P7C0vUrEfAn', 'jamesHarrison175@hotmail.com', 'TXdqs19oy13WZ', 'jamesharrison175@mailnesia.com'])

# start_process(gp, token, reward_link="https://rewards.microsoft.com/redeem/checkout?productId=000800000041", 
# mail_account_info=['lemmerkhayq@outlook.com', 'Beta123ona.', 'kellyBurgos187@hotmail.com', 'AVwsd17h17MV', 'kellyburgos187@mailnesia.com'])