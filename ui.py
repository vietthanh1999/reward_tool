from tkinter import *
from tkinter import ttk

screen=Tk()
screen.title('Reward Tool')
screen.geometry('980x620')

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
file_mail_entry.insert(0, r"C:\Users\Thanh\Desktop\gologin\toolReg\emails.txt")
file_mail_entry.place(x=16, y=50, relwidth=0.8)

link_reward= Label(Input_frame, text="Link reward: ")
link_reward.place(x=16, y=80)
link_reward_entry = Entry(Input_frame)
link_reward_entry.insert(0, r"https://rewards.microsoft.com/redeem/checkout?productId=000800000041")
link_reward_entry.place(x=16, y=100, relwidth=0.8)

mail_on_ip = Label(Input_frame, text="Mail/1IP: ")
mail_on_ip.place(x=16, y=130)
variable_mail_on_ip = StringVar(Input_frame)
variable_mail_on_ip.set(1) # default value
mail_on_ip_entry = OptionMenu(Input_frame, variable_mail_on_ip, 1, 2, 3, 4, 5)
mail_on_ip_entry.place(x=16, y=150, relwidth=0.2)
# mail_on_ip_entry = Entry(Input_frame)
# mail_on_ip_entry.place(x=16, y=150, relwidth=0.4)

lb_run_mail_again = Label(Input_frame, text="So lan chay lai mail")
lb_run_mail_again.place(x=16, y=180)

variable = StringVar(Input_frame)
variable.set(1) # default value
et_run_mail_again = OptionMenu(Input_frame, variable, 1, 2, 3)
et_run_mail_again.place(x=16, y=200, relwidth=0.2)
# et_run_mail_again = Entry(Input_frame)
# et_run_mail_again.place(x=16, y=200, relwidth=0.4)

lb_thread = Label(Input_frame, text="Luong: ")
lb_thread.place(x=16, y=230)
et_thread = Entry(Input_frame)
et_thread.place(x=16, y=250, relwidth=0.4)

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
    for line in file:
        mail_read_list = line.split('|')
        index = 0
        temp_list = []
        for mail in mail_read_list:
            temp_list.append(mail)
            if (index % 2 != 0 and len(temp_list) == 2):
                table_mails.append(temp_list)
                table.insert(parent='',index='end',iid = count, text='', values=(count + 1, temp_list[0], temp_list[1]))
                count += 1
                temp_list = []

            index = index + 1

def start():
    print('START')
    # read_file_email()

def stop():
    print('STOP')
    print(table_mails)

def export_result():
    print("RESULT")
    update_record()

def update_record():
   # Get selected item to Edit
   selected_item = table.selection()[0]
   print(selected_item)
   table.item(selected_item, text="blub", values=("1", "foo", "bar"))

# ============BUTTON===============
start_button = Button(Input_frame, text = "Start", bg='green', activeforeground='white', command= start)
start_button.place(relx=.1, rely=0.9, relwidth=.2)

stop_button = Button(Input_frame, text = "Stop", bg='red', activeforeground='white', command= stop)
stop_button.place(relx=.4, rely=0.9, relwidth=.2)

result_button = Button(Input_frame, text = "Kết quả", bg='#f2f2f2', activeforeground='white', command= export_result)
result_button.place(relx=.7, rely=0.9, relwidth=.2)
# ============END BUTTON===============

# screen.mainloop()