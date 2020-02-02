import pytest
import requests
import sys
import mock_response
from scripts import add_to_firewall
from conftest import MockSshKeys

class TestDigitalOceanClient:
    def test_mock_firewalls(self, do_client, mock_response_ip_in_firewall):
        firewall = do_client.get_firewall()
        assert firewall.get('id') == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        assert firewall.get('name') == "dev-server-firewall"

    def test_add_ip_to_firewall(self, do_client, mock_response_ip_in_firewall):
        firewall = do_client.get_firewall()
        new_ip = '1.2.3.4'
        do_client.add_ip_to_firewall(new_ip, firewall)
        for inbound_rule in firewall.get('inbound_rules'):
            assert inbound_rule.get('sources').get('addresses')[0] == new_ip

    def test_get_ssh_key(self, do_client, mock_ssh_response):
        ssh_key = do_client.get_ssh_key()
        assert ssh_key == 512189

    def test_droplet_on(self, do_client, mock_droplet_on):
        droplet_on = do_client.droplet_on(3164494)
        assert droplet_on

    def test_droplet_found(self, do_client, mock_droplet):
        droplet = do_client.get_droplet('dev-server')
        assert droplet is not None
        assert droplet.get('name') == 'dev-server'
        assert droplet.get('id') == 7164712

    def test_droplet_not_found(self, do_client, capsys, mock_droplet):
        droplet = do_client.get_droplet('dev-server-wow')
        assert droplet is None
        captured = capsys.readouterr()
        assert 'Unable to get droplet with name dev-server-wow' in captured.out

    def test_get_droplet_info(self, do_client, mock_ssh_response):
        image = 'my-docker-image'
        droplet_info = do_client.get_droplet_info(image)
        assert type(droplet_info) == dict
        assert droplet_info.get('name') == 'dev-server'
        assert droplet_info.get('region') == 'nyc1'
        assert droplet_info.get('size') == 's-1vcpu-1gb'
        assert droplet_info.get('image') == 'my-docker-image'
        assert droplet_info.get('ssh_keys') == [512189]
        assert droplet_info.get('user_data') == '''#!/bin/bash
        apt install update && apt install upgrade
        apt install -y mosh
        sudo ufw allow 60000:60020/udp'''

    def test_create_droplet(self, do_client, mock_create_droplet):
        droplet = do_client.create_droplet('my-docker-image')
        assert type(droplet) == dict
        assert droplet.get('id') == 3164494
        assert droplet.get('name') == 'dev-server'

    def test_get_droplet_ip_address(self, do_client, get_mock_droplet, capsys):
        droplet_data = get_mock_droplet
        do_client.get_droplet_ip_address(droplet_data)
        captured = capsys.readouterr()
        assert '104.131.186.241' in captured.out

    def test_shut_down(self, do_client, mock_shut_down):
        shut_down_data = do_client.shut_down(3067649)
        action = shut_down_data.get('action')
        assert action.get('resource_id') == 3067649
        assert action.get('type') == 'shutdown'

    def test_power_off(self, do_client, mock_power_off):
        power_off_data = do_client.power_off(3067649)
        action = power_off_data.get('action')
        assert action.get('resource_id') == 3164450
        assert action.get('type') == 'power_off'

    def test_delete_droplet(self, do_client, mock_delete_droplet):
        status_code = do_client.delete(1234)
        assert status_code == 204

    def test_add_droplet_to_firewall(self, do_client, mock_add_droplet_to_firewall):
        status_code = do_client.add_droplet_to_firewall(3164494, 1500)
        assert status_code == 204

    @pytest.mark.parametrize('side_effects,on_off,expected_text', [
        [[False, False, True], True, 'Droplet 3164494 is available'], \
        [[True, True, False], False, 'Droplet 3164494 is off'],
    ])
    def test_wait_for_droplet_on_or_off(self, do_client, mocker, capsys, side_effects, on_off, expected_text):
        mocker.patch('scripts.digital_ocean_client.DigitalOceanClient.droplet_on', side_effect=side_effects)
        do_client.wait_for_droplet(3164494, on_off)
        captured = capsys.readouterr()
        assert captured.out.count('Waiting for droplet') == 3
        assert expected_text in captured.out

    def test_snapshot(self, do_client, mock_snapshot, capsys):
        snapshot_name = do_client.snapshot(3164494)
        captured = capsys.readouterr()
        assert snapshot_name.startswith('dev-server_')
        assert 'Snapshotted 3164494 with name' in captured.out
        assert captured.out.count('Creating snapshot...') == 3

    def test_get_droplet_snapshot(self, do_client, mock_get_droplet_snapshots):
        snapshots = do_client.get_droplet_snapshots()
        assert snapshots[0].get('name') == 'nginx-fresh'
        assert snapshots[1].get('name') == 'dev-server_'
        assert all(x.get('type') == 'snapshot' for x in snapshots)

    def test_has_droplet_snapshot(self, do_client, mock_get_droplet_snapshots):
        snapshots = do_client.get_droplet_snapshots()
        has_snapshot = do_client.has_droplet_snapshot(snapshots)
        assert has_snapshot

    def test_has_droplet_snapshot_no_devserver(self, do_client, mock_get_droplet_snapshots_without_devserver):
        snapshots = do_client.get_droplet_snapshots()
        has_snapshot = do_client.has_droplet_snapshot(snapshots)
        assert not has_snapshot

    def test_delete_snapshot(self, do_client, mock_snapshot_data, mock_delete_snapshot, capsys):
        do_client.delete_snapshot(mock_snapshot_data)
        captured = capsys.readouterr()
        assert 'Deleting snapshot 7938206, nginx-fresh' in captured.out

    def test_clean_snapshots(self, do_client, capsys, mock_get_droplet_snapshots, mock_delete_snapshot):
        do_client.clean_snapshots('dev-server_')
        captured = capsys.readouterr()
        assert 'Deleting snapshot 7938580, dev-server_' not in captured.out
        assert 'Deleting snapshot 7938206, nginx-fresh' not in captured.out
        assert 'Deleting snapshot 7918580, dev-server_old' in captured.out
