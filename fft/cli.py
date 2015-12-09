#!/usr/bin/env python

import fftmatch as fft
import boyermoore as bm
import argparse

parser = argparse.ArgumentParser(description='Search for a substring in a \
genome')

# Algorithm flag: Options= nlogn, nlogm, boyer moore; Default=nlogm
parser.add_argument('-a','--algorithm', choices=["nlogn", "nlogm", "boyermoore"],
                    default='nlogm', nargs='?', help='The algorithm that you \
want to run the search on. Default=nlogm')

# Pattern arg: substring to search genomes for.
parser.add_argument('pattern', help='The pattern that you want to search for in\
 the genome(s)', nargs=1)

# Genome arg: Genomes to search
parser.add_argument('genomes', nargs='+',
                    help='1 or more fastq files (.fa). \
You can also pass in 1 or more genomes, separated by spaces')

args = parser.parse_args()
genomes = {}

# Scan files and store the title and genome string in genomes dictionary
for genome_fn in args.genomes:
    with open(genome_fn) as gn:
        title = gn.readline().rstrip()
        genome = ''
        for line in gn:
            genome += line.rstrip()
    genomes[title] = genome

# Parse args
if args.algorithm == 'nlogn':
    for gn in genomes:
        matches = fft.fft_match_index_n_log_n(genomes[gn], args.pattern[0])
        print gn, ': Found matches at indices', matches.tolist()
    pass
elif args.algorithm == 'nlogm':
    for gn in genomes:
        matches = fft.fft_match_index_n_log_m(genomes[gn], args.pattern[0])
        print gn, ': Found matches at indices', matches.tolist()
    pass
elif args.algorithm == 'boyermoore':
    for gn in genomes:
        matches = bm.boyer_moore_match_index(genomes[gn], args.pattern[0])
        print gn, ': Found matches at indices', matches.tolist()
    pass
