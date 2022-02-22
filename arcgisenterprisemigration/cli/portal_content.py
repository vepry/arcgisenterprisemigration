import click
from ..arcgisenterprisemigration.load_content import LoadContentPortal
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
