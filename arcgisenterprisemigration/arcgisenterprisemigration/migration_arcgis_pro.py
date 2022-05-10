import arcpy
from ..config import ConfigCMD
import xml.dom.minidom as DOM
import json, requests
from requests.structures import CaseInsensitiveDict


class AuthArcgisPortalPro():
    def __init__(self, url_portal, username_portal, password_portal) -> None:
        self.portal_url = url_portal
        self.auth = arcpy.SignInToPortal(url_portal, username_portal, password_portal)

class AuthArcgisPortalRestPro():
    def __init__(self, url_portal, username_portal, password_portal):
        pass

class AuthArcgisServerRestPro():
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
        self._cookies = self._cookies + ';' +req.headers.get('set-cookie')

        # a = req.json()
        # self.token = a['token']
        # request = self.http.request('GET', self.url_generatetoken, fields=payloads)
        # data = request.data.encode('utf-8')

    def yui(self):
        header = CaseInsensitiveDict()
        header['Cookie'] = self._cookies
        a = requests.get('https://asdasdasda/arcgis/admin/services/batasdesa.MapServer?f=json', headers=header)
        pass


class DeployArcgisPortalPro():
    def __init__(self, auth: AuthArcgisPortalPro) -> None:
        self._config = ConfigCMD()
        self._auth = auth
        self._aprx = None

    def deploy_service(self, svc_name, portal_folder, server_folder, lyr_mxd_path, copy_data_to_server=False,
                       overwrite_service=False,
                       credits='', summary='', tags='', description='', activate_feature_service=False):
        self.append_layer(lyr_mxd_path)
        self._prepare_map_service_portal_sd(svc_name, self._auth.portal_url, portal_folder, server_folder,
                                            copy_data_to_server, overwrite_service,
                                            credits, summary, tags, description, activate_feature_service)

    def deploys(self):
        with open(self._config.list_svc_server_csv) as report_file:
            l_mapx = {}
            for mapxfilename in l_mapx:
                t_proj = arcpy.mp.ArcGISProject('')
                t_proj.importDocument(l_mapx[mapxfilename]['file'])
                l_maps = t_proj.listMaps()
                for o_map in l_maps:
                    sd_file = ''
                    sddraft_file = ''
                    try:
                        pass
                    except Exception as e:
                        pass

    def append_layer(self, layer_mxd_path: str):
        self._aprx.importDocument(layer_mxd_path)

    def _prapare_aprx(self, path_template_aprx, file_path_lyr):
        proj = arcpy.mp.ArcGISProject(path_template_aprx)
        proj.saveACopy(self._config.template_deploy_path)
        self._aprx = arcpy.mp.ArcGISProject(self._config.template_deploy_path)


    def _prepare_map_service_portal_sd(self, svc_name,
                                       portal_url, portal_folder, server_folder,
                                       copy_data_to_server=False, overwrite_service=False,
                                       credits='', summary='', tags='', description='', activate_feature_service=False):
        m = self._aprx.listMaps('*')[0]
        s_draft = arcpy.sharing.CreateSharingDraft('FEDERATED_SERVER', 'MAP_SERVICE', svc_name, m)
        s_draft.copyDataToServer = copy_data_to_server
        s_draft.overwriteExistingService = overwrite_service
        s_draft.portalFolder = portal_folder
        s_draft.serverFolder = server_folder
        s_draft.federatedServerUrl = portal_url
        s_draft.targetServer = portal_url
        s_draft.credits = credits
        s_draft.summary = summary
        s_draft.tags = tags
        s_draft.description = description

        s_draft.exportToSDDraft(self._config.deploy_sd_folder + svc_name + '.sddraft')
        out_file = self.activate_some_features(svc_name, self._config.deploy_sd_folder + svc_name + '.sddraft',
                                               activate_feature_service)
        sd_out_file = self._prepare_sd_file(svc_name, out_file)
        return sd_out_file

    def activate_some_features(self, svc_name, sddraft_path,
                               active_feature=False):
        doc = DOM.parse(sddraft_path)
        typeNames = doc.getElementsByTagName('TypeName')
        for typeName in typeNames:
            if active_feature:
                if typeName.firstChild.data == 'FeatureServer':
                    extension = typeName.parentNode
                    for extElement in extension.childNodes:
                        if extElement.tagName == 'Enabled':
                            extElement.firstChild.data = 'true'
                        if extElement.tagName == 'Info':
                            for propSet in extElement.childNodes:
                                for prop in propSet.childNodes:
                                    for prop1 in prop.childNodes:
                                        if prop1.tagName == "Key":
                                            if prop1.firstChild.data == 'WebCapabilities':
                                                # Defaults are Query,Create,Update,Delete,Uploads,Editing
                                                prop1.nextSibling.firstChild.data = "Create,Sync,Query"

        if active_feature:
            pass
        outFile = self._config.deploy_sd_folder + svc_name + '_2.sddraft'
        f = open(outFile, 'w')
        doc.writexml(f)
        f.close()
        return outFile

    def _prepare_sd_file(self, svc_name, sd_draft_file_path):
        outfile = self._config.deploy_sd_folder + svc_name + '.sd'
        arcpy.StageService_server(sd_draft_file_path, outfile)
        return outfile
