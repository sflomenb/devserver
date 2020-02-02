import requests

class RestClient:
    def __init__(self, headers={}):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get_json(self, url, params=None):
        if params:
            response = self.session.get(url, params=params)
        else:
            response = self.session.get(url)
        response.raise_for_status()
        print(response.status_code)
        return response.json()

    def post_json(self, url, json=None):
        response = self.session.post(url, json=json)
        response.raise_for_status()
        print(response.status_code)
        return response.json()

    def post(self, url, json=None):
        response = self.session.post(url, json=json)
        response.raise_for_status()
        print(response.status_code)
        return response.status_code

    def put_json(self, url, json=None):
        response = self.session.put(url, json=json)
        response.raise_for_status()
        print(response.status_code)
        return response.json()

    def delete(self, url):
        response = self.session.delete(url)
        response.raise_for_status()
        print(response.status_code)
        return response.status_code
