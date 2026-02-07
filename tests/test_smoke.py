import importlib
import unittest
from pathlib import Path


class SmokeTests(unittest.TestCase):
    def test_entrypoints_exist(self):
        root = Path(__file__).resolve().parents[1]
        for name in ["main.py", "biocomputing_api_server.py", "hyper_nextus_server.py"]:
            self.assertTrue((root / name).is_file())

    def test_main_importable(self):
        mod = importlib.import_module("main")
        self.assertTrue(hasattr(mod, "main"))
