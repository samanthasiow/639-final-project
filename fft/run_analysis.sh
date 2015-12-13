#!/bin/bash

echo 'Running analysis of time vs test length.' > ../results/genes_data/performance_by_text_length
echo 'Run with: python analysis.py CAG ../Genes/Genes\ by\ Size/pow_[GENE NUM]/*' >> ../results/genes_data/performance_by_text_length

for i in `seq 6 16`;
    do
        echo 'Getting analysis of time VS text length on genes of size' $i
        python analysis.py CAG ../Genes/Genes\ by\ Size/pow_$i/* >> ../results/genes_data/performance_by_text_length
    done

python graph.py ../results/genes_data/performance_by_text_length

echo 'Running optimized analysis of time vs test length. Chunk size for nlogm = 300.' > ../results/genes_data/optimized_performance_by_text_length
echo 'Run with: python analysis.py -o CAG ../Genes/Genes\ by\ Size/pow_[GENE NUM]/*' >> ../results/genes_data/optimized_performance_by_text_length

for i in `seq 6 16`;
    do
        echo 'Getting optimized analysis of time VS text length on genes of size, with m=300' $i
        python analysis.py -o CAG ../Genes/Genes\ by\ Size/pow_$i/* >> ../results/genes_data/optimized_performance_by_text_length
    done

python graph.py ../results/genes_data/optimized_performance_by_text_length

echo 'Running nklogm analysis of time vs chunk size.' > ../results/genes_data/nlogm_performance_by_chunk_size
echo 'Run with: python analysis.py -c 300 CAG ../Genes/Genes\ by\ Size/pow_[GENE NUM]/*' >> ../results/genes_data/nlogm_performance_by_chunk_size

echo 'Getting nklogm analysis of time VS chunk_size on genes of size 2^10'
python analysis.py -c 1000 CAG ../Genes/Genes\ by\ Size/pow_10/* >> ../results/genes_data/nlogm_performance_by_chunk_size

python graph.py -c nlogm ../results/genes_data/nlogm_performance_by_chunk_size

echo 'Running opencv analysis of time vs chunk size.' > ../results/genes_data/opencv_performance_by_chunk_size
echo 'Run with: python analysis.py -c 300 -v CAG ../Genes/Genes\ by\ Size/pow_10/*' >> ../results/genes_data/opencv_performance_by_chunk_size

echo 'Getting opencv analysis of time VS chunk_size on genes of size 2^10'
python analysis.py -c 300 -v CAG ../Genes/Genes\ by\ Size/pow_10/* >> ../results/genes_data/opencv_performance_by_chunk_size

python graph.py -c opencv ../results/genes_data/opencv_performance_by_chunk_size

echo 'Running algorithm analysis of time vs size of texts.' > ../results/genes_data/opencv_performance_by_chunk_size
echo 'Run with: python analysis.py -k CAG ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* > ../results/genes_data/performance_by_k' >> ../results/genes_data/opencv_performance_by_chunk_size

echo 'Running algorithm analysis of time vs size of text, of text length 2^10.' > ../results/genes_data/performance_by_k
echo 'Run with: python analysis.py -k CAG ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* > ../results/genes_data/performance_by_k' >> ../results/genes_data/performance_by_k
python analysis.py -k CAG ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* ../Genes/Genes\ by\ Size/pow_10/* > ../results/genes_data/performance_by_k

python graph.py -k ../results/genes_data/performance_by_k
