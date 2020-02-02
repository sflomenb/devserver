class MockResponse:
    def __init__(self):
        #print('Creating new MockResponse')
        self.count = 0

    def set_url_and_method(self, url, method):
        self.url = url
        self.method = method
        return self

    @staticmethod
    def raise_for_status():
        pass

    def status_code():
        return 200

    def json(self):
        self.count += 1
        print(f'count has been changed to {self.count}')

class MockFirewallIpInFirewall(MockResponse):
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

class MockSshKeys(MockResponse):
    @staticmethod
    def json():
        return {
          "ssh_keys": [
            {
              "id": 512189,
              "fingerprint": "3b:16:bf:e4:8b:00:8b:b8:59:8c:a9:d3:f0:19:45:fa",
              "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQDDHr/jh2Jy4yALcK4JyWbVkPRaWmhck3IgCoeOO3z1e2dBowLh64QAM+Qb72pxekALga2oi4GvT+TlWNhzPH4V example",
              "name": "Dev server"
            },
            {
              "id": 612389,
              "fingerprint": "3b:16:bf:e4:8b:00:8b:b8:59:8c:a9:d3:f0:19:45:fa",
              "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQDDHr/jh2Jy4yALcK4JyWbVkPRaWmhck3IgCoeOO3z1e2dBowLh64QAM+Qb72pxekALga2oi4GvT+TlWNhzPH4V example",
              "name": "Other key"
            }
          ],
          "links": {
          },
          "meta": {
            "total": 1
          }
        }

class MockDropletFound(MockResponse):
    @staticmethod
    def json():
        return {
          "droplets": [
            {
              "id": 3164444,
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
              "created_at": "2014-11-14T16:29:21Z",
              "features": [
                "backups",
                "ipv6",
                "virtio"
              ],
              "backup_ids": [
                7938002
              ],
              "snapshot_ids": [

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
                    "ip_address": "104.236.32.182",
                    "netmask": "255.255.192.0",
                    "gateway": "104.236.0.1",
                    "type": "public"
                  }
                ],
                "v6": [
                  {
                    "ip_address": "2604:A880:0800:0010:0000:0000:02DD:4001",
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

                ],
                "features": [
                  "virtio",
                  "private_networking",
                  "backups",
                  "ipv6",
                  "metadata"
                ],
                "available": None
              },
              "tags": [

              ]
            },
            {
              "id": 7164712,
              "name": "dev-server",
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
              "created_at": "2014-11-14T16:29:21Z",
              "features": [
                "backups",
                "ipv6",
                "virtio"
              ],
              "backup_ids": [
                7938002
              ],
              "snapshot_ids": [

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
                    "ip_address": "104.236.32.182",
                    "netmask": "255.255.192.0",
                    "gateway": "104.236.0.1",
                    "type": "public"
                  }
                ],
                "v6": [
                  {
                    "ip_address": "2604:A880:0800:0010:0000:0000:02DD:4001",
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

                ],
                "features": [
                  "virtio",
                  "private_networking",
                  "backups",
                  "ipv6",
                  "metadata"
                ],
                "available": None
              },
              "tags": [

              ]
            }
          ],
          "links": {
            "pages": {
              "last": "https://api.digitalocean.com/v2/droplets?page=3&per_page=1",
              "next": "https://api.digitalocean.com/v2/droplets?page=2&per_page=1"
            }
          },
          "meta": {
            "total": 3
          }
        }

class MockDropletNotFound(MockResponse):
    def json(self):
        print(f'COUNT={self.count}')
        return {
          "droplets": [
            {
              "id": 3164444,
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
              "created_at": "2014-11-14T16:29:21Z",
              "features": [
                "backups",
                "ipv6",
                "virtio"
              ],
              "backup_ids": [
                7938002
              ],
              "snapshot_ids": [

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
                    "ip_address": "104.236.32.182",
                    "netmask": "255.255.192.0",
                    "gateway": "104.236.0.1",
                    "type": "public"
                  }
                ],
                "v6": [
                  {
                    "ip_address": "2604:A880:0800:0010:0000:0000:02DD:4001",
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

                ],
                "features": [
                  "virtio",
                  "private_networking",
                  "backups",
                  "ipv6",
                  "metadata"
                ],
                "available": None
              },
              "tags": [

              ]
            }
          ],
          "links": {
            "pages": {
              "last": "https://api.digitalocean.com/v2/droplets?page=3&per_page=1",
              "next": "https://api.digitalocean.com/v2/droplets?page=2&per_page=1"
            }
          },
          "meta": {
            "total": 2
          }
        }


