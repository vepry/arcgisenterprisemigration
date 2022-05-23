from arcgisenterprisemigration.arcgisenterprisemigration.migration_arcgis_pro import DeployArcgisPortalPro, AuthArcgisPortalPro
from arcgisenterprisemigration.config import ConfigCMD
from arcgisenterprisemigration.arcgisenterprisemigration.main import LoginArcgisPortal
import os
import csv
import time

portal_target_username = os.environ['ARCGIS_TARGET_PORTAL_USERNAME']
portal_target_password = os.environ['ARCGIS_TARGET_PORTAL_PASSWORD']
ags_target_username = os.environ['ARCGIS_TARGET_SERVER_USERNAME']
ags_target_password = os.environ['ARCGIS_TARGET_SERVER_PASSWORD']

portal_source_username = os.environ['ARCGIS_SOURCE_PORTAL_USERNAME']
portal_source_password = os.environ['ARCGIS_SOURCE_PORTAL_PASSWORD']
ags_source_username = os.environ['ARCGIS_SOURCE_SERVER_USERNAME']
ags_source_password = os.environ['ARCGIS_SOURCE_SERVER_PASSWORD']

portal_target_url = 'https://geoportaldev.phm.pertamina.com/geoportal'
server_target_url = 'https://geoportaldev.phm.pertamina.com/arcgis'

portal_source_url = 'https://idepbpn-adgis03.ad.phm-pertamina.com/geoportal'
server_source_url = ''

config = ConfigCMD()

auth_portal_api_source = LoginArcgisPortal(portal_source_url, portal_source_username, portal_source_password)

auth_portal_pro_target = AuthArcgisPortalPro(portal_target_url, portal_target_username, portal_target_password)
auth_portal_api_target = LoginArcgisPortal(portal_target_url, portal_target_username, portal_target_password)
deploy_portal_target = DeployArcgisPortalPro(auth_portal_pro_target, auth_portal_api_target)

t_connstr_gisdbphmdev= "ENCRYPTED_PASSWORD=00022e68392b38474f796f6c5534396d69716a537058656c2f68594d3473716e4f7866364b4b6f6f6c5a54717042453d2a00;SERVER=GEODBPHMDEV;INSTANCE=sde:oracle11g:GEODBPHMDEV;DBCLIENT=oracle;DB_CONNECTION_PROPERTIES=GEODBPHMDEV;PROJECT_INSTANCE=sde;USER=geospatial;VERSION=SDE.DEFAULT;AUTHENTICATION_MODE=DBMS"
uri_arcgisinput = "C:\\Local\\EsriIndonnesia\\arcgisinput\\"
token_r_arcgisinput = 'D:\\agsserver\\directories\\arcgissystem\\arcgisinput\\'
uri_template_aprx = ''

new_projection = 'PROJCS["Gunung_Segara_UTM_Zone_50S",GEOGCS["GCS_Gunung_Segara",DATUM["D_Gunung_Segara",SPHEROID["Bessel_1841",6377397.155,299.1528128]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5120200 3000 10000;0 1;0 1;0.001;0.001;0.001;IsHighPrecision'

l_folder_portal = []
l_folder_server = []

def list_folder_server(config, l_folder_server):
    with open(config.list_svc_server_csv) as report_server_file:
            csv_server_report = csv.reader(report_server_file, delimiter=';')
            i_r_server = 0
            for l_r_server in csv_server_report:
                if  i_r_server == 0:
                    i_r_server = i_r_server + 1
                    continue
                if l_r_server[1] in l_folder_server:
                    continue
                l_folder_server.append(l_r_server[1])

def list_folder_portal(config, l_folder_portal):
    with open(config.list_svc_portal_csv) as report_portal_file:
        csv_portal_report = csv.reader(report_portal_file, delimiter=';')
        i_r_portal = 0
        for l_r_portal in csv_portal_report:
            if  i_r_portal == 0:
                i_r_portal = i_r_portal + 1
                continue
            if l_r_portal[7] == "root":
                continue
            flag_add = False
            for o_main_folder_portal in l_folder_portal:
                if l_r_portal[5] == o_main_folder_portal['owner']:
                    if l_r_portal[7] == o_main_folder_portal['name']:
                        flag_add = False
                        break
                flag_add = True
            if flag_add:
                l_folder_portal.append({'owner':l_r_portal[5],'name':l_r_portal[7]})

