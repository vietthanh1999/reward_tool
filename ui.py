import logging
import time
import ctypes
import threading
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from runchrome import start_process
from gologinprofile import GologinProfile
from datetime import date
from globaldata import thread_data_list, main_thread


logging.basicConfig(filename='log-'+str(date.today())+'.txt', format="%(asctime)s %(message)s")

screen=Tk()
# screen.withdraw()
screen.title('Reward Tool')
screen.geometry('980x620')


def handle_exception(exception, value, traceback):
    logging.error(str(exception)+str(value)+str(traceback))
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
five_sim_token_entry.insert(0, r"eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTMxOTQ1MTEsImlhdCI6MTY2MTY1ODUxMSwicmF5IjoiNmM3MzhlZTI1OTA2N2RlNjY5M2U4YTQwZGY0NDgzNDAiLCJzdWIiOjEyMjQ1NzR9.aDurMb5mPDBsTJAEmKSpjfBIRx8xsU5MU8-W-_TchLr1r2bEOjTXx6rNRVtLgXjba7h8VYGCq6EuisPFQy4IsWuanlFgqsv8eHkkmdBV9GyAn-iRbpwsh9YSP2yTZuxzSAhNXtABcORlxzWKjmSyPCNDv4wLpe4tcVUBSIFBzd5QlfiAXxpIPRmnLDamIW5D1cT9t6k_wwaWqFauvPiaUMe_mI-keF_GTV1zFYkukexB4EIucJmbEVuTQ_oXQCnUzRXWa8bi7gTEAgjmdWCm3xU53qoDvsHhtjVmS1Iu1rLbpnEwHJJUiAafQaY_c0IiZQtFDpvdWDBSvN4CK0RfEg'")
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
lb_run_mail_again.place(x=16, y=330)

variable = StringVar(Input_frame)
variable.set(1) # default value
et_run_mail_again = OptionMenu(Input_frame, variable, 1, 2, 3)
et_run_mail_again.place(x=16, y=350, relwidth=0.2)
# et_run_mail_again = Entry(Input_frame)
# et_run_mail_again.place(x=16, y=200, relwidth=0.4)

lb_thread = Label(Input_frame, text="Số luồng: ")
lb_thread.place(x=16, y=380)
# et_thread = Entry(Input_frame)
# et_thread.place(x=16, y=400, relwidth=0.4)
variable_thread = StringVar(Input_frame)
variable_thread.set(1) # default value
et_thread = OptionMenu(Input_frame, variable_thread, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
et_thread.place(x=16, y=400, relwidth=0.2)

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
    print('START')
    try:
        start_process(gp, token=gologin_token_entry.get(), reward_link=link_reward_entry.get(), sms_token=five_sim_token_entry.get(), thread_data_index=thread_data_index, mail_account_info=mail)
        # set trang thai cho row
    except:
        # set trang thai cho row
        update_record(0, "Lỗi")
        print('errrorrr====')
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
        print('Exception raise')
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


def update_threading():
    gp = GologinProfile({'token': gologin_token_entry.get(),
                'proxy_api_link': proxy_api_link_entry.get(),
                'max_mail_used': int(variable_mail_on_ip.get())
                })
    # Kiểm tra xem số lượng thread đang chạy có đủ chưa, nếu chưa đủ thì start tiếp, nếu đủ rồi thì chờ
    while (True):
        threadNumber = int(variable_thread.get())
        print(threadNumber)
        print(thread_data_list)
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
                        print(mail_data)
                        mail_data[5] = 'starting'
                        update_record(mail_data[6], 'starting')
                        new_thread = StartThreadWithException(gp, thread_data_index, mail_data)
                        # new_thread = Thread(target=start,args=[gp, thread_data_index, mail_data])
                        new_thread.start()
                        thread_data_list[thread_data_index] = {'thread': new_thread, 'driver': None}
                        break
        if running == 0 and mail_data == None:
            break
        time.sleep(3)
    messagebox.showinfo("Xong")
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
        print('Exception raise')
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
def threading1():
    update_start_button('disabled')
    update_stop_button('active')
    global main_thread
    main_thread=UpdateThreadWithException()
    main_thread.start()


def open_email_file():
    filename  = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('txt file', '*.txt')])
    file_mail_entry.delete(0, END)
    file_mail_entry.insert(0, filename)
    read_file_email()

def stop():
    print(thread_data_list)
    for i in range(10):
        if thread_data_list[i]:
            print('=================== STOP ================')
            print(thread_data_list[i])
            print('=================== STOP ================')
            if thread_data_list[i]['driver']:
                # thread_data_list[i]['driver'].close()
                thread_data_list[i]['driver'].quit()
            if thread_data_list[i]['thread']:
                thread_data_list[i]['thread'].raise_exception()
            thread_data_list[i] = None
    if main_thread:
        print('stop main thread')
        main_thread.raise_exception()
    print(thread_data_list)
            
    update_start_button('active')
    # update_stop_button('disabled')
    

def export_result():
    print("RESULT")
    update_record()

def update_record(index: int, status: str):
   table.set(index, column='3', value=status)

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


