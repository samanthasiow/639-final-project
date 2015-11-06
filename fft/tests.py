'''
Unit Tests for fftmatch.naive_string_match_index
'''
import unittest
import fftmatch

class FFTStringMatchTestRig(unittest.TestCase):
    def test_single_char_single_occurrence(self):
        func = fftmatch.naive_string_match_index

        text = "ABCD"
        patterns = ["A", "B", "C", "D"]
        expected_outputs = [[0], [1], [2], [3]]

        for pattern, expected_output in zip(patterns, expected_outputs):
            output = expected_output
            self.assertTrue(func(text=text,pattern=pattern) == output)

    def test_single_char_multiple_occurrences(self):
        func = fftmatch.naive_string_match_index

        text = "ABCDABCDABCD"
        patterns = ["A", "B", "C", "D"]
        expected_outputs = [[0,4,8], [1,5,9], [2,6,10], [3,7,11]]

        for pattern, expected_output in zip(patterns, expected_outputs):
            output = expected_output
            self.assertTrue(func(text=text,pattern=pattern) == output)

    def test_multi_char_single_occurrence(self):
        func = fftmatch.naive_string_match_index

        text = "ABCD"
        patterns = ["AB", "BC", "CD"]
        expected_outputs = [[0], [1], [2]]

        for pattern, expected_output in zip(patterns, expected_outputs):
            output = expected_output
            self.assertTrue(func(text=text,pattern=pattern) == output)

    def test_single_char_no_occurrence(self):
        self.assertTrue(False)

    def test_multi_char_no_occurrence(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()