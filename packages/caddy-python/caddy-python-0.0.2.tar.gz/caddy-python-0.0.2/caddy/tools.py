from caddy.base import BaseAPI

class Tools(BaseAPI):
    def __init__(self, api_key=None):
        super().__init__(api_key)
        self.api_key = api_key
        self.route = "/tools"

    def request(self, method: str, path: str, body: object = None) -> object:
        path = f"{self.route}/{path}/run"
        response = self._request(
            method=method,
            path=path,
            body=body
        )
        return response

    def search_tools(self, query):
        path = f'{self.route}/search'
        body = dict()
        body['query'] = query
        response = self._request(
            method='POST',
            path=path,
            body=body
        )
        return response['items']