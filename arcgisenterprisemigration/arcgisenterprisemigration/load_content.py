from .main import LoginArcgisPortal, LoginArcgisServerRest
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.align import Align
from ..config import ConfigCMD
import csv
import json
from arcgis.gis.server.catalog import ServicesDirectory
from requests.structures import CaseInsensitiveDict
import requests


class LoadContentPortal():
    def __init__(self, auth: LoginArcgisPortal) -> None:
        self._auth = auth

    def dump_portal_to_console(self):
        o_portal = self._auth.login_portal()
        l_user = o_portal.users.search('!esri_ & !admin')
        console = Console()
        table = Table(show_header=True)
        table.add_column("id")
        table.add_column("title")
        table.add_column('type')
        table.add_column('homepage')
        table.add_column("name")
        table.add_column("owner")
        table.add_column('shared_with')
        table.add_column('folder')
        table.add_column('user')
        table_centered = Align.left(table)
        with Live(table_centered, console=console, screen=False, auto_refresh=False) as live:
            for user in l_user:
                u_content = user.items()
                for item in u_content:
                    table.add_row(item.id, item.title, item.type, item.homepage, item.name,
                                  item.owner, json.dumps(item.shared_with), 'root', user.username)
                    live.refresh()
                folders = user.folders
                for folder in folders:
                    f_items = user.items(folder=folder['title'])
                    for item in f_items:
                        table.add_row(item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(
                            item.shared_with), folder['title'], user.username)
                        live.refresh()

    def dump_server_to_console(self):
        config = ConfigCMD()
        o_server = self._auth.login_server_w_portal()
        o_content_svc = o_server.content
        l_folder = o_content_svc.folders
        for i_folder in l_folder:
            l_svc = o_content_svc.list(i_folder)
            for i_svc in l_svc:
                pass

    def dump_portal_to_csv(self):
        conf = ConfigCMD()
        o_portal = self._auth.login_portal()
        l_user = o_portal.users.search('!esri_ & !admin')
        console = Console()
        table = Table(show_header=True)
        table.add_column("id")
        table.add_column("title")
        table.add_column('type')
        table.add_column('homepage')
        table.add_column("name")
        table.add_column("owner")
        table.add_column('shared_with')
        table.add_column('folder')
        table.add_column('user')
        table_centered = Align.left(table)

        with open(conf.portal_contents_out_file, 'w', newline='\n') as csvfile:
            try:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(['id','title','type','homepage','name','owner','shared_with', 'folder','user'])
                with Live(table_centered, console=console, screen=False, refresh_per_second=5):
                    for user in l_user:
                        u_content = user.items()
                        for item in u_content:
                            table.add_row(item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(item.shared_with), 'root',user.username)
                            csvwriter.writerow([item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(item.shared_with), 'root',user.username])
                        folders = user.folders
                        for folder in folders:
                            f_items = user.items(folder=folder['title'])
                            for item in f_items:
                                table.add_row(item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(item.shared_with), folder['title'],user.username)
                                csvwriter.writerow([item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(item.shared_with), 'root',user.username])
            except Exception as e:
                csvfile.close()


class LoadContentServer():
    def __init__(self, auth: LoginArcgisPortal) -> None:
        self._auth = auth

    def dump_server_to_console(self):
        config = ConfigCMD()
        #o_server = self._auth.login_server()
        # o_server = self._auth.login_server_w_portal()
        o_arc = ServicesDirectory(config.arcgis_enterprise_source_url, config.arcgis_source_portal_username, config.arcgis_source_portal_password)
        # o_content_svc = o_server.content
        l_folder = o_arc.admin.services.folders
        console = Console()
        table = Table(show_header=True)
        table.add_column("name")
        table.add_column("filePath")
        table_centered = Align.left(table)
        with Live(table_centered, console=console, screen=False, auto_refresh=False) as live:
            for i_folder in l_folder:
                l_svc = o_arc.admin.services.list(i_folder)
                for i_svc in l_svc:
                    try:
                        svc_name = i_svc.properties.get('serviceName')
                        svc_file = i_svc.properties.get('properties')['filePath']
                        table.add_row(svc_name, svc_file)
                    except Exception as e:
                        continue
                    live.refresh()
                # table.add_row()

    def dump_server_to_csv(self):
        config = ConfigCMD()
        # o_server = self._auth.login_server()
        # o_server = self._auth.login_server_w_portal()
        o_arc = ServicesDirectory(config.arcgis_enterprise_source_url, config.arcgis_source_portal_username,
                                  config.arcgis_source_portal_password)
        # o_content_svc = o_server.content
        l_folder = o_arc.admin.services.folders
        console = Console()
        table = Table(show_header=True)
        table.add_column("name")
        table.add_column("filePath")
        table_centered = Align.left(table)
        with open(config.server_contents_out_file, 'w', newline='\n') as csvfile:
            try:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(
                    ['name', 'filePath'])
                with Live(table_centered, console=console, screen=False, auto_refresh=False) as live:
                    for i_folder in l_folder:
                        l_svc = o_arc.admin.services.list(i_folder)
                        for i_svc in l_svc:
                            try:
                                svc_name = i_svc.properties.get('serviceName')
                                svc_file = i_svc.properties.get('properties')['filePath']
                                table.add_row(svc_name, svc_file)
                                csvwriter.writerow([svc_name, svc_file])
                                csvfile.flush()
                            except Exception as e:
                                continue
                            live.refresh()
                        # table.add_row()
            except Exception as e:
                pass
            csvfile.close()


class LoadContentServerRest():
    def __init__(self, auth: LoginArcgisServerRest) -> None:
        self._auth = auth

    def dump_to_console(self):
        pass
    def dump_to_csv(self):
        config = ConfigCMD()
        self._auth.generate_token()
        console = Console()
        table = Table(show_header=True)
        table.add_column("name")
        table.add_column("folder")
        table.add_column("filePath")
        table_centered = Align.left(table)

        with open(config.server_contents_out_file, 'w', newline='\n') as csvfile:
            try:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(
                    ['name', 'folder', 'filePath','rawProperties'])
                with Live(table_centered, console=console, screen=False, auto_refresh=False) as live:
                    url_service = 'https://idepbpn-adgis03.ad.phm-pertamina.com:6443/arcgis' + '/admin/services?f=pjson'
                    header = CaseInsensitiveDict()
                    header['Cookie'] = self._auth._cookies
                    res = requests.get(url_service, headers=header)
                    o_data = res.json()
                    for o_folder in o_data['folders']:
                        url_svc_prop = 'https://idepbpn-adgis03.ad.phm-pertamina.com:6443/arcgis' + '/admin/services/'+o_folder+'?f=pjson'
                        res_svc = requests.get(url_svc_prop, headers=header)
                        l_svc = res_svc.json()
                        for o_svc in l_svc['services']:
                            try:
                                url_svc_i_prop = 'https://idepbpn-adgis03.ad.phm-pertamina.com:6443/arcgis' + '/admin/services/'+o_folder+"/"+o_svc['serviceName']+"."+o_svc['type']+'?f=pjson'
                                req_i_prop = requests.get(url_svc_i_prop, headers=header)
                                data_svc = req_i_prop.json()
                                filePath = data_svc['properties']['filePath']
                                table.add_row(o_svc['serviceName'], o_folder, filePath)
                                csvwriter.writerow([o_svc['serviceName'], o_folder, filePath, json.dumps(data_svc)])
                                csvfile.flush()
                                live.refresh()
                            except Exception as e:
                                continue
            except Exception as e:
                pass
            csvfile.close()

