import requests

session = requests.Session()

def get_request(url, params=None):
    response = session.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code}, Details: {response.json()}')
    return response.json()
