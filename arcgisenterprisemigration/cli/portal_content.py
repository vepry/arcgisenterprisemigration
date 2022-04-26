import click
from ..arcgisenterprisemigration.load_content import LoadContentPortal, LoadContentServer
from ..arcgisenterprisemigration.main import LoginArcgisPortal
import threading
import time
import signal


@click.command()
@click.argument('portal_url')
@click.argument('portal_username')
@click.argument('portal_password')
def load_cmd_portal_content(portal_url, portal_username, portal_password):
    _auth = LoginArcgisPortal(portal_url, portal_username, portal_password)
    _o_content = LoadContentPortal(_auth)
    class TThread(threading.Thread):
        def __init__(self, *args, **keywords) -> None:
            threading.Thread.__init__(self, *args, **keywords)
            
        def kill(self):
            raise SystemExit()
    t1 = TThread(target=_o_content.dump_portal_to_console, daemon=True)
    
    def handler(signum, frame):
        t1.kill()
    signal.signal(signal.SIGINT, handler)
    t1.start()
    while(t1.is_alive()):
        time.sleep(1)

@click.command()
@click.argument('portal_url')
@click.argument('portal_username')
@click.argument('portal_password')
@click.argument('server_url')
def load_cmd_portal_server_content(portal_url, portal_username, portal_password, server_url):
    _auth = LoginArcgisPortal(portal_url, portal_username, portal_password, server_url)
    _o_content = LoadContentPortal(_auth)
    class TThread(threading.Thread):
        def __init__(self, *args, **keywords) -> None:
            threading.Thread.__init__(self, *args, **keywords)
            
        def kill(self):
            raise SystemExit()
    t1 = TThread(target=_o_content.dump_server_to_console, daemon=True)
    
    def handler(signum, frame):
        t1.kill()
    signal.signal(signal.SIGINT, handler)
    t1.start()
    while(t1.is_alive()):
        time.sleep(1)

@click.command()
@click.argument('server_url')
@click.argument('server_username')
@click.argument('server_password')
def load_cmd_server_content(server_url, server_username, server_password):
    _auth = LoginArcgisPortal(url_server=server_url, username_server=server_username, password_server=server_password)
    _o_content = LoadContentServer(_auth)
    class TThread(threading.Thread):
        def __init__(self, *args, **keywords) -> None:
            threading.Thread.__init__(self, *args, **keywords)
            
        def kill(self):
            raise SystemExit()
    t1 = TThread(target=_o_content.dump_to_console, daemon=True)
    
    def handler(signum, frame):
        t1.kill()
    signal.signal(signal.SIGINT, handler)
    t1.start()
    while(t1.is_alive()):
        time.sleep(1)


@click.command()
@click.argument('portal_url')
@click.argument('portal_username')
@click.argument('portal_password')
def load_csv_portal_content(portal_url, portal_username, portal_password):
    _auth = LoginArcgisPortal(portal_url, portal_username, portal_password)
    _o_content = LoadContentPortal(_auth)
    class TThread(threading.Thread):
        def __init__(self, *args, **keywords) -> None:
            threading.Thread.__init__(self, *args, **keywords)
            
        def kill(self):
            raise SystemExit()
    t1 = TThread(target=_o_content.dump_portal_to_csv, daemon=True)
    
    def handler(signum, frame):
        t1.kill()
    signal.signal(signal.SIGINT, handler)
    t1.start()
    while(t1.is_alive()):
        time.sleep(1)

if __name__ == '__main__':
    load_cmd_portal_content()
