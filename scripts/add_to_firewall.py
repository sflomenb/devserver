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
    if len(sys.argv) >= 3:
        IP_ADDR = sys.argv[1]
        TOKEN = sys.argv[2]
    else:
        print('Please enter an IP address and/or token')
        sys.exit(1)

    client = digital_ocean_client.DigitalOceanClient(TOKEN)

    firewall = client.get_firewall()

    inbound_rules = firewall.get('inbound_rules')

    if not ip_in_cur_firewall(inbound_rules, IP_ADDR):
        client.add_ip_to_firewall(IP_ADDR, firewall)
    else:
        print('IP ' + IP_ADDR + ' is part of firewall, nothing to do')

if __name__ == '__main__':
    main()

