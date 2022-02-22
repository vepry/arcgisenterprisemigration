import click
from ..arcgisenterprisemigration.load_user_role import LoadUserRoleArcgisPortal
from ..arcgisenterprisemigration.main import LoginArcgisPortal


@click.command()
@click.argument('portal_url')
@click.argument('portal_username')
@click.argument('portal_password')
def load_cmd_users_roles(portal_url, portal_username, portal_password):
    _auth = LoginArcgisPortal(portal_url, portal_username, portal_password)
    _o_user = LoadUserRoleArcgisPortal(_auth)
    _o_user.dump_portal_to_console()

@click.command()
@click.argument('portal_url')
@click.argument('portal_username')
@click.argument('portal_password')
def load_csv_users_roles(portal_url, portal_username, portal_password):
    _auth = LoginArcgisPortal(portal_url, portal_username, portal_password)
    _o_user = LoadUserRoleArcgisPortal(_auth)
    _o_user.dump_portal_to_csv()

if __name__ == '__main__':
    load_cmd_users_roles()