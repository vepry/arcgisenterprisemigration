from arcgis.gis import GIS

class LoginArcgisPortal():
    def __init__(self, url_portal, username_portal, password_portal, url_server=None, username_server=None, password_server=None) -> None:
        self._url_portal = url_portal
        self._username_portal = username_portal
        self._password_portal = password_portal
        self._url_server = url_server
        self._username_server = username_server
        self._password_server = password_server

    def login_portal(self):
        return GIS(self._url_portal, self._username_portal, self._password_portal, verify_cert=False)