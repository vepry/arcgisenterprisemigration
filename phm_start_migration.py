from arcgisenterprisemigration.arcgisenterprisemigration.migration_arcgis_pro import DeployArcgisPortalPro, AuthArcgisPortalPro
import os

portal_target_username = os.environ['ARCGIS_SOURCE_PORTAL_USERNAME']
portal_target_password = os.environ['ARCGIS_SOURCE_PORTAL_PASSWORD']
ags_target_username = os.environ['ARCGIS_SOURCE_SERVER_USERNAME']
ags_target_password = os.environ['ARCGIS_SOURCE_SERVER_PASSWORD']

portal_source_username = os.environ['ARCGIS_TARGET_PORTAL_USERNAME']
portal_source_password = os.environ['ARCGIS_TARGET_PORTAL_PASSWORD']
ags_source_username = os.environ['ARCGIS_TARGET_SERVER_USERNAME']
ags_source_password = os.environ['ARCGIS_TARGET_SERVER_PASSWORD']

portal_target_url = ''
server_target_url = ''

portal_source_url = ''
server_source_url = ''

auth_portal_target = AuthArcgisPortalPro(portal_target_url, portal_target_username, portal_target_password)
deploy_target = DeployArcgisPortalPro(auth_portal_target)

