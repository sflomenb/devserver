import pytest
import requests
import sys
import mock_response
from scripts import add_to_firewall

class MockFirewallIpNotInFirewall(mock_response.MockResponse):
    @staticmethod
    def json():
        return {
            "firewalls": [
                {
                    "created_at": "2019-09-05T20:44:41Z",
                    "droplet_ids": [],
                    "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                    "inbound_rules": [
                        {
                            "ports": "22",
                            "protocol": "tcp",
                            "sources": {
                                "addresses": [
                                    "11.22.333.444"
                                ]
                            }
                        },
                        {
                            "ports": "80",
                            "protocol": "tcp",
                            "sources": {
                                "addresses": [
                                    "11.22.333.444"
                                ]
                            }
                        },
                        {
                            "ports": "443",
                            "protocol": "tcp",
                            "sources": {
                                "addresses": [
                                    "11.22.333.444"
                                ]
                            }
                        },
                        {
                            "ports": "3306",
                            "protocol": "tcp",
                            "sources": {
                                "addresses": [
                                    "11.22.333.444"
                                ]
                            }
                        }
                    ],
                    "name": "dev-server-firewall",
                    "outbound_rules": [
                        {
                            "destinations": {
                                "addresses": [
                                    "0.0.0.0/0",
                                    "::/0"
                                ]
                            },
                            "ports": "0",
                            "protocol": "icmp"
                        },
                        {
                            "destinations": {
                                "addresses": [
                                    "0.0.0.0/0",
                                    "::/0"
                                ]
                            },
                            "ports": "0",
                            "protocol": "tcp"
                        },
                        {
                            "destinations": {
                                "addresses": [
                                    "0.0.0.0/0",
                                    "::/0"
                                ]
                            },
                            "ports": "0",
                            "protocol": "udp"
                        }
                    ],
                    "pending_changes": [],
                    "status": "succeeded",
                    "tags": []
                }
            ],
            "links": {},
            "meta": {
                "total": 1
            }
        }

@pytest.fixture
def mock_response_ip_not_in_firewall(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockFirewallIpNotInFirewall()
    def mock_put(*args, **kwargs):
        return MockFirewallIpNotInFirewall()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)
    monkeypatch.setattr(requests.sessions.Session, "put", mock_get)

@pytest.fixture(params=[['script.py', '1.2.3.4', 'TOKEN'], \
        pytest.param(['script.py'], marks=pytest.mark.xfail), \
        pytest.param(['script.py', '1.2.3.4'], marks=pytest.mark.xfail)])
def mock_sys(monkeypatch, request):
    monkeypatch.setattr(sys, 'argv', request.param)

def test_nothing_happens_ip_in_firewall(mock_sys, capsys, mock_response_ip_in_firewall):
    add_to_firewall.main()
    captured = capsys.readouterr()
    assert 'IP 1.2.3.4 is part of firewall, nothing to do' in captured.out

def test_nothing_happens_ip_in_firewall(mock_sys, capsys, mock_response_ip_not_in_firewall):
    add_to_firewall.main()
    captured = capsys.readouterr()
    assert 'Adding IP 1.2.3.4 to firewall' in captured.out

@pytest.fixture(params=[
    '1.2.3.4',
    pytest.param('11.22.33.44', marks=pytest.mark.xfail)
])
def ip_address(request):
    return request.param

def test_ip_in_cur_firewall(ip_address):
    inbound_rules = [
        {
            "ports": "22",
            "protocol": "tcp",
            "sources": {
                "addresses": [
                    "1.2.3.4"
                ]
            }
        },
        {
            "ports": "80",
            "protocol": "tcp",
            "sources": {
                "addresses": [
                    "1.2.3.4"
                ]
            }
        },
        {
            "ports": "443",
            "protocol": "tcp",
            "sources": {
                "addresses": [
                    "1.2.3.4"
                ]
            }
        },
        {
            "ports": "3306",
            "protocol": "tcp",
            "sources": {
                "addresses": [
                    "1.2.3.4"
                ]
            }
        }
    ]
    assert add_to_firewall.ip_in_cur_firewall(inbound_rules, ip_address)

