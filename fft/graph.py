import matplotlib.pyplot as pyplot
import yaml
import argparse


parser = argparse.ArgumentParser(description='Graph values from analysis.')
parser.add_argument('data', help='The file to load data from.')

args = parser.parse_args()

data = []
with open(args.data) as dn:
    for line in dn:
        data.append(yaml.load(line.rstrip()))

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

print time['nlogm']
pyplot.xlabel('Text Length')
pyplot.ylabel('Time/msecs')
pyplot.plot(text_length, time['boyermoore'], label='boyer moore')
pyplot.plot(text_length, time['nlogn'], label='nlogn')
pyplot.plot(text_length, time['nlogm'],  label='nlogm',)
pyplot.show()
