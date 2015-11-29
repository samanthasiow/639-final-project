import fftmatch
import boyermoore
import argparse

parser = argparse.ArgumentParser(description='Search for a substring in a \
genome')

parser.add_argument('genomes', nargs='+', 
                    help='1 or more fastq files (.fa). \
You can also pass in 1 or more genomes, separated by spaces')
parser.add_argument('pattern', help='The pattern that you want to search for in\
 the genome(s)')

parser.add_argument('algorithm', choices=["nlogn", "nlogm", "boyermoore"])

args = parser.parse_args()

genomes = parser.genomes

if args.algorithm == 'nlogn':
    #stuff
    pass
