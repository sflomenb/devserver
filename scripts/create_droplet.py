import getpass
import json
import requests
import sys
import time

BASE = 'https://api.digitalocean.com'
HEADERS = {}
DROPLET_NAME = 'dev-server'

def get_firewall():

    list_req = requests.get(BASE + "/v2/firewalls", headers=HEADERS)
    list_req.raise_for_status()

    data = list_req.json()

    return data.get('firewalls')[0]

def get_ssh_key():

    list_keys_req = requests.get(BASE + '/v2/account/keys', headers=HEADERS)
    list_keys_req.raise_for_status()
    data = list_keys_req.json()
    ssh_key_id = [i.get('id') for i in data.get('ssh_keys') if i.get('name') == 'Dev server'][0]
    return ssh_key_id

def get_droplet(name):
    req = requests.get(BASE + '/v2/droplets/',
        headers=HEADERS)
    req.raise_for_status()
    data = req.json()
    for droplet in data.get('droplets'):
        if droplet.get('name') == name:
            return droplet
    print('Unable to get droplet with name ' + name)

def droplet_on(droplet_id):
    req = requests.get(BASE + '/v2/droplets/' + str(droplet_id),
        headers=HEADERS)
    req.raise_for_status()
    return req.json()['droplet']['status'] == 'active'

def wait_for_droplet(droplet_id):
    msg = 'Waiting for droplet'
    print(msg)
    while not droplet_on(droplet_id):
        print(msg)
        time.sleep(10)
    print('Droplet ' + str(droplet_id) + ' is available')

def add_droplet_to_firewall(firewall_id, droplet_id):
    payload = {'droplet_ids' : [droplet_id]}
    req = requests.post(BASE + '/v2/firewalls/' + firewall_id + '/droplets',
        headers=HEADERS,
        json=payload)
    req.raise_for_status()

def get_droplet_info():
    ssh_key_id = get_ssh_key()

    user_data = '''#!/bin/bash
apt install update && apt install upgrade
apt install -y mosh
sudo ufw allow 60000:60020/udp
'''

    payload = {'name'      : DROPLET_NAME,
               'region'    : 'nyc1',
               'size'      : 's-1vcpu-1gb',
               'image'     : 'docker-18-04',
               'ssh_keys'  : [ssh_key_id],
               'user_data' : user_data
    }

    return payload

def create_droplet():

    create_droplet_req = requests.post(BASE + "/v2/droplets",
        headers=HEADERS,
        json=get_droplet_info())
    create_droplet_req.raise_for_status()

    return create_droplet_req.json()['droplet']

def get_droplet_ip_address(droplet_data):
    ip_addr = droplet_data['networks']['v4'][0]['ip_address']
    print(ip_addr)

def main():
    global HEADERS
    if len(sys.argv) >= 2:
        TOKEN = sys.argv[1]
    else:
        print('Please enter a token')
        sys.exit(1)

    HEADERS = {'Authorization': 'Bearer ' + TOKEN}

    droplet_data = get_droplet(DROPLET_NAME)
    if not droplet_data:
        print('Creating droplet')
        droplet_data = create_droplet()
        droplet_id = droplet_data.get('id')
        wait_for_droplet(droplet_id)
        add_droplet_to_firewall(get_firewall().get('id'), droplet_id)
    else:
        print('Droplet ' + DROPLET_NAME + ' already exists')
    get_droplet_ip_address(droplet_data)

if __name__ == '__main__':
    main()
