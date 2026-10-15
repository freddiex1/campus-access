import unittest

import storage
import cli


class TestCli(unittest.TestCase):
    def setUp(self):
        storage.clear_requests()

    def test_invalid_option_then_retry(self):
        answers = iter(["12", "abc", "9", "n"])
        outputs = []
        cli.run_menu(
            input_func=lambda prompt: next(answers),
            output_func=outputs.append,
        )
        self.assertTrue(any("Invalid option '12'" in line for line in outputs))
        self.assertTrue(any("Invalid option 'abc'" in line for line in outputs))
        self.assertTrue(any("Goodbye" in line for line in outputs))


if __name__ == "__main__":
    unittest.main()