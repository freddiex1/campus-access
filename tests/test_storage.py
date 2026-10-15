import json
import os
import tempfile
import unittest

import storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        storage.clear_requests()

    def test_valid_creation(self):
        record = storage.create_request("F001", "visitor")
        self.assertEqual(record, {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "visitor",
            "status": "requested",
            "approved_by": None,
        })

    def test_invalid_card_type(self):
        with self.assertRaises(ValueError):
            storage.create_request("F001", "alien")
        self.assertEqual(storage.list_requests(), [])

    def test_unique_id_after_reload(self):
        storage.create_request("F001", "visitor")
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "data.json")
            storage.save_requests(path)
            storage.clear_requests()
            storage.load_requests(path)
            record = storage.create_request("F002", "staff")
        self.assertEqual(record["id"], "A002")

    def test_corrupt_file_keeps_existing_data(self):
        storage.create_request("F001", "visitor")
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "bad.json")
            with open(path, "w") as f:
                f.write("{ not json")
            with self.assertRaises(ValueError):
                storage.load_requests(path)
        self.assertEqual(len(storage.list_requests()), 1)


if __name__ == "__main__":
    unittest.main()