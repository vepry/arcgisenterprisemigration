import unittest
from click.testing import CliRunner
from arcgisenterprisemigration.cli import users_roles



class TestUserDumpToConsole(unittest.TestCase):
    def test_load_to_console(self):
        runner = CliRunner()
        result = runner.invoke(users_roles.load_cmd_users_roles, ['https://peta.gakkum.menlhk.go.id/portal', 'portaladmin', 'Passw0rd1234'])
        # assert '' in ''