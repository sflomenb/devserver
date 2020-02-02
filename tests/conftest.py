import pytest
from mock_response import *
import requests

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")

@pytest.fixture(autouse=True)
def fake_url(monkeypatch):
    monkeypatch.setattr('scripts.digital_ocean_client.DigitalOceanClient.BASE_URL', 'https://fake-url.com')
    monkeypatch.setattr('digital_ocean_client.DigitalOceanClient.BASE_URL', 'https://fake-url.com')

@pytest.fixture
def do_client():
    from scripts import digital_ocean_client
    return digital_ocean_client.DigitalOceanClient('TOKEN', sleep_time=0.1)

@pytest.fixture
def mock_response_ip_in_firewall(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockFirewallIpInFirewall()
    def mock_put(*args, **kwargs):
        return MockFirewallIpInFirewall()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)
    monkeypatch.setattr(requests.sessions.Session, "put", mock_put)

@pytest.fixture
def mock_ssh_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSshKeys()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)

@pytest.fixture
def mock_droplet(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockDropletFound()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)

@pytest.fixture
def mock_create_droplet(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockSshKeys()
    def mock_post(*args, **kwargs):
        return MockCreateDroplet()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)

@pytest.fixture
def get_mock_droplet():
    return {
        "id": 3164494,
        "name": "example.com",
        "memory": 1024,
        "vcpus": 1,
        "disk": 25,
        "locked": False,
        "status": "active",
        "kernel": {
          "id": 2233,
          "name": "Ubuntu 14.04 x64 vmlinuz-3.13.0-37-generic",
          "version": "3.13.0-37-generic"
        },
        "created_at": "2014-11-14T16:36:31Z",
        "features": [
          "ipv6",
          "virtio"
        ],
        "backup_ids": [

        ],
        "snapshot_ids": [
          7938206
        ],
        "image": {
          "id": 6918990,
          "name": "14.04 x64",
          "distribution": "Ubuntu",
          "slug": "ubuntu-16-04-x64",
          "public": True,
          "regions": [
            "nyc1",
            "ams1",
            "sfo1",
            "nyc2",
            "ams2",
            "sgp1",
            "lon1",
            "nyc3",
            "ams3",
            "nyc3"
          ],
          "created_at": "2014-10-17T20:24:33Z",
          "type": "snapshot",
          "min_disk_size": 20,
          "size_gigabytes": 2.34
        },
        "volume_ids": [

        ],
        "size": {
        },
        "size_slug": "s-1vcpu-1gb",
        "networks": {
          "v4": [
            {
              "ip_address": "104.131.186.241",
              "netmask": "255.255.240.0",
              "gateway": "104.131.176.1",
              "type": "public"
            }
          ],
          "v6": [
            {
              "ip_address": "2604:A880:0800:0010:0000:0000:031D:2001",
              "netmask": 64,
              "gateway": "2604:A880:0800:0010:0000:0000:0000:0001",
              "type": "public"
            }
          ]
        },
        "region": {
          "name": "New York 3",
          "slug": "nyc3",
          "sizes": [
            "s-1vcpu-1gb",
            "s-1vcpu-2gb",
            "s-1vcpu-3gb",
            "s-2vcpu-2gb",
            "s-3vcpu-1gb",
            "s-2vcpu-4gb",
            "s-4vcpu-8gb",
            "s-6vcpu-16gb",
            "s-8vcpu-32gb",
            "s-12vcpu-48gb",
            "s-16vcpu-64gb",
            "s-20vcpu-96gb",
            "s-24vcpu-128gb",
            "s-32vcpu-192gb"
          ],
          "features": [
            "virtio",
            "private_networking",
            "backups",
            "ipv6",
            "metadata"
          ],
          "available": True
        },
        "tags": [

        ]
      }


@pytest.fixture
def mock_droplet_on(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockDropletOn()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)

@pytest.fixture
def mock_droplet_off_then_on(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockDropletOffThenOn()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)


@pytest.fixture
def mock_snapshot(monkeypatch):
    mock_response = MockSnapshotAndAction()
    def mock_get(*args, **kwargs):
        return mock_response.set_url_and_method(args[1], 'get')
    def mock_post(*args, **kwargs):
        return mock_response.set_url_and_method(args[1], 'post')
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)

@pytest.fixture
def mock_get_snapshots(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockGetSnapshots().set_url_and_method(args[1], 'get')
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)

@pytest.fixture
def mock_get_droplet_snapshots(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockGetSnapshots().set_url_and_method(args[1], 'get')
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)

@pytest.fixture
def mock_get_droplet_snapshots_without_devserver(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockGetSnapshotsWithoutDevServer().set_url_and_method(args[1], 'get')
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)

@pytest.fixture
def mock_snapshot_data():
    return {
              "id": 7938206,
              "name": "nginx-fresh",
              "distribution": "Ubuntu",
              "slug": None,
              "public": False,
              "regions": [
                "nyc3",
                "nyc3"
              ],
              "created_at": "2014-11-14T16:37:34Z",
              "type": "snapshot",
              "min_disk_size": 20,
              "size_gigabytes": 2.34
            }

@pytest.fixture
def mock_delete_snapshot(monkeypatch):
    def mock_delete(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(requests.sessions.Session, "delete", mock_delete)

@pytest.fixture
def mock_shut_down(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockShutDown()
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)

@pytest.fixture
def mock_power_off(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockPowerOff()
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)

@pytest.fixture
def mock_add_droplet_to_firewall(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockAddDropletToFirewall()
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)

@pytest.fixture
def mock_delete_droplet(monkeypatch):
    def mock_delete(*args, **kwargs):
        return MockAddDropletToFirewall()
    monkeypatch.setattr(requests.sessions.Session, "delete", mock_delete)

