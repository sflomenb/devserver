import datetime
import json
import requests
import time

class DigitalOceanClient():
    BASE_URL = 'https://api.digitalocean.com'
    def __init__(self, token, droplet_name='dev-server'):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer ' + token, \
                'Accept': 'application/json'})
        self.droplet_name = droplet_name

    def get_firewall(self):
        list_req = self.session.get(f'{self.BASE_URL}/v2/firewalls')
        list_req.raise_for_status()

        data = list_req.json()

        return data.get('firewalls')[0]

    def add_ip_to_firewall(self, ip_addr, firewall):
        print('Adding IP ' + ip_addr + ' to firewall')

        firewall_id = firewall.get('id')
        inbound_rules = firewall.get('inbound_rules')

        # add IP to rules
        for rule in inbound_rules:
            rule.get('sources')['addresses'] = [ip_addr]

        outbound_rules = firewall.get('outbound_rules')

        # change "0" port to "all"
        for rule in outbound_rules:
            if rule.get('ports') == '0':
                if rule.get('protocol') != 'icmp':
                    rule['ports'] = 'all'
                    print(rule)
                else:
                    del rule['ports']

        droplet_ids = firewall.get('droplet_ids')
        firewall_name = firewall.get('name')
        firewall_tags = firewall.get('tags')

        firewall_data = { 'name'          : firewall_name,
                          'inbound_rules' : inbound_rules,
                          'outbound_rules': outbound_rules,
                          'droplet_ids'   : droplet_ids,
                          'tags'          : firewall_tags
        }

        print(json.dumps(firewall_data, indent=2))

        add_ip_req = self.session.put(self.BASE_URL + "/v2/firewalls/" + firewall_id,
                        json=firewall_data)
        print(add_ip_req.text)
        add_ip_req.raise_for_status()

    def get_ssh_key(self):
        list_keys_req = self.session.get(self.BASE_URL + '/v2/account/keys')
        list_keys_req.raise_for_status()
        data = list_keys_req.json()
        ssh_key_id = [i.get('id') for i in data.get('ssh_keys') if i.get('name') == 'Dev server'][0]
        return ssh_key_id

    def get_droplet(self, name):
        req = self.session.get(self.BASE_URL + '/v2/droplets/')
        req.raise_for_status()
        data = req.json()
        for droplet in data.get('droplets'):
            if droplet.get('name') == name:
                return droplet
        print('Unable to get droplet with name ' + name)

    def droplet_on(self, droplet_id):
        req = self.session.get(self.BASE_URL + '/v2/droplets/' + str(droplet_id))
        req.raise_for_status()
        return req.json()['droplet']['status'] == 'active'

    def add_droplet_to_firewall(self, firewall_id, droplet_id):
        payload = {'droplet_ids' : [droplet_id]}
        req = self.session.post(self.BASE_URL + '/v2/firewalls/' + firewall_id + '/droplets',
            json=payload)
        req.raise_for_status()

    def get_droplet_info(self, image):
        ssh_key_id = self.get_ssh_key()

        user_data = '''#!/bin/bash
    apt install update && apt install upgrade
    apt install -y mosh
    sudo ufw allow 60000:60020/udp
    '''

        payload = {'name'      : self.droplet_name,
                   'region'    : 'nyc1',
                   'size'      : 's-1vcpu-1gb',
                   'image'     : image,
                   'ssh_keys'  : [ssh_key_id],
                   'user_data' : user_data
        }

        return payload

    def create_droplet(self, image):
        create_droplet_req = self.session.post(self.BASE_URL + "/v2/droplets",
            json=self.get_droplet_info(image))
        create_droplet_req.raise_for_status()

        return create_droplet_req.json()['droplet']

    def get_droplet_ip_address(self, droplet_data):
        ip_addr = droplet_data['networks']['v4'][0]['ip_address']
        print(ip_addr)

    def shut_down(self, droplet_id):
        req = self.session.post(self.BASE_URL + '/v2/droplets/' + droplet_id + '/actions',
            json={'type': 'shutdown'})
        req.raise_for_status()

    def power_off(self, droplet_id):
        req = self.session.post(f'{self.BASE_URL}/v2/droplets/{droplet_id}/actions',
            json={'type': 'power_off'})
        print(req.url)
        req.raise_for_status()

    def wait_for_droplet(self, droplet_id, on_or_off):
        msg = 'Waiting for droplet'
        print(msg)
        while self.droplet_on(droplet_id) ^ on_or_off:
            print(msg)
            time.sleep(10)
        if on_or_off:
            print('Droplet ' + str(droplet_id) + ' is available')
        else:
            print('Droplet ' + str(droplet_id) + ' is off')

    def delete(self, droplet_id):
        req = self.session.delete(f'{self.BASE_URL}/v2/droplets/{droplet_id}')
        req.raise_for_status()
        print(req.status_code)

    def snapshot(self, droplet_id):
        print("Taking snapshot...")
        snapshot_name = self.droplet_name + '_' + str(datetime.datetime.now()).replace(' ', '_')
        req = self.session.post(f'{self.BASE_URL}/v2/droplets/{droplet_id}/actions',
                json={'type': 'snapshot', \
                        'name': snapshot_name})
        req.raise_for_status()
        print(req.status_code)
        data = req.json().get('action')
        action_id = data.get('id')
        completed_at = data.get('completed_at')
        msg = 'Creating snapshot...'
        while not completed_at:
            print(msg)
            time.sleep(10)
            action_request = self.session.get(f'{self.BASE_URL}/v2/droplets/{droplet_id}/actions/{action_id}')
            action_request.raise_for_status()
            print(action_request.status_code)
            data = action_request.json().get('action')
            completed_at = data.get('completed_at')
        print(f'Snapshotted {droplet_id} with name {snapshot_name} at {completed_at}')
        return snapshot_name

    def get_droplet_snapshots(self):
        print("Looking for snapshot")
        req = self.session.get(f'{self.BASE_URL}/v2/snapshots',
                params={'resource_type': 'droplet'})
        req.raise_for_status()
        print(req.status_code)
        return req.json().get('snapshots')

    def has_droplet_snapshot(self, snapshots):
        return [i for i in snapshots if self.droplet_name in i.get('name')]

    def delete_snapshot(self, snapshot):
        snapshot_id = snapshot.get('id')
        print(f'Deleting snapshot {snapshot_id}, {snapshot.get("name")}')
        req = self.session.delete(f'{self.BASE_URL}/v2/snapshots/{snapshot_id}')
        req.raise_for_status()
        print(req.status_code)

    # delete devserver snapshots except the one just created
    def clean_snapshots(self, snapshot_name):
        snapshots = self.get_droplet_snapshots()
        for snapshot in snapshots:
            name = snapshot.get('name')
            if 'dev-server' in name and name != snapshot_name:
                self.delete_snapshot(snapshot)
