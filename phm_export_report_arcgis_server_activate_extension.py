from arcgisenterprisemigration.arcgisenterprisemigration.migration_arcgis_pro import DeployArcgisPortalPro, AuthArcgisServerRestPro, AuthArcgisPortalPro
from arcgisenterprisemigration.config import ConfigCMD
import os
from arcgisenterprisemigration.arcgisenterprisemigration.load_content import LoadContentServerRest
import csv
import json
from arcgisenterprisemigration.arcgisenterprisemigration.mapping_func_service import MappingServiceServer

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
auth_source_server = AuthArcgisServerRestPro('https://geoportaldev.phm.pertamina.com/geoportal', 'https://app-gis-dev.pertamina.com:6443/arcgis', ags_target_username, ags_target_password)


with open(config.list_svc_server_csv, 'r') as report_server_file:
    csv_server_report = csv.reader(report_server_file, delimiter=';')
    i_r_server = 0
    for l_r_server in csv_server_report:
        if i_r_server == 0:
            i_r_server = i_r_server + 1
            continue
        temp_str = l_r_server[3].replace("'", '"')
        f_data = json.loads(temp_str)
        o_svc = MappingServiceServer(auth_source_server)
        o_svc.save_properties(l_r_server[0], l_r_server[1], 'MapServer', f_data)
        a= ''
