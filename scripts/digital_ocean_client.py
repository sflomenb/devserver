import datetime
import json
import time
import rest_client

class DigitalOceanClient():
    BASE_URL = 'https://api.digitalocean.com'
    def __init__(self, token, droplet_name='dev-server', sleep_time=10):
        self.rest_client = rest_client.RestClient(headers={'Authorization': 'Bearer ' + token, \
                'Accept': 'application/json'})
        self.droplet_name = droplet_name
        self.sleep_time = sleep_time

    def get_firewall(self):
        data = self.rest_client.get_json(f'{self.BASE_URL}/v2/firewalls')

        # there is only one firewall in the account
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

        add_ip_req = self.rest_client.put_json(self.BASE_URL + "/v2/firewalls/" + firewall_id,
                        json=firewall_data)
        return firewall_data

    def get_ssh_key(self):
        data = self.rest_client.get_json(self.BASE_URL + '/v2/account/keys')
        ssh_key_id = [i.get('id') for i in data.get('ssh_keys') if i.get('name') == 'Dev server'][0]
        return ssh_key_id

    def get_droplet(self, name):
        data = self.rest_client.get_json(self.BASE_URL + '/v2/droplets/')
        for droplet in data.get('droplets'):
            if droplet.get('name') == name:
                return droplet
        print('Unable to get droplet with name ' + name)

    def droplet_on(self, droplet_id):
        data = self.rest_client.get_json(self.BASE_URL + '/v2/droplets/' + str(droplet_id))
        return data['droplet']['status'] == 'active'

    def add_droplet_to_firewall(self, firewall_id, droplet_id):
        payload = {'droplet_ids' : [droplet_id]}
        return self.rest_client.post(self.BASE_URL + '/v2/firewalls/' + str(firewall_id) + '/droplets',
            json=payload)

    def get_droplet_info(self, image):
        ssh_key_id = self.get_ssh_key()

        user_data = '''#!/bin/bash
        apt install update && apt install upgrade
        apt install -y mosh
        sudo ufw allow 60000:60020/udp'''

        payload = {'name'      : self.droplet_name,
                   'region'    : 'nyc1',
                   'size'      : 's-1vcpu-1gb',
                   'image'     : image,
                   'ssh_keys'  : [ssh_key_id],
                   'user_data' : user_data
        }

        return payload

    def create_droplet(self, image):
        data = self.rest_client.post_json(self.BASE_URL + "/v2/droplets",
            json=self.get_droplet_info(image))

        return data['droplet']

    def get_droplet_ip_address(self, droplet_data):
        ip_addr = droplet_data['networks']['v4'][0]['ip_address']
        print(ip_addr)

    def shut_down(self, droplet_id):
        return self.rest_client.post_json(self.BASE_URL + '/v2/droplets/' + str(droplet_id) + '/actions',
            json={'type': 'shutdown'})

    def power_off(self, droplet_id):
        return self.rest_client.post_json(f'{self.BASE_URL}/v2/droplets/{droplet_id}/actions',
            json={'type': 'power_off'})

    def wait_for_droplet(self, droplet_id, on_or_off):
        msg = 'Waiting for droplet'
        print(msg)
        while self.droplet_on(droplet_id) ^ on_or_off:
            print(msg)
            time.sleep(self.sleep_time)
        if on_or_off:
            print('Droplet ' + str(droplet_id) + ' is available')
        else:
            print('Droplet ' + str(droplet_id) + ' is off')

    def delete(self, droplet_id):
        return self.rest_client.delete(f'{self.BASE_URL}/v2/droplets/{droplet_id}')

    def snapshot(self, droplet_id):
        print("Taking snapshot...")
        snapshot_name = self.droplet_name + '_' + str(datetime.datetime.now()).replace(' ', '_')
        request_data = self.rest_client.post_json(f'{self.BASE_URL}/v2/droplets/{droplet_id}/actions',
                json={'type': 'snapshot', \
                        'name': snapshot_name})
        action_data = request_data.get('action')
        action_id = action_data.get('id')
        completed_at = action_data.get('completed_at')
        msg = 'Creating snapshot...'
        while not completed_at:
            print(msg)
            time.sleep(self.sleep_time)
            request_data = self.rest_client.get_json(f'{self.BASE_URL}/v2/droplets/{droplet_id}/actions/{action_id}')
            action_data = request_data.get('action')
            completed_at = action_data.get('completed_at')
        print(f'Snapshotted {droplet_id} with name {snapshot_name} at {completed_at}')
        return snapshot_name

    def get_droplet_snapshots(self):
        print("Looking for snapshot")
        data = self.rest_client.get_json(f'{self.BASE_URL}/v2/snapshots',
                params={'resource_type': 'droplet'})
        return data.get('snapshots')

    def has_droplet_snapshot(self, snapshots):
        return [i for i in snapshots if self.droplet_name in i.get('name')]

    def delete_snapshot(self, snapshot):
        snapshot_id = snapshot.get('id')
        print(f'Deleting snapshot {snapshot_id}, {snapshot.get("name")}')
        self.rest_client.delete(f'{self.BASE_URL}/v2/snapshots/{snapshot_id}')

    # delete devserver snapshots except the one just created
    def clean_snapshots(self, snapshot_name):
        snapshots = self.get_droplet_snapshots()
        for snapshot in snapshots:
            name = snapshot.get('name')
            if 'dev-server' in name and name != snapshot_name:
                self.delete_snapshot(snapshot)
