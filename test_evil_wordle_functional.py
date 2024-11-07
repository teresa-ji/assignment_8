import unittest
from unittest.mock import patch
import sys
import io
import os
import difflib
import evil_wordle


class TestWordle(unittest.TestCase):

    def check_diff(self, actual_output, output_file):
        """Helper function to check differences between actual output and the expected file content"""

        with open(
            os.path.join("expected_default_outputs", output_file), "r", encoding="UTF-8"
        ) as outfile:
            expected_default_output = outfile.read()

        with open(
            os.path.join("expected_high_contrast_outputs", output_file),
            "r",
            encoding="UTF-8",
        ) as outfile:
            expected_high_contrast_output = outfile.read()

        default_diff = list(
            difflib.unified_diff(
                expected_default_output.splitlines(keepends=True),
                actual_output.splitlines(keepends=True),
                fromfile="expected output",
                tofile="actual output",
                lineterm="",
            )
        )

        high_contrast_diff = list(
            difflib.unified_diff(
                expected_high_contrast_output.splitlines(keepends=True),
                actual_output.splitlines(keepends=True),
                fromfile="expected output",
                tofile="actual output",
                lineterm="",
            )
        )

        if len(default_diff) <= len(high_contrast_diff):
            diff_result = default_diff
        else:
            diff_result = high_contrast_diff

        if diff_result:
            diff_output = "\n".join(diff_result)
            self.fail(
                f"Differences found between actual output and {output_file}:\n{diff_output}"
            )

    def run_wordle_with_input(self, input_file):
        """Helper function to run wordle.py with input from a file, and capture output as a string"""
        with open(input_file, "r") as infile:
            inputs = infile.read().splitlines()
        i = 0

        # Function to mock each input call
        def input_mock(prompt=""):
            nonlocal i
            # Print or log each input as it's read from the file
            if i < len(inputs):
                current_input = inputs[i]
                print(f"{prompt}{current_input}")
                i += 1
                return current_input
            raise EOFError("EOF when reading a line")

        output_buffer = io.StringIO()
        with patch("builtins.input", input_mock), patch(
            "sys.stdout", new=output_buffer
        ):
            sys.argv = ["evil_wordle.py"]
            evil_wordle.main()

        return output_buffer.getvalue()

    def run_test_case(self, test_case):
        """Helper function to handle test case execution and diff checking"""
        input_file = f"{test_case}.in"
        output_file = f"{test_case}.ansi"

        actual_output = self.run_wordle_with_input(input_file)
        self.check_diff(actual_output, output_file)

    def test_banns(self):
        """python3 evil_wordle.py < banns.in"""
        self.run_test_case("banns")

    def test_boozy(self):
        """python3 evil_wordle.py < boozy.in"""
        self.run_test_case("boozy")

    def test_judge(self):
        """python3 evil_wordle.py < judge.in"""
        self.run_test_case("judge")

    def test_kakas(self):
        """python3 evil_wordle.py < kakas.in"""
        self.run_test_case("kakas")

    def test_kooks(self):
        """python3 evil_wordle.py < kooks.in"""
        self.run_test_case("kooks")

    def test_pared(self):
        """python3 evil_wordle.py < pared.in"""
        self.run_test_case("pared")

    def test_sages(self):
        """python3 evil_wordle.py < sages.in"""
        self.run_test_case("sages")

    def test_sixes(self):
        """python3 evil_wordle.py < sixes.in"""
        self.run_test_case("sixes")

    def test_wides(self):
        """python3 evil_wordle.py < wides.in"""
        self.run_test_case("wides")

    def test_woozy(self):
        """python3 evil_wordle.py < woozy.in"""
        self.run_test_case("woozy")


def main():
    if len(sys.argv) > 1:
        test_name = "_".join(sys.argv[1:])
        # Check if the provided test name is valid
        valid_tests = [
            "banns",
            "boozy",
            "judge",
            "kakas",
            "kooks",
            "pared",
            "sages",
            "sixes",
            "wides",
            "woozy",
        ]

        if test_name in valid_tests:
            loader = unittest.TestLoader()
            all_tests = loader.loadTestsFromTestCase(TestWordle)
            suite = unittest.TestSuite()

            for test in all_tests:
                if test_name == test.id().split(".")[-1][5:]:
                    suite.addTest(test)
                    break
            else:
                print(
                    f"Invalid test name: {test_name}. Please choose from {valid_tests}."
                )
            runner = unittest.TextTestRunner()
            runner.run(suite)
        else:
            print(f"Invalid test name: {test_name}. Please choose from {valid_tests}.")
    else:
        # If no argument is passed, run all tests
        unittest.main()


if __name__ == "__main__":
    main()
