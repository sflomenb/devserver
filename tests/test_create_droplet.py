import pytest
import requests
import sys
import mock_response
import requests_mock
from mock_response import *
from scripts import create_droplet


class MockGetFirewall(MockResponse):
    def json(self):
        return {
          "firewalls": [
            {
              "id": "fb6045f1-cf1d-4ca3-bfac-18832663025b",
              "name": "firewall",
              "status": "succeeded",
              "inbound_rules": [
                {
                  "protocol": "tcp",
                  "ports": "80",
                  "sources": {
                    "load_balancer_uids": [
                      "4de7ac8b-495b-4884-9a69-1050c6793cd6"
                    ]
                  }
                },
                {
                  "protocol": "tcp",
                  "ports": "22",
                  "sources": {
                    "tags": [
                      "gateway"
                    ],
                    "addresses": [
                      "18.0.0.0/8"
                    ]
                  }
                }
              ],
              "outbound_rules": [
                {
                  "protocol": "tcp",
                  "ports": "80",
                  "destinations": {
                    "addresses": [
                      "0.0.0.0/0",
                      "::/0"
                    ]
                  }
                }
              ],
              "created_at": "2017-05-23T21:23:59Z",
              "droplet_ids": [
                8043964
              ],
              "tags": [

              ],
              "pending_changes": [

              ]
            }
          ],
          "links": {
          },
          "meta": {
            "total": 1
          }
        }

@pytest.fixture(params=[['script.py', 'TOKEN'], \
        pytest.param(['script.py'], marks=pytest.mark.xfail), \
        pytest.param([], marks=pytest.mark.xfail)])
def mock_sys(monkeypatch, request):
    monkeypatch.setattr(sys, 'argv', request.param)

def test_create_droplet_found(mock_sys, mock_droplet, capsys):
    create_droplet.main()
    captured = capsys.readouterr()
    assert 'Droplet dev-server already exists' in captured.out

@pytest.mark.parametrize('mock_get_snapshots,expected_text', [[MockGetSnapshots(), 'Creating from snapshot'], [MockGetSnapshotsWithoutDevServer(), 'Creating droplet']])
def test_create_droplet_not_found(mock_sys, monkeypatch, capsys, mocker, mock_get_snapshots, expected_text, **kwargs):
    def mock_get(*args, **kwargs):
        url = args[1]
        if url.endswith('/v2/snapshots'):
            return mock_get_snapshots.set_url_and_method(args[1], 'get')
        elif url.endswith('/v2/account/keys'):
            return MockSshKeys()
        elif url.endswith('/v2/firewalls'):
            return MockGetFirewall()
    def mock_post(*args, **kwargs):
        url = args[1]
        if url.endswith('/v2/droplets'):
            return MockCreateDroplet()
        elif '/v2/firewalls/' in url and url.endswith('/droplets'):
            return MockAddDropletToFirewall()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)
    mocker.patch('create_droplet.digital_ocean_client.DigitalOceanClient.droplet_on', side_effect=[True, True, False])
    mocker.patch('create_droplet.digital_ocean_client.DigitalOceanClient.get_droplet', side_effect=[None, MockDropletFound().json().get('droplets')[1]])
    create_droplet.main()
    captured = capsys.readouterr()
    assert expected_text in captured.out
    assert '104.236.32.182' in captured.out

