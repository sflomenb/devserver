import argparse
import sys
import digital_ocean_client

def destroy_droplet(client):
    droplet_info = client.get_droplet(client.droplet_name)
    if droplet_info:
        droplet_id = droplet_info.get('id')
    else:
        sys.exit(1)
    if not droplet_id:
        sys.exit(1)
    print(f'Destroying droplet {client.droplet_name}')
    print(f'Droplet ID:{droplet_id}')
    client.power_off(droplet_id)
    client.wait_for_droplet(droplet_id, False)
    snapshot_name = client.snapshot(droplet_id)
    client.clean_snapshots(snapshot_name)
    client.delete(droplet_id)
    print('Droplet destroyed')

def main():
    parser = argparse.ArgumentParser(description='Destroy devserver droplet')
    parser.add_argument('token', help='Digtal Ocean API token')
    parser.add_argument('--name', help='droplet name')
    args = parser.parse_args()

    TOKEN = args.token
    name = args.name

    client = digital_ocean_client.DigitalOceanClient(TOKEN, name)

    destroy_droplet(client)

if __name__ == '__main__':
    main()
