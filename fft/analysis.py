#!/usr/bin/env python
import fftmatch as fft
import boyermoore as bm
import argparse
import collections
from timer import Timer
import json
import cvmatch

def nlogm_chunk_analysis(genomes, chunk_max, total_length):
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

def opencv_chunk_analysis(genomes, chunk_max, total_length):
    # analysis dictionary holds all data about the algorithms
    analysis = {'substring_length':len(args.pattern), 'substring': args.pattern,
                'text_length':total_length}

    # Get time to run algorithm on all substrings
    boyermoore_data = {'name': 'boyermoore'}
    opencv_data = {'name': 'opencv'}

    with Timer() as t:
        bm_matches = bm.boyer_moore_mult_match_index(genomes, args.pattern)
    boyermoore_data['time'] = t.msecs
    boyermoore_data['accuracy'] = 1

    for i in range(3,chunk_max,3):
        with Timer() as t:
            opencv_matches = cvmatch.cv_match_index_chunk(genomes, args.pattern, chunk_size=i)
        opencv_data['time'] = t.msecs
        opencv_data['chunk_size'] = i

        accuracy = 0
        for i in range(len(opencv_matches)):
            i_accuracy = len(opencv_matches[i]) / len(bm_matches[i])
            accuracy += i_accuracy
        opencv_data['accuracy'] = accuracy / len(bm_matches)

        algorithms = []
        algorithms.append(boyermoore_data)
        algorithms.append(opencv_data)

        analysis['algorithms'] = algorithms
        # make pretty json format
        print json.dumps(analysis)

def k_analysis(genomes):
    # analysis dictionary holds all data about the algorithms
    analysis = {'substring_length':len(args.pattern), 'substring': args.pattern}

    # Get time to run algorithm on all substrings
    boyermoore_data = {'name': 'boyermoore'}
    nlogn_data = {'name': 'nlogn'}
    opencv_data = {'name': 'opencv'}
    for i in range(0,len(genomes)):
        analysis['k'] = i
        if len(genomes[:i]) == 0:
            k_genomes = [genomes[0]]
        else:
            k_genomes = genomes[:i]
        with Timer() as t:
            bm_matches = bm.boyer_moore_mult_match_index(k_genomes, args.pattern)
        boyermoore_data['time'] = t.msecs
        boyermoore_data['accuracy'] = 1

        with Timer() as t:
            nlogn_matches = fft.fft_match_index_2d(k_genomes, args.pattern)
        nlogn_data['time'] = t.msecs
        accuracy = 0

        for i in range(len(nlogn_matches)):
            i_accuracy = len(nlogn_matches[i]) / len(bm_matches[i])
            accuracy += i_accuracy
        nlogn_data['accuracy'] = accuracy / len(bm_matches)

        with Timer() as t:
            cvmatch.cv_match_index(k_genomes, args.pattern)
        opencv_data['time'] = t.msecs

        algorithms = []
        algorithms.append(boyermoore_data)
        algorithms.append(nlogn_data)
        algorithms.append(opencv_data)

        analysis['algorithms'] = algorithms
        # make pretty json format
        print json.dumps(analysis)

def time_analysis(genomes, total_length):
    # analysis dictionary holds all data about the algorithms
    analysis = {'substring_length':len(args.pattern), 'substring': args.pattern,
                'text_length':total_length}

    # Get time to run algorithm on all substrings
    boyermoore_data = {'name': 'boyermoore'}
    nlogn_data = {'name': 'nlogn'}
    nlogm_data = {'name': 'nlogm'}
    opencv_data = {'name': 'opencv'}

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

    with Timer() as t:
        cvmatch.cv_match_index(genomes, args.pattern)
    opencv_data['time'] = t.msecs

    accuracy = 0
    for i in range(len(nlogm_matches)):
        i_accuracy = len(nlogm_matches[i]) / len(bm_matches[i])
        accuracy += i_accuracy
    opencv_data['accuracy'] = accuracy / len(bm_matches)

    algorithms = []
    algorithms.append(boyermoore_data)
    algorithms.append(nlogn_data)
    algorithms.append(nlogm_data)
    algorithms.append(opencv_data)

    analysis['algorithms'] = algorithms
    # make pretty json format
    print json.dumps(analysis)

parser = argparse.ArgumentParser(description='Get time data on algorithms.')

# Pattern arg: substring to search genomes for.
parser.add_argument('-c','--chunk',nargs='?', type=int,
                    help='Analyze by chunk size an algorithm.')
# Pattern arg: substring to search genomes for.
parser.add_argument('-v','--opencv', action="store_true",
                    help='Analyze by chunk size on the opencv algorithm.')
# Pattern arg: substring to search genomes for.
parser.add_argument('-k','--genenum', action="store_true",
                    help='Analyze by number of texts the algorithms.')

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
        title = gn.readline()
        genome = ''
        for line in gn:
            genome += line.rstrip()
            total_length += len(genome)
    genomes.append(genome)

if args.genenum:
    k_analysis(genomes)
elif args.chunk:
    if args.opencv:
        opencv_chunk_analysis(genomes,args.chunk, total_length)
    else:
        nlogm_chunk_analysis(genomes, args.chunk, total_length)
else:
    time_analysis(genomes,total_length)
