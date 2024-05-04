#Brute force algorithm to solve the shortest common superstring (SCS) problem
#Input: a set of strings
#Output: their shortest common superstring

import sys

#Function tu find the length of longest suffix of 'a' matching a prefix of 'b'
#arguments: string a, string b
#return the length of the overlap and if no overlap exists, return 0
def overlap(a, b):
    
    start = 0
    while True:
        start = a.find(b[:1], start)
        if start == -1:
            return 0
        if b.startswith(a[start:]):
            return len(a) - start
        start += 1

#Function to buid a common string from a set of strings
#arguments: a set of strings, sequences
#return: common_string
def build_common_string(sequences):
    common_string = sequences[0]
    for i in range(1, len(sequences)):
        o = overlap(common_string, sequences[i])
        if o > 0:
            common_string += sequences[i][o:]
        else:
            common_string += sequences[i]
    return common_string

#Function to generate a list of lists of all possible permutations of a set of strings
#arguments: a set of strings
#return: all_combinations
def generate_combinations(strings):
    if len(strings) == 0:
        return [['']]
    
    all_combinations = []
    for i in range(len(strings)):
        current_string = strings[i]
        remaining_strings = strings[:i] + strings[i+1:]
        remaining_combinations = generate_combinations(remaining_strings)
        for combination in remaining_combinations:
            new_combination = [current_string] + combination
            all_combinations.append(new_combination)
    
    return all_combinations

#Function to find all the common superstring
#arguments: a list of strings
#return: all_common_superstrings
def all_common_superstrings(strings):
    all_combinations = generate_combinations(strings)
    all_common_superstrings = []
    for combination in all_combinations:
        all_common_superstrings.append(build_common_string(combination[:-1]))
    return all_common_superstrings

#Function to find the shortest common superstring
#arguments: a set of strings sequences
#return: their shortest_superstring
def shortest_superstring(sequences):
    common_superstrings = all_common_superstrings(sequences)
    shortest_superstring = common_superstrings[0]
    for common_superstring in common_superstrings:
        if len(common_superstring) < len(shortest_superstring):
            shortest_superstring = common_superstring
    return shortest_superstring

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 Shortest_Common_Superstring_bruteForce_algorithm.py <sequence1> <sequence2> ... <sequenceN>")
        sys.exit()

    sequences = sys.argv[1:]
    shortest_superstring = shortest_superstring(sequences)
    print(f'Shortest common superstring: {shortest_superstring}\nLength: {len(shortest_superstring)}\n')