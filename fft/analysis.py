#!/usr/bin/env python
import fftmatch as fft
import boyermoore as bm
import argparse
import collections
from timer import Timer
import json

def chunk_analysis(genomes, chunk_max):
    # analysis dictionary holds all data about the algorithms
    analysis = {'substring_length':len(args.pattern), 'substring': args.pattern,
                'text_length':total_length}

    # Get time to run algorithm on all substrings
    boyermoore_data = {'name': 'boyermoore'}
    nlogm_data = {'name': 'nlogm'}

    with Timer() as t:
        bm_matches = bm.boyer_moore_mult_match_index(genomes, args.pattern)
    boyermoore_data['time'] = t.msecs
    boyermoore_data['accuracy'] = 1

    for i in range(3,chunk_max,3):
        nlogm_matches = []
        with Timer() as t:
            for g in genomes:
                nlogm_matches.append(fft.fft_match_index_n_log_m(g, args.pattern, chunk_size=i))
        nlogm_data['time'] = t.msecs
        nlogm_data['chunk_size'] = i

        accuracy = 0
        for i in range(len(nlogm_matches)):
            i_accuracy = len(nlogm_matches[i]) / len(bm_matches[i])
            accuracy += i_accuracy
        nlogm_data['accuracy'] = accuracy / len(bm_matches)

        algorithms = []
        algorithms.append(boyermoore_data)
        algorithms.append(nlogm_data)

        analysis['algorithms'] = algorithms
        # make pretty json format
        print json.dumps(analysis)


def time_analysis(genomes):
    # analysis dictionary holds all data about the algorithms
    analysis = {'substring_length':len(args.pattern), 'substring': args.pattern,
                'text_length':total_length}

    # Get time to run algorithm on all substrings
    boyermoore_data = {'name': 'boyermoore'}
    nlogn_data = {'name': 'nlogn'}
    nlogm_data = {'name': 'nlogm'}

    with Timer() as t:
        bm_matches = bm.boyer_moore_mult_match_index(genomes, args.pattern)
    boyermoore_data['time'] = t.msecs
    boyermoore_data['accuracy'] = 1

    with Timer() as t:
        nlogn_matches = fft.fft_match_index_2d(genomes, args.pattern)
    nlogn_data['time'] = t.msecs
    accuracy = 0

    for i in range(len(nlogn_matches)):
        i_accuracy = len(nlogn_matches[i]) / len(bm_matches[i])
        accuracy += i_accuracy
    nlogn_data['accuracy'] = accuracy / len(bm_matches)

    nlogm_matches = []
    with Timer() as t:
        for g in genomes:
            nlogm_matches.append(fft.fft_match_index_n_log_m(g, args.pattern, chunk_size=300))
    nlogm_data['time'] = t.msecs

    accuracy = 0
    for i in range(len(nlogm_matches)):
        i_accuracy = len(nlogm_matches[i]) / len(bm_matches[i])
        accuracy += i_accuracy
    nlogm_data['accuracy'] = accuracy / len(bm_matches)

    algorithms = []
    algorithms.append(boyermoore_data)
    algorithms.append(nlogn_data)
    algorithms.append(nlogm_data)

    analysis['algorithms'] = algorithms
    # make pretty json format
    print json.dumps(analysis)

parser = argparse.ArgumentParser(description='Get time data on algorithms.')

# Pattern arg: substring to search genomes for.
parser.add_argument('-c','--chunk',nargs='?', type=int,
                    help='Analyze by chunk size on the nlogm algorithm.')

parser.add_argument('pattern', help='The pattern that you want to search for in\
 the genome(s)')

# Genome arg: Genomes to search
parser.add_argument('genomes', nargs='+',
                    help='1 or more fastq files (.fa). \
You can also pass in 1 or more genomes, separated by spaces')

args = parser.parse_args()
genomes = []
total_length = 0

# Scan files and store the title and genome string in genomes dictionary
for genome_fn in args.genomes:
    with open(genome_fn) as gn:
        # title = gn.readline()
        genome = ''
        for line in gn:
            genome += line.rstrip()
            total_length += len(genome)
    genomes.append(genome)

if args.chunk:
    chunk_analysis(genomes, args.chunk)
else:
    time_analysis(genomes)