class MockCreateDroplet(MockResponse):
    @staticmethod
    def json():
        return {
          "droplet": {
            "id": 3164494,
            "name": "dev-server",
            "memory": 1024,
            "vcpus": 1,
            "disk": 25,
            "locked": True,
            "status": "new",
            "kernel": {
              "id": 2233,
              "name": "Ubuntu 14.04 x64 vmlinuz-3.13.0-37-generic",
              "version": "3.13.0-37-generic"
            },
            "created_at": "2014-11-14T16:36:31Z",
            "features": [
              "virtio"
            ],
            "backup_ids": [

            ],
            "snapshot_ids": [

            ],
            "image": {
            },
            "volume_ids": [

            ],
            "size": {
            },
            "size_slug": "s-1vcpu-1gb",
            "networks": {
            },
            "region": {
            },
            "tags": [
              "web"
            ]
          },
          "links": {
            "actions": [
              {
                "id": 36805096,
                "rel": "create",
                "href": "https://api.digitalocean.com/v2/actions/36805096"
              }
            ]
          }
        }

class MockDropletOn(MockResponse):
    @staticmethod
    def json():
        return {
            "droplet": {
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
        }

class MockDropletOffThenOn(MockResponse):
    def __init__(self):
        self.counter = 0
    def json(self):
        if self.counter < 2:
            status = "off"
        else:
            status = "on"
        return {
            "droplet": {
                "id": 3164494,
                "name": "example.com",
                "memory": 1024,
                "vcpus": 1,
                "disk": 25,
                "locked": False,
                "status": status,
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
        }

class MockSnapshot(MockResponse):
    def json(self):
        super().json()

class MockSnapshotAndAction(MockResponse):
    def json(self):
        super().json()
        print(self.url)
        if self.method == 'post':
            return {
              "action": {
                "id": 36805022,
                "status": "in-progress",
                "type": "snapshot",
                "started_at": "2014-11-14T16:34:39Z",
                "completed_at": None,
                "resource_id": 3164450,
                "resource_type": "droplet",
                "region": {
                  "name": "New York 3",
                  "slug": "nyc3",
                  "sizes": [
                    "s-1vcpu-3gb",
                    "m-1vcpu-8gb",
                    "s-3vcpu-1gb",
                    "s-1vcpu-2gb",
                    "s-2vcpu-2gb",
                    "s-2vcpu-4gb",
                    "s-4vcpu-8gb",
                    "s-6vcpu-16gb",
                    "s-8vcpu-32gb",
                    "s-12vcpu-48gb",
                    "s-16vcpu-64gb",
                    "s-20vcpu-96gb",
                    "s-1vcpu-1gb",
                    "c-1vcpu-2gb",
                    "s-24vcpu-128gb"
                  ],
                  "features": [
                    "private_networking",
                    "backups",
                    "ipv6",
                    "metadata",
                    "server_id",
                    "install_agent",
                    "storage",
                    "image_transfer"
                  ],
                  "available": True
                },
                "region_slug": "nyc3"
              }
            }
        else:
            if self.count < 4:
                completed_at = None
            else:
                completed_at = "2014-11-14T16:34:39Z"
            return {
              "action": {
                "id": 36805022,
                "status": "in-progress",
                "type": "snapshot",
                "started_at": "2014-11-14T16:34:39Z",
                "completed_at": completed_at,
                "resource_id": 3164450,
                "resource_type": "droplet",
                "region": {
                  "name": "New York 3",
                  "slug": "nyc3",
                  "sizes": [
                    "s-1vcpu-3gb",
                    "m-1vcpu-8gb",
                    "s-3vcpu-1gb",
                    "s-1vcpu-2gb",
                    "s-2vcpu-2gb",
                    "s-2vcpu-4gb",
                    "s-4vcpu-8gb",
                    "s-6vcpu-16gb",
                    "s-8vcpu-32gb",
                    "s-12vcpu-48gb",
                    "s-16vcpu-64gb",
                    "s-20vcpu-96gb",
                    "s-1vcpu-1gb",
                    "c-1vcpu-2gb",
                    "s-24vcpu-128gb"
                  ],
                  "features": [
                    "private_networking",
                    "backups",
                    "ipv6",
                    "metadata",
                    "server_id",
                    "install_agent",
                    "storage",
                    "image_transfer"
                  ],
                  "available": True
                },
                "region_slug": "nyc3"
              }
            }

class MockGetSnapshots(MockResponse):
    def json(self):
        super().json()
        return {
          "snapshots": [
            {
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
            },
            {
              "id": 7938580,
              "name": "dev-server_",
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
            },
            {
              "id": 7918580,
              "name": "dev-server_old",
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
          ],
          "links": {
          },
          "meta": {
            "total": 2
          }
        }

class MockGetSnapshotsWithoutDevServer(MockResponse):
    def json(self):
        super().json()
        return {
          "snapshots": [
            {
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
            },
          ],
          "links": {
          },
          "meta": {
            "total": 2
          }
        }

class MockShutDown(MockResponse):
        def json(self):
            super().json()
            return {
              "action": {
                "id": 36077293,
                "status": "in-progress",
                "type": "shutdown",
                "started_at": "2014-11-04T17:08:03Z",
                "completed_at": None,
                "resource_id": 3067649,
                "resource_type": "droplet",
                "region": {
                  "name": "New York 2",
                  "slug": "nyc2",
                  "sizes": [
                    "s-1vcpu-3gb",
                    "m-1vcpu-8gb",
                    "s-3vcpu-1gb",
                    "s-1vcpu-2gb",
                    "s-2vcpu-2gb",
                    "s-2vcpu-4gb",
                    "s-4vcpu-8gb",
                    "s-6vcpu-16gb",
                    "s-8vcpu-32gb",
                    "s-12vcpu-48gb",
                    "s-16vcpu-64gb",
                    "s-20vcpu-96gb",
                    "s-1vcpu-1gb",
                    "c-1vcpu-2gb",
                    "s-24vcpu-128gb"
                  ],
                  "features": [
                    "private_networking",
                    "backups",
                    "ipv6",
                    "metadata",
                    "server_id",
                    "install_agent",
                    "storage",
                    "image_transfer"
                  ],
                  "available": True
                },
                "region_slug": "nyc2"
              }
            }

class MockPowerOff(MockResponse):
        def json(self):
            super().json()
            return {
              "action": {
                "id": 36804751,
                "status": "in-progress",
                "type": "power_off",
                "started_at": "2014-11-14T16:31:07Z",
                "completed_at": None,
                "resource_id": 3164450,
                "resource_type": "droplet",
                "region": {
                  "name": "New York 3",
                  "slug": "nyc3",
                  "sizes": [
                    "s-1vcpu-3gb",
                    "m-1vcpu-8gb",
                    "s-3vcpu-1gb",
                    "s-1vcpu-2gb",
                    "s-2vcpu-2gb",
                    "s-2vcpu-4gb",
                    "s-4vcpu-8gb",
                    "s-6vcpu-16gb",
                    "s-8vcpu-32gb",
                    "s-12vcpu-48gb",
                    "s-16vcpu-64gb",
                    "s-20vcpu-96gb",
                    "s-1vcpu-1gb",
                    "c-1vcpu-2gb",
                    "s-24vcpu-128gb"
                  ],
                  "features": [
                    "private_networking",
                    "backups",
                    "ipv6",
                    "metadata",
                    "server_id",
                    "install_agent",
                    "storage",
                    "image_transfer"
                  ],
                  "available": True
                },
                "region_slug": "nyc3"
              }
            }

class MockAddDropletToFirewall(MockResponse):
    status_code = 204

class MockDeleteDroplet(MockResponse):
    status_code = 204

