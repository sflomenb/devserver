import argparse
import sys
import digital_ocean_client

def ip_in_cur_firewall(inbound_rules, ip_addr):
    ips = []
    for rule in inbound_rules:
        for k, v in rule.get('sources').items():
            for ip in v:
                if ip == ip_addr:
                    ips.append(ip)
    return ips

def main():

    parser = argparse.ArgumentParser(description='Add current IP address to firewall')
    parser.add_argument('ip_address', help='IP address to add to the firewall')
    parser.add_argument('token', help='Digtal Ocean API token')
    args = parser.parse_args()

    IP_ADDR = args.ip_address
    TOKEN = args.token

    client = digital_ocean_client.DigitalOceanClient(TOKEN)

    firewall = client.get_firewall()

    inbound_rules = firewall.get('inbound_rules')

    if not ip_in_cur_firewall(inbound_rules, IP_ADDR):
        client.add_ip_to_firewall(IP_ADDR, firewall)
    else:
        print('IP ' + IP_ADDR + ' is part of firewall, nothing to do')

if __name__ == '__main__':
    main()

