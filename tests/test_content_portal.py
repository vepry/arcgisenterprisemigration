import unittest
from click.testing import CliRunner
from arcgisenterprisemigration.cli import portal_content


class TestPortalContentDump(unittest.TestCase):
    def test_load_to_console(self):
        runner = CliRunner()
        result = runner.invoke(portal_content.load_cmd_portal_content, ['', '', ''])

    def test_load_server_to_console(self):
        runner = CliRunner()
        # result = runner.invoke(portal_content.load_cmd_portal_server_content, ['https://peta.gakkum.menlhk.go.id/portal', 'portaladmin', 'Passw0rd1234', 'https://peta.gakkum.menlhk.go.id/arcis/admin'])
        result = runner.invoke(portal_content.load_cmd_server_content, ['https://peta.gakkum.menlhk.go.id/arcgis/admin', 'siteadmin', 'siteadmin1234'])