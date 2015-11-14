'''
Unit Tests for fftmatch.naive_string_match_index
'''
import unittest
import fftmatch
import numpy as np

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
        func = fftmatch.naive_string_match_index
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pattern = "#"
        self.assertTrue(len(func(text=text,pattern=pattern))==0)

    def test_multi_char_no_occurrence(self):
        func = fftmatch.naive_string_match_index
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pattern = "CE"
        self.assertTrue(len(func(text=text,pattern=pattern))==0)

    def test_multi_char_multiple_occurrence(self):
        func = fftmatch.naive_string_match_index

        text = "AAABBACDDCDCBAADA"
        patterns = [text[i:i+3] for i in range(len(text)-3+1)]

        for index, pattern in enumerate(patterns):
            self.assertTrue(func(text=text,pattern=pattern)==[index])

    def test_multi_genome_search(self):
        func = fftmatch.fft_match_index_n_sq_log_n
        texts = ["ABCDABCDABCDABCD"]*4
        pattern = "ABCD"

        expected_output = np.array([[0,4,8,12]]*4)

        self.assertTrue((func(texts, pattern) == expected_output).all())

if __name__ == '__main__':
    unittest.main()
