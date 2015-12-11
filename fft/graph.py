import matplotlib.pyplot as pyplot
import yaml
import argparse

def plot_chunk_time(data):
    boyer_moore = []
    nlogm = {}
    for d in data:
        for alg in d['algorithms']:
            if alg['name'] == 'nlogm':
                chunk_size = alg['chunk_size']
                nlogm[chunk_size] = alg['time']
            else:
                boyer_moore.append(alg['time'])

    chunk_size = []
    nlogm_time = []
    for k,v in nlogm.items():
        chunk_size.append(k)
        nlogm_time.append(v)

    pyplot.xlabel('Chunk Size')
    pyplot.ylabel('Time/msecs')
    pyplot.plot(chunk_size, boyer_moore, label='boyer moore')
    pyplot.plot(chunk_size, nlogm_time, 'ro', label='nlogm')
    pyplot.legend(loc='upper right')
    pyplot.title('Performance time of nlogm vs Length of m')
    pyplot.show()

def plot_alg_time(data):
    text_length = []
    accuracy = {}
    time = {}

    for d in data:
        # first, graph accuracy vs text length for each algorithm
        text_length.append(d['text_length'])
        for alg in d['algorithms']:
            if alg['name'] not in accuracy:
                accuracy[alg['name']] = []
            accuracy[alg['name']].append(alg['accuracy'])
            if alg['name'] not in time:
                time[alg['name']] = []
            time[alg['name']].append(alg['time'])

    pyplot.xlabel('Text Length')
    pyplot.ylabel('Time/msecs')
    pyplot.plot(text_length, time['boyermoore'], label='boyer moore')
    pyplot.plot(text_length, time['nlogn'], label='nlogn')
    pyplot.plot(text_length, time['nlogm'],  label='nlogm',)
    pyplot.title('Time Performance of Algorithms vs Text Length')

    pyplot.legend(loc='upper left')
    pyplot.show()

parser = argparse.ArgumentParser(description='Graph values from analysis.')
parser.add_argument('-c','--chunk', action='store_true',
                    help='Graph by chunk size on the nlogm algorithm.')
parser.add_argument('data', help='The file to load data from.')


args = parser.parse_args()

data = []
with open(args.data) as dn:
    title = dn.readline()
    execution = dn.readline()
    for line in dn:
        data.append(yaml.load(line.rstrip()))

if args.chunk:
    plot_chunk_time(data)
else:
    plot_alg_time(data)
