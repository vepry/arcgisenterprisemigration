import arcpy
from ..config import ConfigCMD
import xml.dom.minidom as DOM


class AuthArcgisPortalPro():
    def __init__(self, url_portal, username_portal, password_portal) -> None:
        self.portal_url = url_portal
        self.auth = arcpy.SignInToPortal(url_portal, username_portal, password_portal)

class DeployArcgisPortalPro():
    def __init__(self, auth: AuthArcgisPortalPro, 
    aprx_path) -> None:
        self._config = ConfigCMD()
        self._auth = auth
        self._aprx = arcpy.mp.ArcGISProject(aprx_path)

    def deploy_service(self, svc_name, portal_folder, server_folder, lyr_mxd_path, copy_data_to_server = False, overwrite_service=False,
    credits='',summary='', tags='', description='', activate_feature_service=False):
        self.append_layer(lyr_mxd_path)
        self._prepare_map_service_portal_sd(svc_name, self._auth.portal_url, portal_folder, server_folder,
            copy_data_to_server, overwrite_service,
            credits,summary, tags, description, activate_feature_service)
        

    def append_layer(self, layer_mxd_path: str):
        self._aprx.importDocument(layer_mxd_path)

    def _prepare_map_service_portal_sd(self, svc_name, 
    portal_url, portal_folder, server_folder,
    copy_data_to_server = False, overwrite_service=False,
    credits='',summary='', tags='', description='', activate_feature_service=False):
        m = self._aprx.listMaps('*')[0]
        s_draft = arcpy.sharing.CreateSharingDraft('FEDERATED_SERVER','MAP_SERVICE', svc_name, m)
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
        out_file = self.activate_some_features(svc_name, self._config.deploy_sd_folder + svc_name + '.sddraft', activate_feature_service)
        sd_out_file = self._prepare_sd_file(svc_name, out_file)
        return sd_out_file

    def activate_some_features(self, svc_name, sddraft_path, 
    active_feature = False):
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


        
