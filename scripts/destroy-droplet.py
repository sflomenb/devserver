import getpass
import json
import requests
import sys
import time

BASE = 'https://api.digitalocean.com'
HEADERS = {}
DROPLET_NAME = 'dev-server'

def get_droplet(name):
    req = requests.get(BASE + '/v2/droplets/',
        headers=HEADERS)
    req.raise_for_status()
    data = req.json()
    for droplet in data.get('droplets'):
        if droplet.get('name') == name:
            return str(droplet.get('id'))
    print('Unable to get droplet with name ' + name)
    sys.exit(1)

def shut_down(droplet_id):
    req = requests.post(BASE + '/v2/droplets/' + droplet_id + '/actions',
        headers=HEADERS,
        json={'type': 'shutdown'})
    req.raise_for_status()

def power_off(droplet_id):
    req = requests.post(BASE + '/v2/droplets/' + droplet_id + '/actions',
        headers=HEADERS,
        json={'type': 'power_off'})
    print(req.url)
    req.raise_for_status()

def droplet_on(droplet_id):
    req = requests.get(BASE + '/v2/droplets/' + droplet_id,
        headers=HEADERS)
    req.raise_for_status()
    data = req.json()
    print()
    print(json.dumps(data, indent=2))
    return data['droplet']['status'] == 'active'

def wait_for_droplet(droplet_id):
    msg = 'Waiting for droplet'
    print(msg)
    while droplet_on(droplet_id):
        print(msg)
        time.sleep(10)
    print('Droplet ' + droplet_id + ' is off')

def delete(droplet_id):
    req = requests.delete(BASE + '/v2/droplets/' + droplet_id,
        headers=HEADERS)
    req.raise_for_status()
    print(req.status_code)

def destroy_droplet():

    droplet_id = get_droplet(DROPLET_NAME)

    power_off(droplet_id)
    wait_for_droplet(droplet_id)
    delete(droplet_id)

def main():
    global HEADERS
    if len(sys.argv) >= 2:
        TOKEN = sys.argv[1]
    else:
        print('Please enter a token')
        sys.exit(1)

    HEADERS = {'Authorization': 'Bearer ' + TOKEN}

    destroy_droplet()

if __name__ == '__main__':
    main()
