from .main import LoginArcgisServerRest, LoginArcgisPortal
from arcgisenterprisemigration.config import ConfigCMD
from requests.structures import CaseInsensitiveDict
import requests
from arcgis.gis.server import Service

class MappingServiceServer():
    def __init__(self, auth: LoginArcgisServerRest = None, auth_api: LoginArcgisPortal = None) -> None:
        self._auth = auth
        self._auth_api = auth_api

    def save_properties(self, service_name, folder, service_type, properties_data):
        config = ConfigCMD()
        self._auth.generate_token()
        url_service = 'https://app-gis-dev.pertamina.com:6443/arcgis' + '/admin/services/'+folder+"/"+service_name+"."+service_type+'?f=pjson'
        header = CaseInsensitiveDict()
        header['Cookie'] = self._auth._cookies
        res = requests.get(url_service, headers=header)
        o_data = res.json()
        o_data['capabilities'] = properties_data['capabilities']
        o_data['extensions'] = properties_data['extensions']

    def save_properties_api(self, service_name, folder, service_type, properties_data):
        config = ConfigCMD()
        _server_api = self._auth_api.login_server_w_portal()
        _service = _server_api.content.get(service_name, folder)


