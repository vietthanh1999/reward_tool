import uuid
import requests
import random
import json

API_URL = 'https://api.gologin.com'
OS_LIST = ['win', 'lin', 'mac']


class GologinProfile(object):
    def __init__(self, options):
        self.token = options.get('token', '')
        self.proxy_api_link = options.get('proxy_api_link', '')
        self.list_proxy = []
        # Số mail tối đa trên 1 IP US
        self.max_mail_used = options.get('max_mail_used', 5)

    def make_headers(self):
        return {
            'Authorization': 'Bearer '+self.token,
            'User-Agent': 'Selenium-API'
        }

    # proxies  {ip: str, port: str}[]
    def fetch_proxys(self):
        response = json.loads(requests.get(
            self.proxy_api_link).content.decode('utf-8'))
        proxies = response.get('data', [])
        for proxy in proxies:
            self.list_proxy.append({
                'ip': proxy['ip'],
                'port': proxy['port'],
                'used': 0
            })

    def create_fingerprint(self):
        headers = self.make_headers()
        os_type: str = random.choice(OS_LIST)
        return json.loads(requests.get(API_URL + '/browser/fingerprint?os=' + os_type, headers=headers).content.decode('utf-8'))

    def get_available_proxy(self):
        for p in self.list_proxy:
            if p['used'] < self.max_mail_used:
                p['used'] = p['used']+1
                return p
        return None

    def create_profile(self):
        try:
            headers = self.make_headers()
            fingerprint = self.create_fingerprint()
            proxy = self.get_available_proxy()
            if proxy == None:
                self.fetch_proxys()
                proxy = self.get_available_proxy()

            profile = {
                "name": str(uuid.uuid1()),
                "browserType": "chrome",
                "os": fingerprint.get('os'),
                "googleServicesEnabled": True,
                "lockEnabled": False,
                "debugMode": False,
                "navigator": {
                    "userAgent": fingerprint['navigator']['userAgent'],
                    "resolution": fingerprint['navigator']['resolution'],
                    "language": "en-GB,en-US",
                    "platform": fingerprint['navigator']['platform'],
                    "doNotTrack": False,
                    "hardwareConcurrency": fingerprint['navigator']['hardwareConcurrency'],
                    "deviceMemory": fingerprint['navigator']['deviceMemory'],
                    "maxTouchPoints": fingerprint['navigator']['maxTouchPoints'],
                },
                "proxyEnabled": True,
                # update proxy here
                "proxy":  {
                    "mode": "http",
                    "host": proxy['ip'],
                    "port": int(proxy['port']),
                    # "username": "",
                    # "password": ""
                },
                "storage": {
                    "local": True,
                    "extensions": True,
                    "bookmarks": True,
                    "history": True,
                    "passwords": True,
                    "session": True
                },
                "plugins": {
                    "enableVulnerable": True,
                    "enableFlash": True
                },
                "plugins": {
                    "enableVulnerable": True,
                    "enableFlash": True
                },
                "timezone": {
                    "enabled": True,
                    "fillBasedOnIp": True,
                    "timezone": "us"
                },
                "audioContext": {
                    "mode": "noise",
                    "noise": 0
                },
                "canvas": {
                    "mode": "noise",
                    "noise": 0
                },
                "fonts": {
                    "families": fingerprint['fonts'],
                    "enableMasking": True,
                    "enableDomRect": True
                },
                "mediaDevices": {
                    "videoInputs": 1,
                    "audioInputs": 1,
                    "audioOutputs": 1,
                    "enableMasking": True
                },
                "webRTC": {
                    "mode": "alerted",
                    "enabled": True,
                    "customize": True,
                    "localIpMasking": False,
                    "fillBasedOnIp": True,
                    "publicIp": "",
                    "localIps": []
                },
                "webGL": {
                    "mode": "noise",
                    "getClientRectsNoise": 0,
                    "noise": 0
                },
                "clientRects": {
                    "mode": "noise",
                    "noise": 0
                },
                "webGLMetadata": {
                    "mode": "mask",
                    "vendor": fingerprint['webGLMetadata']['vendor'],
                    "renderer": fingerprint['webGLMetadata']['renderer'],
                },
                "webglParams": fingerprint['webglParams'],
                "updateExtensions": True,
            }

            response = json.loads(requests.post(
                API_URL + '/browser/', headers=headers, json=profile).content.decode('utf-8'))

            if response.get('id') == None:
                print("Can't create profile")
                return False

            return response.get('id')
        except:
            print("Can't create profile")
            return False


# Test
# gp = GologinProfile({'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2U4ZTE1ZmVhMGEzZGU2Y2FiMTJiMDQiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2U4ZTFiMTkyYjg1OWFhNWNkNjhiODUifQ.qJGQvR_SnNJN6NUQPc9XdLBVlQrDg27f88u7akj1jVg',
#                      'proxy_api_link': 'https://tq.lunaproxy.com/getflowip?neek=1021070&num=10&type=2&sep=1&regions=us&ip_si=1&level=1&sb=',
#                      'max_mail_used': 2
#                      })
# profile_id_1 = gp.create_profile()
# profile_id_2 = gp.create_profile()
# print('profile_id_1: '+str(profile_id_1))
# print('profile_id_2: '+str(profile_id_2))
# print(gp.list_proxy)
