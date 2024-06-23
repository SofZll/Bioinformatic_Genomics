# Compute the inside and outside CpG island models, and use them for scoring a query sequence
# Input: CpG sequences, non-CpG sequences, .fa file genome sequence
# Output: log-ratio score of X given the inside and outside models
# Bonus assignment: Scan a long genome sequence using a sliding window to find CpG islands
# Output Bonus: a txt with file nema (without extension), start, end and length of CpG islands, the CpG count, the CGcontent, pctGC and the log-ratio score of each CpG island

import sys
import math

#Function to compute the inside CpG island model
#arguments: CpG sequences
#return: the inside CpG island model
def inside_cpg_model(cpg):
    inside_model = {}
    for i in range(len(cpg[0])):
        inside_model[i] = {}
        for base in 'ACGT':
            inside_model[i][base] = 0
    for seq in cpg:
        for i in range(len(seq)):
            inside_model[i][seq[i]] += 1
    return inside_model

#Function to compute the outside CpG island model
#arguments: non-CpG sequences
#return: the outside CpG island model
def outside_cpg_model(non_cpg):
    outside_model = {}
    for i in range(len(non_cpg[0])):
        outside_model[i] = {}
        for base in 'ACGT':
            outside_model[i][base] = 0
    for seq in non_cpg:
        for i in range(len(seq)):
            outside_model[i][seq[i]] += 1
    return outside_model

#Function to score a query sequence given the inside and outside models
#arguments: query sequence, inside model, outside model
#return: the log-ratio score of the query sequence given the inside and outside models
def score_sequence(query, inside_model, outside_model):
    score = 0
    for i in range(len(query)):
        score += math.log2((inside_model[i][query[i]] + 1) / (outside_model[i][query[i]] + 1))
    return score

#Function to scan a long genome sequence using a sliding window
#skip the long stretches of 'N'
#arguments: genome sequence, window size, inside model, outside model
#return: the start, end and length of CpG islands, the CpG count, the CGcontent, pctGC and the log-ratio score of each CpG island
def scan_genome(genome, window_size, inside_model, outside_model):
    cpg_islands = []
    for i in range(len(genome) - window_size + 1):
        window = genome[i:i+window_size]
        if 'N' in window:
            continue
        cpg_count = window.count('CG')
        cpg_content = cpg_count / window_size
        pct_gc = (window.count('G') + window.count('C')) / window_size
        score = score_sequence(window, inside_model, outside_model)
        if score > 0:
            cpg_islands.append((i, i+window_size-1, window_size, cpg_count, cpg_content, pct_gc, score))
    return cpg_islands

#Function to clene the genome sequence
#conert lower-case characters to upper-case
#arguments: a .fa file
#return: list of the genome sequences 
def clean_genome(file):
    with open(file, 'r') as f:
        genome = ''
        for line in f:
            if not line.startswith('>'):
                genome += line.strip().upper()
    return genome

if __name__ == '__main__':
    # inpunt CpG sequences, non-CpG sequences, .fa file genome sequence
    if len(sys.argv) != 4:
        sys.exit("Usage: python CpG_island_models.py CpG_sequences non_CpG_sequences genome.fa")
    cpg = sys.argv[1].split()
    non_cpg = sys.argv[2].split()
    genome = clean_genome(sys.argv[3])

    # compute the inside and outside CpG island models
    inside_model = inside_cpg_model(cpg)
    outside_model = outside_cpg_model(non_cpg)

    # scan the genome sequence using a sliding window
    lenIaland = 555
    scores = scan_genome(genome, lenIaland, inside_model, outside_model)

    # output .txt file with CpG islands
    with open(sys.argv[3].split('.')[0] + '_CpG_islands.txt', 'w') as f:
        f.write('chr\tstart\tend\tlength\tCpG_count\tCpG_content\tpctGC\tscore\n')
        for i, island in enumerate(scores):
            f.write(f'{sys.argv[3].split('.')[0]}\t{sys.argv[3].split('.')[0]}\t{island[0]}\t{island[1]}\t{island[2]}\t{island[3]}\t{island[4]}\t{island[5]}\t{island[6]}\n')