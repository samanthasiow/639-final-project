# 639-final-project
EN 600.639: Final Project with Samantha Siow, Michael Norris, Aaron Lerner, and Isac Lee

Dependencies
------------
* numpy `pip install numpy`
* opencv (on mac, `brew tap homebrew/science` then `brew install opencv`)
* swig (on mac, `brew install swig`)

How to run
----------

Our code is in the fft directory

    $ python cli.py

#algorithms that match a single genome to a single substring

    fftmatch.naive_string_match_index(text, pattern)
    fftmatch.fft_match_index_n_log_n(text, pattern)
Naive 1-D FFT-based match-index algorithm

  fftmatch.fft_match_index_n_log_m(text, pattern)
Most efficient 1-D FFT-based FFT-based match-index algorithm

    boyermoore.boyer_moore_match_index(text, pattern)
Used to benchmark all of our algorithms with

#algorithms that match multiple genomes to a single substring

    fftmatch.fft_match_index_n_sq_log_n(texts, pattern)
Similar to the n log n 1-D algorithm

    fftmatch.fft_match_index_n_sq_log_n\_naive(texts, pattern)
This uses the 1-D algorithm on each text individually from a list of texts.

    fftmatch.fft_match_index_n_sq_log_m(texts, pattern)

This breaks up the text into smaller chunks of size 2\*len(pattern) and does a
2-D FFT on the text.

    cvmatch.cv_match_index(texts, pattern)

This uses openCV's template-matching algorithm to solve the match index problem

    cvmatch.cv_match_index_chunk(texts, pattern)
This uses openCV's template-matching algorithm on size 2\*len(pattern) chunks

# Benchmarking
Run with:

    sh run_analysis.sh

Writes results to the results folder. 
Performs analysis on the time performance
of the algorithms according to text length, as well as the time performance of
the nlogm algorithm by the chunk size.
