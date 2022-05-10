from arcgisenterprisemigration.arcgisenterprisemigration.load_user_role import LoadUserRoleArcgisPortal
from arcgisenterprisemigration.arcgisenterprisemigration.main import LoginArcgisPortal
from arcgisenterprisemigration.config import ConfigCMD
import os

portal_target_username = os.environ['ARCGIS_TARGET_PORTAL_USERNAME']
portal_target_password = os.environ['ARCGIS_TARGET_PORTAL_PASSWORD']
ags_target_username = os.environ['ARCGIS_TARGET_SERVER_USERNAME']
ags_target_password = os.environ['ARCGIS_TARGET_SERVER_PASSWORD']

portal_source_username = os.environ['ARCGIS_SOURCE_PORTAL_USERNAME']
portal_source_password = os.environ['ARCGIS_SOURCE_PORTAL_PASSWORD']
ags_source_username = os.environ['ARCGIS_SOURCE_SERVER_USERNAME']
ags_source_password = os.environ['ARCGIS_SOURCE_SERVER_PASSWORD']

portal_target_url = ''
portal_source_url = os.environ['ARCGIS_ENTERPRISE_SOURCE_URL']

config = ConfigCMD()
auth_portal_target = LoginArcgisPortal(portal_source_url, portal_source_username, portal_source_password)
user = LoadUserRoleArcgisPortal(auth_portal_target)
user.dump_portal_to_csv()
