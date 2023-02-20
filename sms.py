import json
import requests
import time

class Sms(object):
  def __init__(self, options):
    self.token = options.get('token', '')

  def make_headers(self):
    return {
        'Authorization': 'Bearer '+self.token,
    }

  # Example response data.
  # {
  #   "id": 416623936,
  #   "phone": "+19492438627",
  #   "operator": "virtual32",
  #   "product": "microsoft",
  #   "price": 15.19,
  #   "status": "RECEIVED",
  #   "expires": "2023-02-14T17:01:17.571824917Z",
  #   "sms": null,
  #   "created_at": "2023-02-14T16:51:17.571824917Z",
  #   "country": "usa"
  # }
  def order_5sim(self):
    headers = self.make_headers()
    response = json.loads(requests.get('https://5sim.net/v1/user/buy/activation/usa/any/microsoft', headers=headers).content.decode('utf-8'))
    print(response)
    return response
    

  # return code/False
  def get_code_5sim(self, id):
    headers = self.make_headers()
    retry_time = 0
    while (retry_time < 100):
      response = json.loads(requests.get('https://5sim.net/v1/user/check/'+str(id), headers=headers).content.decode('utf-8'))
      print(response)
      smss = response.get('sms', [])
      if len(smss) != 0:
        for sms in smss:
          if sms.get('code'):
            return sms.get('code')

      retry_time = retry_time + 1
      time.sleep(8)
      print('retry get code from 5sim: '+ str(retry_time))
    return False

# sms = Sms({'token': 'fasf'})
# result = sms.get_code_5sim(1213131)
# print(result)


  # Example https://5sim.net/v1/user/check/<id> data
  #   {
  #     "id": 416623936,
  #     "phone": "+19492438627",
  #     "operator": "virtual32",
  #     "product": "microsoft",
  #     "price": 15.19,
  #     "status": "RECEIVED",
  #     "expires": "2023-02-14T17:01:17.571825Z",
  #     "sms": [
  #         {
  #             "created_at": "2023-02-14T16:53:57.800312Z",
  #             "date": "2023-02-14T16:53:57.79834Z",
  #             "sender": "*",
  #             "text": "021872",
  #             "code": "021872"
  #         }
  #     ],
  #     "created_at": "2023-02-14T16:51:17.571825Z",
  #     "country": "usa"
  # }