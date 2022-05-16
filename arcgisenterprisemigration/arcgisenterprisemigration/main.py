from arcgis.gis import GIS
from arcgis.gis.server import Server
import requests

class LoginArcgisPortal():
    def __init__(self, url_portal=None, username_portal=None, password_portal=None, url_server=None, username_server=None, password_server=None) -> None:
        self._url_portal = url_portal
        self._username_portal = username_portal
        self._password_portal = password_portal
        self._url_server = url_server
        self._username_server = username_server
        self._password_server = password_server

    def login_portal(self):
        return GIS(self._url_portal, username=self._username_portal, password=self._password_portal, verify_cert=False)
    
    def login_iwa(self):
        return GIS(self._url_portal )

    def login_server_w_portal(self):
        gis = self.login_portal()
        return Server(self._url_server, gis=gis)

    def login_server(self):
        return Server(url=self._url_server, username=self._username_server, password=self._password_server)

class LoginArcgisServerRest():
    def __init__(self, url_portal, url_server, username_server, password_server):
        self.url_portal = url_portal
        self.url_server_admin = url_server + '/admin'
        # self.url_generatetoken = url_portal + '/sharing/rest/generateToken'
        self.url_generatetoken = url_server + '/admin/login?redirect='
        self.username_server = username_server
        self.password_server = password_server

    def generate_token(self):
        # payloads = {
        #     'username': self.username_server,
        #     'password': self.password_server,
        #     'client': 'referer',
        #     'referer': self.url_portal,
        #     'expiration': 60,
        #     'f': 'json'
        # }
        payloads = {
            'username': self.username_server,
            'password': self.password_server,
            'portalToken': '',
            'referer': ''
        }
        # req = requests.get(self.url_generatetoken, params=payloads, verify=False)
        req = requests.post(self.url_generatetoken, data=payloads, verify=False)
        self._cookies = req.request.headers.get('Cookie')
        self._cookies = self._cookies if req.headers.get('set-cookie') == None else self._cookies + ';' +req.headers.get('set-cookie')
