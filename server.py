from gevent import monkey
monkey.patch_all()

import hug
import yaml
import json
import socket
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
    #print(r.json())
    return r.json()['records'][0]


@hug.get('/')
def default():
    return {"status": 405, "message": "method not allowed!"}


@hug.get('/update_addr')
def update_addr(domain: str, sub_domain: str, ip_addr: str):
    full_domain = '{sub_domain}.{domain}'.format(sub_domain=sub_domain, domain=domain)
    if 'domains' in USER_CONFIG and full_domain not in USER_CONFIG['domains']:
        return {
            "message": "Domain not allowed",
            "status": "-2",
        }

    current_host = socket.gethostbyname(full_domain)
    if current_host == ip_addr:
        return {
            "message": "IP not changed",
            "code": -3,
        }

    try:
        domain_info = record_info(domain, sub_domain)
    except KeyError:
        return {
            "message": "Domain not registered!",
            "code": "-1",
        }

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
    result = r.json()
    return {
        "code": "200" if result['status']['code'] == "1" else result['status']['code'],
        "message": result['status']['message'],
    }

