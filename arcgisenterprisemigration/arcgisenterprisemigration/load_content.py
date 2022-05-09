from .main import LoginArcgisPortal
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.align import Align
from ..config import ConfigCMD
import csv
import json
from arcgis.gis.server.catalog import ServicesDirectory


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

