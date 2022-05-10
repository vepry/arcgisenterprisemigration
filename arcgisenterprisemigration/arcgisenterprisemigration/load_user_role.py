from .main import LoginArcgisPortal
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.align import Align
from ..config import ConfigCMD
import csv


class LoadUserRoleArcgisPortal():
    def __init__(self, auth: LoginArcgisPortal) -> None:
        self._auth = auth

    def dump_portal_to_console(self):
        o_portal = self._auth.login_portal()
        l_user = o_portal.users.search('')
        console = Console()
        table = Table(show_header=True)
        table.add_column("Username")
        table.add_column("FirstName")
        table.add_column('LastName')
        table.add_column('Email')
        table.add_column("Role")
        for user in l_user:
            table.add_row(user.username, user.firstName, user.lastName, user.email, str(user.role))
        console.print(table)

    def dump_portal_to_csv(self):
        conf = ConfigCMD()
        o_portal = self._auth.login_portal()
        l_user = o_portal.users.search('')
        console = Console()
        table = Table(show_header=True)
        table.add_column("Username")
        table.add_column("FirstName")
        table.add_column('LastName')
        table.add_column('Email')
        table.add_column("Role")
        table_centered = Align.left(table)
        with open(conf.user_role_out_file, 'w', newline='\n') as csvfile:
            try:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow(
                    ['Username', 'FirstName', 'LastName', 'Email', 'Role'])
                csvfile.flush()
                with Live(table_centered, console=console, screen=False, auto_refresh=False) as live:
                    for user in l_user:
                        csvwriter.writerow([user.username, user.firstName, user.lastName, user.email, str(user.role)])
                        table.add_row(user.username, user.firstName, user.lastName, user.email, str(user.role))
                        live.refresh()
                        csvfile.flush()
            except Exception as e:
                csvfile.close()
