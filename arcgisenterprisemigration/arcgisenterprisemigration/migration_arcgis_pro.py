import arcpy
from ..config import ConfigCMD
import xml.dom.minidom as DOM
import json, requests
import os
from requests.structures import CaseInsensitiveDict
from arcgis.gis.server import Server
from arcgisenterprisemigration.arcgisenterprisemigration.main import LoginArcgisPortal


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
        self._cookies = self._cookies if req.headers.get('set-cookie') == None else self._cookies + ';' +req.headers.get('set-cookie')

        # a = req.json()
        # self.token = a['token']
        # request = self.http.request('GET', self.url_generatetoken, fields=payloads)
        # data = request.data.encode('utf-8')

    def yui(self):
        header = CaseInsensitiveDict()
        header['Cookie'] = self._cookies
        a = requests.get('https://idepbpn-adgis03.ad.phm-pertamina.com:6443/arcgis/admin/services?f=pjson', headers=header)
        pass


class DeployArcgisPortalPro():
    def __init__(self, auth: AuthArcgisPortalPro, auth_api: LoginArcgisPortal) -> None:
        self._config = ConfigCMD()
        self._auth = auth
        self._auth_api = auth_api
        self._aprx = None

    def deploy_service(self, svc_name, portal_folder, server_folder, new_conn_str, lyr_mxd_path, copy_data_to_server=False,
                       overwrite_service=True,
                       credits='', summary='', tags='', description='', activate_feature_service=False, name_conn='sde'):
        self._prapare_aprx(self._config.template_aprx_path, lyr_mxd_path)
        self.append_layer(lyr_mxd_path)
        metadata = self._get_metadata()
        self._aprx.save()
        self.fixing_new_datasource(new_conn_str, name_conn)
        self._aprx.save()
        self._aprx.saveACopy(r"C:\Local\project\output\aprx"+"\\"+ svc_name + ".aprx")
        #del self._aprx
        #self._aprx.saveACopy(r"C:\Local\project\output\template2.aprx")
        # self._prepare_map_service_portal_sd(svc_name, self._auth.portal_url, portal_folder, server_folder,
                                            #copy_data_to_server, overwrite_service,
                                            #metadata.credits, metadata.summary, metadata.tags, metadata.description, activate_feature_service)

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
        if os.path.exists(self._config.template_deploy_path):
            os.remove(self._config.template_deploy_path)
        proj.saveACopy(self._config.template_deploy_path)
        self._aprx = arcpy.mp.ArcGISProject(self._config.template_deploy_path)

    def _server_connection(self):
        srv_conn = self._auth.auth


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

    def clone_item(self, source_portal_auth, svc_id):
        try:
            a = source_portal_auth.login_portal().content.get(svc_id)
            b = self._auth_api.login_portal()
            b.content.clone_items(items=[a])
        except Exception as e:
            pass

    def _prepare_sd_file(self, svc_name, sd_draft_file_path):
        outfile = self._config.deploy_sd_folder + svc_name + '.sd'
        arcpy.StageService_server(sd_draft_file_path, outfile)
        return outfile

    def create_folder(self, o_list_portal, l_server=[]):
        self._create_folder_portal(o_list_portal)
        if len(l_server) > 0:
            self._create_folder_server(l_server)

    def _create_folder_portal(self, o_list_portal):
        portal_content_manager = self._auth_api.login_portal().content
        for o_folder in o_list_portal:
            portal_content_manager.create_folder(o_folder['name'], o_folder['owner'])

    def _get_metadata(self):
        l_maps = self._aprx.listMaps()
        o_map = l_maps[0]
        obj = type('',(object,),{"credits":o_map.metadata.credits, "description": o_map.metadata.description, "tags": o_map.metadata.tags, "summary": o_map.metadata.summary, "title": o_map.metadata.title})()
        return obj

    def fixing_new_datasource(self, new_strc_conn, name_conn):
        l_maps = self._aprx.listMaps()
        o_map = l_maps[0]
        p_map = l_maps[1]
        pl_layer = p_map.listLayers()[0]
        t_connstr = pl_layer.connectionProperties
        lyrs = o_map.listLayers()
        for o_lyr in lyrs:
            try:
                if o_lyr.connectionProperties.get('connection_info') != None:
                    if o_lyr.connectionProperties['connection_info']['server'] == name_conn:
                        t_connstr['dataset'] = o_lyr.connectionProperties['dataset']
                        o_lyr.updateConnectionProperties(o_lyr.connectionProperties, t_connstr, validate=False)
                if o_lyr.connectionProperties.get('event_table_source') != None:
                    if o_lyr.connectionProperties['event_table_source']['connection_info']['server'] == name_conn:
                        temp_conn = o_lyr.connectionProperties
                        temp_conn['event_table_source']['connection_info'] = t_connstr['connection_info']
                        l_i = o_lyr.connectionProperties['event_table_source']['dataset'].split('.')
                        temp_conn['event_table_source']['dataset'] = 'geospatial.'+'.'.join(l_i[1:])
                        o_lyr.updateConnectionProperties(current_connection_info=o_lyr.connectionProperties, new_connection_info=temp_conn, validate=False)

            except Exception as e:
                pass
        

    def _phm_generate_xy_event_layer(self):
        pass


    def _create_folder_server(self, l_folder, server_role = 'HOSTING_SERVER'):
        svr_conn = self._auth_api.login_portal().admin.servers.get(role=server_role)
        l_s_folder = svr_conn[0].content.folders
        for o_folder in l_folder:
            if o_folder in l_s_folder:
                continue
            svc_manager = svr_conn[0].services
            svc_manager.create_folder(o_folder)
