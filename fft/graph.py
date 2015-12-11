import matplotlib.pyplot as pyplot
import yaml
import argparse

def plot_chunk_time(data, alg_name):
    boyer_moore = []
    alg = {}
    for d in data:
        for a in d['algorithms']:
            if a['name'] == alg_name:
                chunk_size = a['chunk_size']
                alg[chunk_size] = a['time']
            else:
                boyer_moore.append(a['time'])

    chunk_size = []
    alg_time = []
    for k,v in alg.items():
        chunk_size.append(k)
        alg_time.append(v)

    pyplot.xlabel('Chunk Size')
    pyplot.ylabel('Time/msecs')
    # print 'CS:', chunk_size
    # print 'BM:', boyer_moore
    # print 'AT:', alg_time
    pyplot.plot(chunk_size, boyer_moore, label='Boyer Moore')

    if alg_name == "nlogm":
        pyplot.plot(chunk_size, alg_time, 'ro', label='n^2 log m')
    else:
        pyplot.plot(chunk_size, alg_time, 'ro', label='OpenCV')
    pyplot.legend(loc='upper right')
    pyplot.title('Performance time of nlogm vs Length of \'chunks\'')
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
    pyplot.plot(text_length, time['opencv'], label='opencv')
    pyplot.plot(text_length, time['nlogn'], label='n^2 logn')
    pyplot.plot(text_length, time['nlogm'],  label='n^2 logm',)
    pyplot.title('Time Performance of Algorithms vs Text Length')

    pyplot.legend(loc='upper left')
    pyplot.show()

parser = argparse.ArgumentParser(description='Graph values from analysis.')
parser.add_argument('-c','--chunk', nargs=1, choices=['nlogm', 'opencv'],
                    help='Graph by chunk size on an algorithm.')
parser.add_argument('data', help='The file to load data from.')


args = parser.parse_args()

data = []
with open(args.data) as dn:
    title = dn.readline()
    execution = dn.readline()
    for line in dn:
        data.append(yaml.load(line.rstrip()))

if args.chunk:
    plot_chunk_time(data, args.chunk[0])
else:
    plot_alg_time(data)
