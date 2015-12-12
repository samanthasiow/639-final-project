import matplotlib.pyplot as pyplot
import yaml
import argparse

def plot_chunk_time(data, alg_name):
    boyer_moore = []
    alg = {}
    for d in data:
        text_length = d['text_length']
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
    pyplot.plot(chunk_size, boyer_moore, label='Boyer Moore')

    chunk_size, alg_time = (list(t) for t in zip(*sorted(zip(chunk_size,alg_time))))

    if alg_name == "nlogm":
        pyplot.plot(chunk_size, alg_time, label='nk logm')
        title = 'Performance time of nk logm vs Length of \'chunks\' on text of length ' + str(text_length)
    else:
        pyplot.plot(chunk_size, alg_time, label='OpenCV')
        title = 'Performance time of OpenCV vs Length of \'chunks\' on text of length ' + str(text_length)
    pyplot.legend(loc='upper right')
    pyplot.title(title)
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
    pyplot.plot(text_length, time['nlogn'], label='nk lognk')
    pyplot.plot(text_length, time['nlogm'],  label='nk logm',)
    pyplot.title('Time Performance of Algorithms vs Text Length')

    pyplot.legend(loc='upper left')
    pyplot.show()

def plot_k_time(data):
    k_length = []
    time = {}

    for d in data:
        # first, graph accuracy vs text length for each algorithm
        k_length.append(d['k'])
        for alg in d['algorithms']:
            if alg['name'] not in time:
                time[alg['name']] = []
            time[alg['name']].append(alg['time'])

    pyplot.xlabel('k')
    pyplot.ylabel('Time/msecs')
    pyplot.plot(k_length, time['boyermoore'], label='boyer moore')
    pyplot.plot(k_length, time['opencv'], label='opencv')
    pyplot.plot(k_length, time['nlogn'], label='nk lognk')
    title = 'Time Performance of Algorithms vs Number of Texts on text length, 10240'
    pyplot.title(title)

    pyplot.legend(loc='upper left')
    pyplot.show()

parser = argparse.ArgumentParser(description='Graph values from analysis.')
parser.add_argument('-c','--chunk', nargs=1, choices=['nlogm', 'opencv'],
                    help='Graph by chunk size on an algorithm.')
# Pattern arg: substring to search genomes for.
parser.add_argument('-k','--genenum', action="store_true",
                    help='Analyze by number of texts the algorithms.')
parser.add_argument('data', help='The file to load data from.')


args = parser.parse_args()

data = []
with open(args.data) as dn:
    title = dn.readline()
    execution = dn.readline()
    for line in dn:
        data.append(yaml.load(line.rstrip()))

if args.genenum:
    plot_k_time(data)
elif args.chunk:
    plot_chunk_time(data, args.chunk[0])
else:
    plot_alg_time(data)
