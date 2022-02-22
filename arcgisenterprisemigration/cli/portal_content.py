import click
from ..arcgisenterprisemigration.load_content import LoadContentPortal
from ..arcgisenterprisemigration.main import LoginArcgisPortal


@click.command()
@click.argument('portal_url')
@click.argument('portal_username')
@click.argument('portal_password')
def load_cmd_portal_content(portal_url, portal_username, portal_password):
    _auth = LoginArcgisPortal(portal_url, portal_username, portal_password)
    _o_content = LoadContentPortal(_auth)
    _o_content.dump_portal_to_console()

if __name__ == '__main__':
    load_cmd_portal_content()
