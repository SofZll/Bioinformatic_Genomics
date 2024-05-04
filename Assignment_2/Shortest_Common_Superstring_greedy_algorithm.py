#Greedy algorithm to solve the shortest common superstring (SCS) problem
#Input: a set of strings
#Output: their shortest common superstring

import sys

#Function tu find the length of longest suffix of 'a' matching a prefix of 'b'
#overlap must be at least 3 characters long
#arguments: string a, string b and the min_overlap_length
#return the overlap_length and if no overlap exists, return 0
def overlap(a, b, min_overlap_length):
    
    start = 0
    while True:
        start = a.find(b[:min_overlap_length], start)
        if start == -1:
            return 0
        if b.startswith(a[start:]):
            return len(a) - start
        start += 1

#Function to built up a matrix of overlaps between all pairs of strings
#arguments: a set of strings
#return: overlap_matrix
def overlap_matrix(strings):
    overlap_matrix = [[0 for _ in range(len(strings))] for _ in range(len(strings))]
    for i in range(len(strings)):
        for j in range(len(strings)):
            if i != j:
                overlap_matrix[i][j] = overlap(strings[i], strings[j], 3)
    return overlap_matrix

#Function to find the pair of strings with the maximum overlap
#arguments: overlaps_matrix between all pairs of strings
#return: from_string to_string with the maximum overlap
def max_overlap_pair(overlap_matrix):
    max_overlap = 0
    from_string = 0
    to_string = 0
    for i in range(len(overlap_matrix)):
        for j in range(len(overlap_matrix)):
            if i != j:
                if overlap_matrix[i][j] > max_overlap:
                    max_overlap = overlap_matrix[i][j]
                    from_string = i
                    to_string = j
    return from_string, to_string, max_overlap

#Function to merge the pair of strings with the maximum overlap
#arguments: a set of strings, from_string, to_string, overlap_length
#return: merged_string
def merge_strings(strings, from_string, to_string, overlap_length):
    merged_string = strings[from_string] + strings[to_string][overlap_length:]
    return merged_string

#Function to reduce the strings list after merging two strings
#arguments: list of strings, from_string, to_string, merged_string
#return: reduced_strings
def reduce_strings(strings, from_string, to_string, merged_string):
    reduced_strings = strings
    if from_string < to_string:
        reduced_strings.pop(to_string)
        reduced_strings.pop(from_string)
    else:
        reduced_strings.pop(from_string)
        reduced_strings.pop(to_string)
    reduced_strings.append(merged_string)
    return reduced_strings

#Function to reduce the overlap matrix after merging two strings
#arguments: overlap_matrix, strins, from_string, to_string, merged_string
#return: reduced_overlap_matrix
def reduce_overlap_matrix(overlap_matrix, strings, from_string, to_string, merged_string):
    reduced_overlap_matrix = overlap_matrix
    if from_string < to_string:
        reduced_overlap_matrix.pop(to_string)
        reduced_overlap_matrix.pop(from_string)
    else:
        reduced_overlap_matrix.pop(from_string)
        reduced_overlap_matrix.pop(to_string)
    for i in range(len(reduced_overlap_matrix)):
        if from_string < to_string:
            reduced_overlap_matrix[i].pop(to_string)
            reduced_overlap_matrix[i].pop(from_string)
        else:
            reduced_overlap_matrix[i].pop(from_string)
            reduced_overlap_matrix[i].pop(to_string)
    for i in range(len(reduced_overlap_matrix)):
        reduced_overlap_matrix[i].append(overlap(merged_string, strings[i], 3))
    reduced_overlap_matrix.append([])
    for i in range(len(reduced_overlap_matrix)-1):
        reduced_overlap_matrix[-1].append(overlap(merged_string, strings[i], 3))
    reduced_overlap_matrix[-1].append(0)
    return reduced_overlap_matrix

#Function to find the shortest common superstring
#arguments: a set of strings sequences
#return: their shortest_superstring
def shortest_superstring(sequences):
    list_of_strings = sequences
    overlap_val_matrix = overlap_matrix(list_of_strings)
    while len(list_of_strings) > 1:
        from_string, to_string, overlap_length = max_overlap_pair(overlap_val_matrix)
        merged_string = merge_strings(list_of_strings, from_string, to_string, overlap_length)
        list_of_strings = reduce_strings(list_of_strings, from_string, to_string, merged_string)
        overlap_val_matrix = reduce_overlap_matrix(overlap_val_matrix, list_of_strings, from_string, to_string, merged_string)
    shortest_superstring = list_of_strings[0]
    return shortest_superstring


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 Shortest_Common_Superstring_greedy_algorithm.py <sequence1> <sequence2> ... <sequenceN>")
        sys.exit()

    sequences = sys.argv[1:]
    shortest_superstring = shortest_superstring(sequences)
    print(f"The shortest common superstring is: {shortest_superstring}\nLength: {len(shortest_superstring)}\n")