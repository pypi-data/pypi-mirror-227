import http.client
import json
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

class Requests:
    def __init__(self):
        self.timeout = None
        self.max_redirects = 5
        self.session = {}
        self.cookie_jar = {}
        self.history = []

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_max_redirects(self, max_redirects):
        self.max_redirects = max_redirects

    def get(self, url, headers=None, params=None):
        return self.request("GET", url, headers=headers, params=params)

    def post(self, url, headers=None, data=None, json_data=None, files=None):
        return self.request("POST", url, headers=headers, data=data, json_data=json_data, files=files)

    def put(self, url, headers=None, data=None, json_data=None):
        return self.request("PUT", url, headers=headers, data=data, json_data=json_data)

    def delete(self, url, headers=None):
        return self.request("DELETE", url, headers=headers)

    def request(self, method, url, headers=None, params=None, data=None, json_data=None, files=None):
        url_parsed = urlparse(url)
        host = url_parsed.hostname
        port = url_parsed.port or 80
        path = url_parsed.path or '/'
        query = url_parsed.query

        conn = http.client.HTTPConnection(host, port)

        headers = headers or {}
        headers["Host"] = f"{host}:{port}"

        if params:
            query += "?" + "&".join([f"{key}={value}" for key, value in params.items()])

        body = None
        if json_data:
            data = json.dumps(json_data)
            headers["Content-Type"] = "application/json"
            body = data.encode()

        if data:
            headers["Content-Length"] = str(len(data))
            body = data.encode()

        conn.request(method, path + query, body=body, headers=headers)
        response = conn.getresponse()

        response_text = response.read().decode()

        conn.close()

        response_obj = Response(response.status, response_text, response.headers)
        self.history.append(response_obj)

        if response.status == 302 and 'location' in response.headers and self.max_redirects > 0:
            self.max_redirects -= 1
            return self.request(method, response.headers['location'], headers=headers)

        return response_obj

    def session(self):
        return Session(self)

class Response:
    def __init__(self, status_code, text, headers):
        self.status_code = status_code
        self.text = text
        self.headers = headers
    
    def json(self):
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return None

    def xml(self):
        if "application/xml" in self.headers.get("Content-Type", ""):
            return ET.fromstring(self.text)
        return None

    def text(self):
        return self.text
    
    def headers(self):
        return self.headers

class Session:
    def __init__(self, emonic_requests):
        self.emonic_requests = emonic_requests

    def get(self, url, headers=None, params=None):
        return self.emonic_requests.get(url, headers=headers, params=params)

    def post(self, url, headers=None, data=None, json_data=None, files=None):
        return self.emonic_requests.post(url, headers=headers, data=data, json_data=json_data, files=files)

    def put(self, url, headers=None, data=None, json_data=None):
        return self.emonic_requests.put(url, headers=headers, data=data, json_data=json_data)

    def delete(self, url, headers=None):
        return self.emonic_requests.delete(url, headers=headers)