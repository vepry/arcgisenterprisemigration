import arcpy


class AuthArcgisPortalPro():
    def __init__(self, url_portal, username_portal, password_portal) -> None:
        self.auth = arcpy.SignInToPortal(url_portal, username_portal, password_portal)

class DeployArcgisPortalPro():
    def __init__(self, auth: AuthArcgisPortalPro, aprx_path) -> None:
        self._auth = auth
        self._aprx = arcpy.mp.ArcGISProject(aprx_path)

    def append_layer(self, layer_mxd_path: str):
        self._aprx.importDocument(layer_mxd_path)