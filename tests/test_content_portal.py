import unittest
from click.testing import CliRunner
from arcgisenterprisemigration.cli import portal_content


class TestPortalContentDump(unittest.TestCase):
    def test_load_to_console(self):
        runner = CliRunner()
        result = runner.invoke(portal_content.load_cmd_portal_content, ['', '', ''])