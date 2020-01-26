import getpass
import json
import requests
import sys
import time

BASE = 'https://api.digitalocean.com'
DROPLET_NAME = 'dev-server'

def get_firewall(session):

    list_req = session.get(BASE + "/v2/firewalls")
    list_req.raise_for_status()

    data = list_req.json()

    return data.get('firewalls')[0]

def get_ssh_key(session):

    list_keys_req = session.get(BASE + '/v2/account/keys')
    list_keys_req.raise_for_status()
    data = list_keys_req.json()
    ssh_key_id = [i.get('id') for i in data.get('ssh_keys') if i.get('name') == 'Dev server'][0]
    return ssh_key_id

def get_droplet(session, name):
    req = session.get(BASE + '/v2/droplets/')
    req.raise_for_status()
    data = req.json()
    for droplet in data.get('droplets'):
        if droplet.get('name') == name:
            return droplet
    print('Unable to get droplet with name ' + name)

def droplet_on(session, droplet_id):
    req = session.get(BASE + '/v2/droplets/' + str(droplet_id))
    req.raise_for_status()
    return req.json()['droplet']['status'] == 'active'

def wait_for_droplet(session, droplet_id):
    msg = 'Waiting for droplet'
    print(msg)
    while not droplet_on(droplet_id):
        print(msg)
        time.sleep(10)
    print('Droplet ' + str(droplet_id) + ' is available')

def add_droplet_to_firewall(session, firewall_id, droplet_id):
    payload = {'droplet_ids' : [droplet_id]}
    req = session.post(BASE + '/v2/firewalls/' + firewall_id + '/droplets',
        json=payload)
    req.raise_for_status()

def get_droplet_info(session):
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

def create_droplet(session):

    create_droplet_req = session.post(BASE + "/v2/droplets",
        json=get_droplet_info())
    create_droplet_req.raise_for_status()

    return create_droplet_req.json()['droplet']

def get_droplet_ip_address(session, droplet_data):
    ip_addr = droplet_data['networks']['v4'][0]['ip_address']
    print(ip_addr)

def main():
    if len(sys.argv) >= 2:
        TOKEN = sys.argv[1]
    else:
        print('Please enter a token')
        sys.exit(1)

    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json'})

    droplet_data = get_droplet(session, DROPLET_NAME)
    if not droplet_data:
        print('Creating droplet')
        droplet_data = create_droplet(session)
        droplet_id = droplet_data.get('id')
        wait_for_droplet(session, droplet_id)
        add_droplet_to_firewall(session, get_firewall().get('id'), droplet_id)
    else:
        print('Droplet ' + DROPLET_NAME + ' already exists')
    get_droplet_ip_address(session, droplet_data)

if __name__ == '__main__':
    main()
