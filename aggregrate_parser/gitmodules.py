from .submodule import Submodule
from pathlib import Path
import unittest


class InvalidGitmodulesFile(Exception):
    pass


class GitmodulesFile:
    def __init__(self, file: Path):
        if file.exists():
            with open(file) as f:
                lines = f.readlines()

        self.submodules = GitmodulesFile.parse_submodules(lines)

    def parse_submodules(lines: [str]) -> list[Submodule]:
        submodule = None
        for l in lines:
            line = l.strip()
            submodules = []

            # If we are on a '[submodule]' block, create a new Submodule class
            if line.startswith('['):
                # if this is not the first submodule we need to add the
                # previous one to the final list, and then create a fresh one
                if submodule is not None:
                    submodules.append(submodule)

                submodule = Submodule(l)

            # if we are not on a '[submodule]' block pass it to the existing
            # submodule
            else:

                # Oops, we didn't see a submodule block, so the file is not
                # valid
                if submodule is None:
                    err = "Error parsing gitmodules file: I couldn't find a " \
                        "starting [submodule] block"
                    raise InvalidGitmodulesFile(err)
                # Parse and assign the value to the submodule
                submodule.ingest(l)
        submodules.append(submodule)
        return submodules


class TestGitmodulesFile(unittest.TestCase):
    def test_parse_submodules(self):
        s = ['[submodule "test"]', 'url = https://google.com']
        sm = GitmodulesFile.parse_submodules(s)[0]
        self.assertEqual(sm.name, 'test')
        self.assertEqual(sm.url, 'https://google.com')
