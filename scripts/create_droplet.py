import argparse
import sys
from datetime import datetime
import digital_ocean_client

def main():
    start=datetime.now()
    parser = argparse.ArgumentParser(description='Create devserver droplet')
    parser.add_argument('token', help='Digtal Ocean API token')
    parser.add_argument('--name', help='droplet name')
    args = parser.parse_args()

    TOKEN = args.token
    name = args.name

    if name:
        client = digital_ocean_client.DigitalOceanClient(TOKEN, name)
    else:
        client = digital_ocean_client.DigitalOceanClient(TOKEN)

    droplet_data = client.get_droplet(client.droplet_name)
    if not droplet_data:
        # check if we have snapshot
        snapshots = client.get_droplet_snapshots()
        image = None
        has_droplet_snapshot = client.has_droplet_snapshot(snapshots)
        if has_droplet_snapshot:
            print('Creating from snapshot')
            image = int(has_droplet_snapshot[0].get('id'))
        else:
            print('Creating droplet')
            image = 'docker-18-04'
        print(image)
        droplet_data = client.create_droplet(image)
        droplet_id = droplet_data.get('id')
        client.wait_for_droplet(droplet_id, True)
        client.add_droplet_to_firewall(client.get_firewall().get('id'), droplet_id)
    else:
        print('Droplet ' + client.droplet_name + ' already exists')
    client.get_droplet_ip_address(client.get_droplet(client.droplet_name))
    print(datetime.now()-start)

if __name__ == '__main__':
    main()
