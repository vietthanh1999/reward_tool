import requests
import re
import time

retry_time_wait = [0, 10, 20, 30]


def get_code_from_mailnesia(email: str, last_time: int):
    retry_time = 0
    while (retry_time < 4):
        time.sleep(retry_time_wait[retry_time])
        result = requests.get(
            'https://mailnesia.com/mailbox/'+email.split('@')[0]).content.decode('utf-8')

        list_mail_id = re.findall('id="[0-9]{10}"', result)
        # id của mail đang dùng timestame
        new_mail_ids = []
        for mail_id in list_mail_id:
            # check new mail
            current_mail_id = int(mail_id[4:14])
            if current_mail_id > last_time:
                new_mail_ids.append(current_mail_id)

        # Không có mail mới
        if new_mail_ids.count == 0:
            print('retry get code for' + email + ': ' + str(retry_time))
            retry_time = retry_time + 1
            continue

        # Loại bỏ id trùng
        new_mail_ids = list(dict.fromkeys(new_mail_ids))
        new_mail_ids.sort(reverse=True)
        for mail_id in new_mail_ids:
            mail = requests.get('https://mailnesia.com/mailbox/'+email.split('@')[
                0]+'/' + str(mail_id)).content.decode('utf-8')
            result = re.findall(r'>[0-9]{7}<', mail)
            if (result):
                code = result[0]
                return code[1:8]

        print('retry get code for' + email + ': ' + str(retry_time))
        retry_time = retry_time + 1

    return False


# code = get_code_from_mailnesia('amandaangelin1@mailnesia.com', 1)
# print(code)
