import requests

from rc.exceptions import RcException

class APIClientException(RcException):
    def __init__(self, msg):
        super().__init__(f"config file error: {msg}")

class APIClient:
    def __init__(self, base_url, headers=None, auth=None):
        self.base_url = base_url
        self.headers = headers or {}
        self.auth = auth

    def _make_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(
                method, url, params=params, headers=self.headers, data=data, auth=self.auth
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None

    def request(self, method, endpoint, params=None, data=None):
        return self._make_request(method, endpoint, params=params, data=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass  # You can perform cleanup actions here if needed

# Using the APIClient as a context manager
base_url = "https://api.example.com"
custom_headers = {"User-Agent": "MyApp/1.0"}
auth_credentials = ("username", "password")

with APIClient(base_url, headers=custom_headers, auth=auth_credentials) as client:
    response = client.request("GET", "data")
    if response:
        data = response.json()
        print("Received data:", data)
