import unittest
import re


class Submodule:
    """ This represents a submodule in a .gitmodules file """
    ALLOWED_PROPERTIES = ['branch', 'url']

    def __init__(self, name: str):
        self.name = Submodule.parse_name_line(name)

    def ingest(self, line: str):
        """ Eat a line and assign the value to the key in this class """
        (key, value) = self.parse_line(line)
        if key in self.ALLOWED_PROPERTIES:
            setattr(self, key, value)

    def parse_name_line(line: str) -> str:
        """ Parses [submodule "name"] and returns just 'name' """
        return line.split('"')[1]

    def parse_line(self, line: str) -> tuple[str, str]:
        split_items = re.split(r'\s*=\s*', line.strip(), 1)
        return (split_items[0], split_items[-1])


class TestSubmodule(unittest.TestCase):
    """ Tests for the submodule class """

    def test_parse_name_line(self):
        self.assertEqual(Submodule.parse_name_line(
            '[submodule "testing/testing"]'), 'testing/testing')

    def test_create_submodule(self):
        sm = Submodule('[submodule "testing/testing"]')
        self.assertEqual(sm.name, 'testing/testing')

        sm = Submodule('\t[submodule "testing/testing"]')
        self.assertEqual(sm.name, 'testing/testing')

    def test_parse_line(self):
        sm = Submodule('[submodule "test"]')
        self.assertEqual(sm.parse_line(
            '\turl = https://google.com'), ('url', 'https://google.com'))

    def test_ingest(self):
        sm = Submodule('[submodule "test"]')
        sm.ingest('\turl = https://example.com/')
        self.assertEqual(sm.url, 'https://example.com/')

        sm.ingest('\tbranch = main')
        self.assertEqual(sm.branch, 'main')
