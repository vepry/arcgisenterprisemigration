from arcgisenterprisemigration.arcgisenterprisemigration.migration_arcgis_pro import DeployArcgisPortalPro, AuthArcgisServerRestPro, AuthArcgisPortalPro
from arcgisenterprisemigration.config import ConfigCMD
import os
from arcgisenterprisemigration.arcgisenterprisemigration.load_content import LoadContentServerRest

portal_target_username = os.environ['ARCGIS_TARGET_PORTAL_USERNAME']
portal_target_password = os.environ['ARCGIS_TARGET_PORTAL_PASSWORD']
ags_target_username = os.environ['ARCGIS_TARGET_SERVER_USERNAME']
ags_target_password = os.environ['ARCGIS_TARGET_SERVER_PASSWORD']

portal_source_username = os.environ['ARCGIS_SOURCE_PORTAL_USERNAME']
portal_source_password = os.environ['ARCGIS_SOURCE_PORTAL_PASSWORD']
ags_source_username = os.environ['ARCGIS_SOURCE_SERVER_USERNAME']
ags_source_password = os.environ['ARCGIS_SOURCE_SERVER_PASSWORD']

portal_target_url = os.environ['ARCGIS_ENTERPRISE_TARGET_URL']
server_target_url = ''

portal_source_url = os.environ['ARCGIS_ENTERPRISE_SOURCE_URL']
server_source_url = os.environ['ARCGIS_ENTERPRISE_SOURCE_URL']

config = ConfigCMD()
auth_source_server = AuthArcgisServerRestPro('https://idepbpn-adgis03.ad.phm-pertamina.com/geoportal', 'https://idepbpn-adgis03.ad.phm-pertamina.com:6443/arcgis', ags_source_username, ags_source_password)
load_content_server = LoadContentServerRest(auth_source_server)
load_content_server.dump_to_csv()
