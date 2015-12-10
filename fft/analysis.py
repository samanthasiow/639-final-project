#!/usr/bin/env python
import fftmatch as fft
import boyermoore as bm
import argparse
import collections
from timer import Timer
import json

parser = argparse.ArgumentParser(description='Search for a substring in a \
genome')

# Pattern arg: substring to search genomes for.
parser.add_argument('pattern', help='The pattern that you want to search for in\
 the genome(s)')

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

sorted_genomes = collections.OrderedDict(sorted(genomes.items(),
                                      key=lambda t: t[0]))
genome_strings = sorted_genomes.values()
genome_titles = sorted_genomes.keys()

# analysis dictionary holds all data about the algorithms
analysis = {'substring_length':len(args.pattern), 'substring': args.pattern}
text_length = 0

# Get time to run algorithm on all substrings
boyermoore_data = {'name': 'boyermoore'}
nlogn_data = {'name': 'nlogn'}
nlogm_data = {'name': 'nlogm'}

# all accuracy is compared against boyer moore
total_matches = []
with Timer() as t:
    for gn in genomes:
        matches = bm.boyer_moore_match_index(genomes[gn], args.pattern)
        total_matches.append(len(matches))
        text_length += len(gn)
boyermoore_data['time'] = t.msecs
analysis['text_length'] = text_length
boyermoore_data['accuracy'] = 100

# nlogn calculations
nlogn_matches = []
with Timer() as t:
    for gn in genomes:
        matches = fft.fft_match_index_n_log_n(genomes[gn], args.pattern)
        nlogn_matches.append(len(matches))
nlogn_data['time'] = t.msecs

# nlogn accuracy calculation
for i in range(len(total_matches)):
    nlogn_matches[i] = nlogn_matches[i] / total_matches[i]
nlogn_data['accuracy'] = reduce(lambda x, y: x + y, nlogn_matches) * 100 / len(nlogn_matches)

# nlogm calculations
nlogm_matches = []
with Timer() as t:
    for gn in genomes:
        matches = fft.fft_match_index_n_log_m(genomes[gn], args.pattern)
        nlogm_matches.append(len(matches))
nlogm_data['time'] = t.msecs

# nlogm accuracy calculations
for i in range(len(total_matches)):
    nlogm_matches[i] = nlogm_matches[i] / total_matches[i]
nlogm_data['accuracy'] = reduce(lambda x, y: x + y, nlogm_matches) * 100 / len(nlogm_matches)

algorithms = []
algorithms.append(boyermoore_data)
algorithms.append(nlogn_data)
algorithms.append(nlogm_data)

analysis['algorithms'] = algorithms

# make pretty json format
print json.dumps(analysis)
