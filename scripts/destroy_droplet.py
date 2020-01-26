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
    print(f'Droplet ID:{droplet_id}')
    client.power_off(droplet_id)
    client.wait_for_droplet(droplet_id, False)
    snapshot_name = client.snapshot(droplet_id)
    client.clean_snapshots(snapshot_name)
    client.delete(droplet_id)
    print('Droplet destroyed')

def main():
    if len(sys.argv) >= 2:
        TOKEN = sys.argv[1]
    else:
        print('Please enter a token')
        sys.exit(1)

    client = digital_ocean_client.DigitalOceanClient(TOKEN)

    destroy_droplet(client)

if __name__ == '__main__':
    main()
