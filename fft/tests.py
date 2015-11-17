'''
Unit Tests for fftmatch.naive_string_match_index
'''
import unittest
import fftmatch
import numpy as np
import functools
import boyermoore

def string_match_decorator(string_matching_algorithms):
    def inner_decorator(function):
        @functools.wraps(function)
        def inner_function(self):
            '''Class method to run string matching algorithms'''
            for sma in string_matching_algorithms:
                function(self, sma)
        return inner_function
    return inner_decorator

#algorithms that match a single genome to a single substring
oned_string_matching_algorithms = [fftmatch.naive_string_match_index,
                              fftmatch.fft_match_index_n_log_n,
                              fftmatch.fft_match_index_n_log_m,
                              boyermoore.boyer_moore_match_index]

#algorithms that match multiple genomes to a single substring
twod_string_matching_algorithms = [fftmatch.fft_match_index_n_sq_log_n,
                                   fftmatch.fft_match_index_n_sq_log_m]
class FFTStringMatchTestRig(unittest.TestCase):
    @string_match_decorator(oned_string_matching_algorithms)
    def test_single_char_single_occurrence(self, func):
        text = "AGCT"
        patterns = ["A", "G", "C", "T"]
        expected_outputs = [[0], [1], [2], [3]]

        for pattern, expected_output in zip(patterns, expected_outputs):
            output = expected_output
            #self.assertTrue((func(text=text,pattern=pattern) == output).all())

    @string_match_decorator(oned_string_matching_algorithms)
    def test_single_char_multiple_occurrences(self, func):
        text = "AGTC" * 3
        patterns = ["A", "G", "T", "C"]
        expected_outputs = [[0,4,8], [1,5,9], [2,6,10], [3,7,11]]

        for pattern, expected_output in zip(patterns, expected_outputs):
            output = np.array(expected_output)
            self.assertTrue((func(text=text,pattern=pattern) == output).all())

    @string_match_decorator(oned_string_matching_algorithms)
    def test_multi_char_single_occurrence(self, func):
        text = "AGTC"
        patterns = ["AG", "GT", "TC"]
        expected_outputs = [[0], [1], [2]]

        for pattern, expected_output in zip(patterns, expected_outputs):
            output = expected_output
            self.assertTrue(func(text=text,pattern=pattern) == output)

    @string_match_decorator(oned_string_matching_algorithms)
    def test_single_char_no_occurrence(self, func):
        text = "AGTAGTTATATGGGATATAT"
        pattern = "C"
        self.assertTrue(len(func(text=text,pattern=pattern))==0)

    @string_match_decorator(oned_string_matching_algorithms)
    def test_multi_char_no_occurrence(self, func):
        text = "AGATATAATTATATACCATATTACCACACA"
        pattern = "CG"
        self.assertTrue(len(func(text=text,pattern=pattern))==0)

    @string_match_decorator(oned_string_matching_algorithms)
    def test_multi_char_single_occurrence(self, func):
        text = "AGCTACCGCATTAGG"
        patterns = [text[i:i+3] for i in range(len(text)-3+1)]

        for index, pattern in enumerate(patterns):
            self.assertTrue(
                (func(text=text,pattern=pattern)==np.array([index])).all()
            )

    @string_match_decorator(oned_string_matching_algorithms)
    def test_multi_char_multiple_occurrence(self, func):
        text = "AGCTAACCCACGGTCAA"
        patterns = [text[i:i+3] for i in range(len(text)-3+1)]
        half_len = len(text)
        text *= 2

        for index, pattern in enumerate(patterns):
            self.assertTrue(
                (func(text=text,pattern=pattern) == \
                    np.array([index,index+half_len])).all()
            )

class MultiGenomeTestRig(unittest.TestCase):
    @string_match_decorator(twod_string_matching_algorithms)
    def test_multi_genome_search(self, func):
        texts = ["ABCDABCDABCDABCD"]*4
        pattern = "ABCD"

        expected_output = np.array([[0,4,8,12]]*4)

        self.assertTrue((func(texts, pattern) == expected_output).all())

    @string_match_decorator(twod_string_matching_algorithms)
    def test_multi_genome_search_different_patterns(self, func):
        texts = ["ABCDABCDABCDABCD"]*4
        patterns = "ABCD", "BCD", "CD", "DAB"

        expected_outputs = [np.array([[0,4,8,12]]*4),
                           np.array([[1,5,9,13]]*4),
                           np.array([[2,6,10,14]]*4),
                           np.array([[3,7,11]]*4)]

        for i in range(len(patterns)):
            self.assertTrue((func(texts, patterns[i]) == expected_outputs[i]).all())


if __name__ == '__main__':
    unittest.main()
