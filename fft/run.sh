#!/bin/bash

echo nlogn start
date
./cli.py -a nlogn CAG ../reference/huntington/huntington.fa > huntingtin_CAGs_nlogn.txt
date
echo nlogn finish

echo nlogm start
date
./cli.py -a nlogm CAG ../reference/huntington/huntington.fa > huntingtin_CAGs_nlogm.txt
date
echo nlogm finish
