from .main import LoginArcgisPortal
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.align import Align
from ..config import ConfigCMD
import csv
import json


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

    def dump_portal_to_csv(self):
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
        with Live(table_centered, console=console, screen=False, refresh_per_second=5):
            for user in l_user:
                u_content = user.items()
                for item in u_content:
                    table.add_row(item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(item.shared_with), 'root',user.username)
                folders = user.folders
                for folder in folders:
                    f_items = user.items(folder=folder['title'])
                    for item in f_items:
                        table.add_row(item.id, item.title, item.type, item.homepage, item.name, item.owner, json.dumps(item.shared_with), folder['title'],user.username)
                        