#!/usr/bin/env python

import fftmatch as fft
import boyermoore as bm
import argparse
import collections
import cvmatch

parser = argparse.ArgumentParser(description='Search for a substring in a \
genome')

# Algorithm flag: Options= nlogn, nlogm, boyer moore; Default=nlogm
parser.add_argument('-a','--algorithm', choices=["nlogn", "nlogm", "boyermoore",
"opencv"],
                    default='nlogm', nargs='?', help='The algorithm that you \
want to run the search on. Default=nlogm')

# Pattern arg: substring to search genomes for.
parser.add_argument('pattern', help='The pattern that you want to search for in\
 the genome(s)')

# Genome arg: Genomes to search
parser.add_argument('genomes', nargs='+',
                    help='1 or more fastq files (.fa). \
You can also pass in 1 or more genomes, separated by spaces')

parser.add_argument('-b', type=int, nargs='?', help='b for \
nlogm', default=0)


args = parser.parse_args()
genomes = {}

if args.b == 0:
    args.b='m'

count = {}

# Scan files and store the title and genome string in genomes dictionary
for genome_fn in args.genomes:
    with open(genome_fn) as gn:
        title = gn.readline().rstrip()
        genome = ''
        for line in gn:
            genome += line.rstrip()

    if title in count:
        count[title] += 1
    else:
        count[title] = 1
    title = title + str(count[title])
    genomes[title] = genome

sorted_genomes = collections.OrderedDict(sorted(genomes.items(),
                                      key=lambda t: t[0]))
genome_strings = sorted_genomes.values()
genome_titles = sorted_genomes.keys()

# Parse args
if args.algorithm == 'nlogn':
    for gn in genomes:
        matches = fft.fft_match_index_n_log_n(genomes[gn], args.pattern)
        print gn, ': Found matches at indices', matches.tolist()
elif args.algorithm == 'nlogm':
    if len(genomes) > 1:
        matches = fft.fft_match_index_n_sq_log_m(genomes.values(),\
        args.pattern[0], args.b)
        print 'found matches at', matches.tolist()
    else:
        for gn in genomes:
            matches = fft.fft_match_index_n_log_m(genomes[gn], args.pattern[0],args.b)
            print gn, ': Found matches at indices', matches.tolist()
elif args.algorithm == 'boyermoore':
    for gn in genomes:
        matches = bm.boyer_moore_match_index(genomes[gn], args.pattern)
        print gn, ': Found matches at indices', matches.tolist()
elif args.algorithm == 'opencv':
    matches = cvmatch.cv_match_index_chunk(genomes.values(), args.pattern[0], args.b)
    print genomes[genomes.keys()[0]]
    print genomes.keys(), ': Found matches at indices', matches.tolist()