def step_deploy(config, deploy_portal_target, uri_arcgisinput, token_r_arcgisinput):

    skip_folders = ['Hosted', 'System', 'Utilities']

    with open(config.deploy_report_service_file, 'w', newline='\n') as deployment_report:
        reportwriter = csv.writer(deployment_report, delimiter=';')
        reportwriter.writerow(['id_old','svc_name','svc_type','owner_old','folder','status','err_msg'])
        with open(config.list_svc_portal_csv, 'r') as report_portal_file:
            csv_portal_report = csv.reader(report_portal_file, delimiter=';')
            i_r_server = 0
            i_r_portal = 0
            p = 0
            for l_r_portal in csv_portal_report:
                if i_r_portal == 0:
                    i_r_portal = i_r_portal + 1
                    continue
                with open(config.list_svc_server_csv, 'r') as report_server_file:
                    #make report ada beberapa mx yg ga ada di config store
                    csv_server_report = csv.reader(report_server_file, delimiter=';')
                    i_r_server = 0
                    for l_r_server in csv_server_report:
                        if i_r_server == 0:
                            i_r_server = i_r_server + 1
                            continue
                        if l_r_portal[1] != l_r_server[0]:
                            continue
                        if l_r_server[1] == 'Hosted':
                            try:
                                # deploy_portal_target.clone_item(auth_portal_api_source, l_r_portal[0])
                                reportwriter.writerow(
                                    [l_r_portal[0], l_r_portal[1], l_r_portal[2], l_r_portal[5], l_r_portal[7],
                                     'Success', ''])
                            except Exception as e:
                                reportwriter.writerow([l_r_portal[0], l_r_portal[1], l_r_portal[2], l_r_portal[5], l_r_portal[7], 'Failed', 'Ini service hosted..'])
                            deployment_report.flush()
                            continue
                        if l_r_server[1] in skip_folders:
                            continue
                        # if os.path.exists(r"C:\Local\project\output\aprx"+"\\"+ l_r_portal[1] + ".aprx"):
                        #     continue
                        url_mxd_file = l_r_server[2].replace(token_r_arcgisinput, uri_arcgisinput)
                        url_mxd_file = url_mxd_file.replace('.msd', '.mxd')
                        if os.path.exists(url_mxd_file) == False:
                            reportwriter.writerow([l_r_portal[0], l_r_portal[1], l_r_portal[2], l_r_portal[5], l_r_portal[7], 'Failed', 'Mxd tidak ada..'])
                            deployment_report.flush()
                            continue
                        #check mxd

                        try:
                            deploy_portal_target = DeployArcgisPortalPro(auth_portal_pro_target, auth_portal_api_target)
                            deploy_portal_target.deploy_service(l_r_portal[1], l_r_portal[7], l_r_server[1], t_connstr_gisdbphmdev, url_mxd_file, name_conn='gisdbphmdev')
                            reportwriter.writerow(
                                [l_r_portal[0], l_r_portal[1], l_r_portal[2], l_r_portal[5], l_r_portal[7],
                                 'Success', ''])
                            deployment_report.flush()
                            time.sleep(15)
                        except Exception as e:
                            reportwriter.writerow(
                                [l_r_portal[0], l_r_portal[1], l_r_portal[2], l_r_portal[5], l_r_portal[7],
                                 'Failed', str(e).replace('\n','').replace('"', '').replace('\t','').replace(' ','')])
                            deployment_report.flush()
                            del deploy_portal_target
                            time.sleep(15)


def change_ownership_portal():
    auth_portal_t = auth_portal_api_target.login_portal()
    l_user = auth_portal_t.users.search('')
    for user in l_user:
        u_content = user.items()
        for item in u_content:
            with open('') as report_content_portal:
                csv_content_portal_report = csv.reader(report_content_portal, delimiter=';')
                i_r_portal = 0
                for o_portal in csv_content_portal_report:
                    if i_r_portal == 0:
                        i_r_portal = i_r_portal + 1
                        continue
                    if o_portal[1] != item.title:
                        continue
                    if o_portal[5] == 'agpadmin':
                        continue
                    with open() as user_map:
                        csv_user_map = csv.reader(user_map, delimiter=';')
                        i_r_user = 0
                        for user_report in csv_user_map:
                            if i_r_user == 0:
                                i_r_user = i_r_user + 1
                                continue
                            if user_report[0] != o_portal[5]:
                                continue
                            item.reassign_to(user_report[1])



# arcpy.management.XYTableToPoint(r"C:\Local\EsriIndonnesia\geospatial@geodbphmdev.sde\GEOSPATIAL.WELL", r"C:\Users\L0300800\Documents\ArcGIS\Projects\MyProject\MyProject.gdb\WELL_XYTableToPoint", "X_OLD", "Y_OLD", None, 'PROJCS["Gunung_Segara_UTM_Zone_50S",GEOGCS["GCS_Gunung_Segara",DATUM["D_Gunung_Segara",SPHEROID["Bessel_1841",6377397.155,299.1528128]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5120200 3000 10000;0 1;0 1;0.001;0.001;0.001;IsHighPrecision')

list_folder_server(config, l_folder_server)
list_folder_portal(config, l_folder_portal)
# deploy_portal_target.create_folder(l_folder_portal, l_folder_server)

step_deploy(config, deploy_portal_target, uri_arcgisinput, token_r_arcgisinput)

change_ownership_portal()




