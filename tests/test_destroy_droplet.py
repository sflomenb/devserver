import pytest
import requests
import sys
import mock_response
import requests_mock
from mock_response import *
from scripts import destroy_droplet

@pytest.fixture(params=[['script.py', 'TOKEN'], \
        ['script.py', 'TOKEN', '--name', 'my-droplet'], \
        pytest.param(['script.py'], marks=pytest.mark.xfail), \
        pytest.param([], marks=pytest.mark.xfail)])
def mock_sys(monkeypatch, request):
    monkeypatch.setattr(sys, 'argv', request.param)

@pytest.mark.parametrize('mock_get_droplet,expected_text,should_skip_snapshots', [
    [MockDropletFound(),['Droplet ID:','Droplet destroyed'], False], \
    [MockDropletFound(),['Droplet ID:','Droplet destroyed'], True], \
    pytest.param(MockDropletNotFound(), None, False, marks=pytest.mark.xfail), \
    pytest.param(MockDropletNotFound(), None, True, marks=pytest.mark.xfail) \
])
def test_destroy_droplet(mock_get_droplet, expected_text, should_skip_snapshots, monkeypatch, mocker, capsys, do_client):
    mock_snapshot = MockSnapshotAndAction()
    def mock_get(*args, **kwargs):
        url = args[1]
        if url.endswith('/v2/droplets/'):
            return mock_get_droplet
        elif url.endswith('snapshots'):
            return MockGetSnapshots()
        elif 'action' in url:
            return mock_snapshot.set_url_and_method(url, 'get')
    def mock_post(*args, **kwargs):
        url = args[1]
        if 'action' in url:
            if 'json' in kwargs:
                action_type = kwargs['json'].get('type')
                if action_type == 'power_off':
                    return MockPowerOff()
                elif action_type == 'snapshot':
                    return mock_snapshot.set_url_and_method(url, 'post')
    def mock_delete(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr(requests.sessions.Session, "get", mock_get)
    monkeypatch.setattr(requests.sessions.Session, "post", mock_post)
    monkeypatch.setattr(requests.sessions.Session, "delete", mock_delete)
    mocker.patch('scripts.digital_ocean_client.DigitalOceanClient.droplet_on', side_effect=[True, True, False])
    destroy_droplet.destroy_droplet(do_client, should_skip_snapshots)
    captured = capsys.readouterr()
    for text in expected_text:
        assert text in captured.out

    name_to_assert = sys.argv[-1] if '--name' in sys.argv  else 'dev-server'
    assert f'Destroying droplet {name_to_assert}' in captured.out
    assert ('Creating snapshot...' in captured.out) ^ should_skip_snapshots

def test_main(mock_sys, mocker):
    mocker.patch('scripts.destroy_droplet.destroy_droplet')
    destroy_droplet.main()

