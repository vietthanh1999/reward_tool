import requests
import re

def get_code_from_mailnesia(email: str):
  result = requests.get('https://mailnesia.com/mailbox/'+email).content.decode('utf-8')

  list_mail_id = re.findall('id="[0-9]{10}"',result)
  last_mail_id = 0
  for mail_id in list_mail_id:
      current_mail_id = int(mail_id[4:14])
      if last_mail_id < current_mail_id:
          last_mail_id = current_mail_id

  last_mail = requests.get('https://mailnesia.com/mailbox/'+email+'/' + str(last_mail_id)).content.decode('utf-8')
  code = re.findall(r'>[0-9]{7}<', last_mail)[0]
  return code[1:8]

# code = get_code_from_mailnesia('amandaangeline')
# print(code)