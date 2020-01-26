import sys
import digital_ocean_client


def main():
    if len(sys.argv) >= 2:
        TOKEN = sys.argv[1]
    else:
        print('Please enter a token')
        sys.exit(1)

    client = digital_ocean_client.DigitalOceanClient(TOKEN)

    droplet_data = client.get_droplet(client.droplet_name)
    if not droplet_data:
        print('Creating droplet')
        droplet_data = client.create_droplet()
        droplet_id = droplet_data.get('id')
        client.wait_for_droplet(droplet_id, True)
        client.add_droplet_to_firewall(client.get_firewall().get('id'), droplet_id)
    else:
        print('Droplet ' + client.droplet_name + ' already exists')
    client.get_droplet_ip_address(client.get_droplet(client.droplet_name))

if __name__ == '__main__':
    main()
