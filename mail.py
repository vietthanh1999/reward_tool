import requests
import re
import time

def get_code_from_mailnesia(email: str):
  retry_time = 0
  while(retry_time < 3):
    time.sleep(10)
    print(email.split('@')[0])
    result = requests.get('https://mailnesia.com/mailbox/'+email.split('@')[0]).content.decode('utf-8')
    
    list_mail_id = re.findall('id="[0-9]{10}"',result)
    last_mail_id = 0
    for mail_id in list_mail_id:
        current_mail_id = int(mail_id[4:14])
        if last_mail_id < current_mail_id:
            last_mail_id = current_mail_id

    last_mail = requests.get('https://mailnesia.com/mailbox/'+email.split('@')[0]+'/' + str(last_mail_id)).content.decode('utf-8')
    if (re.findall(r'>[0-9]{7}<', last_mail)):
      code = re.findall(r'>[0-9]{7}<', last_mail)[0]
      return code[1:8]
    else:
      retry_time = retry_time + 1
      print('retry get code from mailnesia: ' + str(retry_time))
  
  return False

# code = get_code_from_mailnesia('jamesharrison175@mailnesia.com')
# print(code)