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
        
        genome = ''
        for line in gn:
            genome += line.rstrip()
    genomes[genome_fn] = genome

sorted_genomes = collections.OrderedDict(sorted(genomes.items(),
                                      key=lambda t: t[0]))
genome_strings = sorted_genomes.values()
genome_titles = sorted_genomes.keys()

for k,gn in genomes.items():
    # analysis dictionary holds all data about the algorithms
    analysis = {'substring_length':len(args.pattern), 'substring': args.pattern, 'text_length': len(gn)}

    # Get time to run algorithm on all substrings
    boyermoore_data = {'name': 'boyermoore'}
    nlogn_data = {'name': 'nlogn'}
    nlogm_data = {'name': 'nlogm'}

    with Timer() as t:
        bm_matches = bm.boyer_moore_match_index(gn, args.pattern)
    boyermoore_data['time'] = t.msecs
    boyermoore_data['accuracy'] = 1
    num_matches = len(bm_matches)

    with Timer() as t:
        nlogn_matches = fft.fft_match_index_n_log_n(gn, args.pattern)
    nlogn_data['time'] = t.msecs
    nlogn_data['accuracy'] = len(nlogn_matches) / num_matches
    print len(nlogn_matches) / num_matches

    with Timer() as t:
        nlogm_matches = fft.fft_match_index_n_log_m(gn, args.pattern)
    nlogm_data['time'] = t.msecs
    nlogm_data['accuracy'] = len(nlogm_matches) / num_matches

    algorithms = []
    algorithms.append(boyermoore_data)
    algorithms.append(nlogn_data)
    algorithms.append(nlogm_data)

    analysis['algorithms'] = algorithms
    # make pretty json format
    print json.dumps(analysis)
