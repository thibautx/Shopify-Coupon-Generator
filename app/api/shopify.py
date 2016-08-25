import json
import requests
from bs4 import BeautifulSoup

USERNAME = 'thibaut.xiong@gmail.com'
PASSWORD = 'bizzy123'

LOGIN_URL = 'https://bizzy-dev.myshopify.com/admin/auth/login'
DISCOUNT_URL = 'https://bizzy-dev.myshopify.com/admin/discounts.json'


class Shopify(object):

    def __init__(self):
        self.session = requests.session()
        self._login()
        self._set_headers()

    def _login(self):
        """
        Login to Shopify and get set csfr key.
        """
        login_info = {'login': USERNAME, 'password': PASSWORD}
        headers = {}
        response = self.session.post(LOGIN_URL, data=login_info, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        self.csfr = soup.find('meta', {'name': 'csrf-token'})['content']

    def _set_headers(self):
        self.headers = {}
        self.headers = {'X-CSRF-Token': self.csfr}
        self.headers['Content-Type'] = 'application/json'
        self.headers['Accept'] = 'application/json'

    def add_discount(self, discount):

        payload = {'authenticity_token': self.csfr,
                   'usage_limit_type': 'no_limit',
                   'discount': discount.to_dict()}

        r = self.session.post(DISCOUNT_URL, data=json.dumps(payload), headers=self.headers)
        return r
