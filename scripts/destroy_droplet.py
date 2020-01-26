import sys
import digital_ocean_client

def destroy_droplet(client):
    droplet_id = client.get_droplet(client.droplet_name)

    client.power_off(droplet_id)
    client.wait_for_droplet(droplet_id, False)
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
