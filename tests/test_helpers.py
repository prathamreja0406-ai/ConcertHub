import tempfile
import unittest
from pathlib import Path

import app.database as database


class ConcertHubTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.original_db_path = database.DB_PATH
        self.original_data_dir = database.DATA_DIR

        database.DATA_DIR = Path(self.temp_dir.name)
        database.DB_PATH = Path(self.temp_dir.name) / "test_concert_hub.db"

        database.initialize_database()

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        database.DATA_DIR = self.original_data_dir

        self.temp_dir.cleanup()
