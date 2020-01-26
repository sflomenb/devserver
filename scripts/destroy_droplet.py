import getpass
import json
import requests
import sys
import time

BASE = 'https://api.digitalocean.com'
DROPLET_NAME = 'dev-server'

def get_droplet(session, name):
    req = session.get(BASE + '/v2/droplets/')
    req.raise_for_status()
    data = req.json()
    for droplet in data.get('droplets'):
        if droplet.get('name') == name:
            return str(droplet.get('id'))
    print('Unable to get droplet with name ' + name)
    sys.exit(1)

def shut_down(session, droplet_id):
    req = session.post(BASE + '/v2/droplets/' + droplet_id + '/actions',
        json={'type': 'shutdown'})
    req.raise_for_status()

def power_off(session, droplet_id):
    req = session.post(BASE + '/v2/droplets/' + droplet_id + '/actions',
        json={'type': 'power_off'})
    print(req.url)
    req.raise_for_status()

def droplet_on(session, droplet_id):
    req = session.get(BASE + '/v2/droplets/' + droplet_id)
    req.raise_for_status()
    data = req.json()
    return data['droplet']['status'] == 'active'

def wait_for_droplet(session, droplet_id):
    msg = 'Waiting for droplet'
    print(msg)
    while droplet_on(droplet_id):
        print(msg)
        time.sleep(10)
    print('Droplet ' + droplet_id + ' is off')

def delete(session, droplet_id):
    req = session.delete(BASE + '/v2/droplets/' + droplet_id)
    req.raise_for_status()
    print(req.status_code)

def destroy_droplet(session):
    droplet_id = get_droplet(DROPLET_NAME)

    power_off(droplet_id)
    wait_for_droplet(droplet_id)
    delete(droplet_id)

def main():
    if len(sys.argv) >= 2:
        TOKEN = sys.argv[1]
    else:
        print('Please enter a token')
        sys.exit(1)

    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/json'})

    destroy_droplet(session)

if __name__ == '__main__':
    main()
