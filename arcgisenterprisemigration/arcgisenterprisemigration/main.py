from arcgis.gis import GIS
from arcgis.gis.server import Server

class LoginArcgisPortal():
    def __init__(self, url_portal=None, username_portal=None, password_portal=None, url_server=None, username_server=None, password_server=None) -> None:
        self._url_portal = url_portal
        self._username_portal = username_portal
        self._password_portal = password_portal
        self._url_server = url_server
        self._username_server = username_server
        self._password_server = password_server

    def login_portal(self):
        return GIS(self._url_portal, self._username_portal, self._password_portal, verify_cert=False)

    def login_server_w_portal(self):
        gis = self.login_portal()
        return Server(self._url_server, gis=gis)

    def login_server(self):
        return Server(url=self._url_server, username=self._username_server, password=self._password_server)
