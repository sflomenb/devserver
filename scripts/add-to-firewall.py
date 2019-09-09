import getpass
import json
import requests
import sys

BASE = 'https://api.digitalocean.com'
HEADERS = {}

def get_firewall():

    list_req = requests.get(BASE + "/v2/firewalls", headers=HEADERS)
    list_req.raise_for_status()

    data = list_req.json()

    return data.get('firewalls')[0]

def add_ip_to_firewall(ip_addr, firewall):

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

    add_ip_req = requests.put(BASE + "/v2/firewalls/" + firewall_id,
                    headers=HEADERS,
                    json=firewall_data)
    print(add_ip_req.text)
    add_ip_req.raise_for_status()

def ip_in_cur_firewall(inbound_rules, ip_addr):
    ips = []
    for rule in inbound_rules:
        for k, v in rule.get('sources').items():
            for ip in v:
                if ip == ip_addr:
                    ips.append(ip)
    return ips

def main():
    global HEADERS
    if len(sys.argv) >= 3:
        IP_ADDR = sys.argv[1]
        TOKEN = sys.argv[2]
    else:
        print('Please enter an IP address and/or token')
        sys.exit(1)

    HEADERS = {'Authorization': 'Bearer ' + TOKEN}

    firewall = get_firewall()

    inbound_rules = firewall.get('inbound_rules')

    if not ip_in_cur_firewall(inbound_rules, IP_ADDR):
        add_ip_to_firewall(IP_ADDR, firewall)
    else:
        print('IP ' + IP_ADDR + ' is part of firewall, nothing to do')

if __name__ == '__main__':
    main()

