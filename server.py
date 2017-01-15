import hug
import yaml
import json
import requests

def get_config(name):
    with open(name) as f:
        return yaml.safe_load(f)

USER_CONFIG = get_config('config.yaml')
DNSPOD_CONFIG = get_config('dnspod.yaml')

HEADERS = {'User-Agent': 'HaoDDNS Client/1.0.0 (exiaohao@gmail.com)', }

def record_info(domain, sub_domain):
    data = {
        "login_email": USER_CONFIG['email'],
        "login_password": USER_CONFIG['password'],
        "format": 'json',
        "domain": domain,
        "sub_domain": sub_domain
    }
    r = requests.post(DNSPOD_CONFIG['list'], data=data, timeout=5)
    print(r.json())
    return r.json()['records'][0]


@hug.get('/update_addr')
def happy_birthday(domain: str, sub_domain: str, ip_addr: str):
    domain_info = record_info(domain, sub_domain)
    print('Domain Info:\n', domain_info)
    payload = {
        "login_email": USER_CONFIG['email'],
        "login_password": USER_CONFIG['password'],
        "format": 'json',
        "domain": domain,
        "record_id": domain_info['id'],
        "sub_domain": sub_domain,
        "record_line": '默认',
        "value": ip_addr
    }
    # print(payload)
    #p = ["{}={}".format(k ,v) for k, v in payload.items()]
    #print('&'.join(p))
    r = requests.post(DNSPOD_CONFIG['ddns'], data=payload, headers=HEADERS)
    return r.json()

