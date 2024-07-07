# Compute the inside and outside CpG island models, and use them for scoring a query sequence
# Input: CpG sequences, non-CpG sequences, a query string X
# Output: log-ratio score of X given the inside and outside models

import sys
import math
import random

#Function to compute the inside CpG island model
#arguments: CpG sequences
#return: the inside CpG island model
def inside_cpg_model(cpg):
    # Initialize the inside model
    inside_model = {}
    for i in range(len(cpg[0])):
        inside_model[i] = {base: 0 for base in 'ACGT'}
    
    # Count the occurrences of each nucleotide at each position
    for seq in cpg:
        for i in range(len(seq)):
            inside_model[i][seq[i]] += 1
    
    # Normalize the counts to probabilities
    for i in inside_model:
        total = sum(inside_model[i].values())
        if total > 0:  # Avoid division by zero
            for base in inside_model[i]:
                inside_model[i][base] /= total
    
    return inside_model

#Function to compute the outside CpG island model
#arguments: non-CpG sequences
#return: the outside CpG island model
def outside_cpg_model(non_cpg):
    # Initialize the outside model
    outside_model = {}
    for i in range(len(non_cpg[0])):
        outside_model[i] = {base: 0 for base in 'ACGT'}
    
    # Count the occurrences of each nucleotide at each position
    for seq in non_cpg:
        for i in range(len(seq)):
            outside_model[i][seq[i]] += 1
    
    # Normalize the counts to probabilities
    for i in outside_model:
        total = sum(outside_model[i].values())
        if total > 0:  # Avoid division by zero
            for base in outside_model[i]:
                outside_model[i][base] /= total
    
    return outside_model

#Function to score a query sequence given the inside and outside models
#arguments: query sequence, inside model, outside model
#return: the log-ratio score of the query sequence given the inside and outside models
def score_sequence(query, inside_model, outside_model):
    score = 0
    for i in range(len(query)):
        score += math.log2((inside_model[i][query[i]] + 1) / (outside_model[i][query[i]] + 1))
    return score

# Generate or input a query sequence of 100 nt
def generate_query_sequence(length=100):
    return ''.join(random.choice('ACGT') for _ in range(length))

if __name__ == '__main__':
    # inpunt CpG sequences, non-CpG sequences, a query string X
    if len(sys.argv) != 4:
        sys.exit("Usage: python CpG_island_models.py CpG_sequences non_CpG_sequences query_string")
    cpg = sys.argv[1].split()
    non_cpg = sys.argv[2].split()
    
    if len(sys.argv) == 4:
        query = sys.argv[3]
    else:
        query = generate_query_sequence()
    
    # compute the inside and outside CpG island models
    inside_model = inside_cpg_model(cpg)
    outside_model = outside_cpg_model(non_cpg)

    # score the query sequence given the inside and outside models
    score = score_sequence(query, inside_model, outside_model)

    print(f"the log-ratio score of {query} given the inside and outside models is {score}")

