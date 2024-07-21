import requests


class ForexAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def get_orders(self):
        endpoint = f"{self.base_url}/orders"
        r = self.session.get(endpoint)
        return r

    def post_orders(self, order_request):
        endpoint = f"{self.base_url}/orders"
        r = self.session.post(endpoint, json=order_request)
        return r

    def get_order_by_id(self, order_id):
        endpoint = f"{self.base_url}/orders/{order_id}"
        r = self.session.get(endpoint)
        return r

    def delete_order_by_id(self, order_id):
        endpoint = f"{self.base_url}/orders/{order_id}"
        r = self.session.delete(endpoint)
        return r
