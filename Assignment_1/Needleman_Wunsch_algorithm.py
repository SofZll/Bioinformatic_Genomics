# Needleman & Wunsch algoritm

import sys

# Function to fill the matrix with the gap penalties
# arguments: Matrix
# return: Matrix
def gap_penalties_filler(Matrix):
    counter_r = 1
    counter_c = 1
    Matrix[0][0] = (0, 'n')

    while counter_r < len(Matrix) or counter_c < len(Matrix[0]):
        if counter_r < len(Matrix):
            Matrix[counter_r][0] = (-2 * counter_r, 'n')
            counter_r += 1
        if counter_c < len(Matrix[0]):
            Matrix[0][counter_c] = (-2 * counter_c, 'n')
            counter_c += 1

    #print(Matrix)

    return Matrix

# Function to fill the matrix with the scores
# arguments: Matrix, sequence1, sequence2
# return: Matrix
def score_filler(Matrix, sequence1, sequence2):
    for i in range(1, len(sequence1) + 1):
        for j in range(1, len(sequence2) + 1):
            if sequence1[i - 1] == sequence2[j - 1]:
                match = 1
            else:
                match = -1

            diagonal = Matrix[i - 1][j - 1][0] + match
            up = Matrix[i - 1][j][0] - 2
            left = Matrix[i][j - 1][0] - 2

            max_score = max(diagonal, up, left)

            if max_score == diagonal:
               Matrix[i][j] = (max_score, 'd')
            elif max_score == up:
                Matrix[i][j] = (max_score, 'u')
            else:
                Matrix[i][j] = (max_score, 'l')
    #print(Matrix)

    return Matrix

# Function to trace back the path
# arguments: Matrix, sequence1, sequence2
# return: Global_alignment
def trace_back(Matrix, sequence1, sequence2):
    i = len(sequence1)
    j = len(sequence2)
    alignment1 = ''
    alignment2 = ''

    while i > 0 or j > 0:
        if Matrix[i][j][1] == 'd':
            alignment1 = sequence1[i - 1] + alignment1
            alignment2 = sequence2[j - 1] + alignment2
            i -= 1
            j -= 1
        elif Matrix[i][j][1] == 'u':
            alignment1 = sequence1[i - 1] + alignment1
            alignment2 = '-' + alignment2
            i -= 1
        else:
            alignment1 = '-' + alignment1
            alignment2 = sequence2[j - 1] + alignment2
            j -= 1
    
    return (alignment1, alignment2)

# Needleman & Wunsch algorithm function
# arguments: sequence1, sequence2
# return: Global_alignment
def Needleman_Wunsch_algorithm(sequence1, sequence2):
    Matrix = [[(0, 'n')] * (len(sequence2) + 1) for i in range(len(sequence1) + 1)]
    #print(Matrix)
    Matrix = gap_penalties_filler(Matrix)
    Matrix = score_filler(Matrix, sequence1, sequence2)
    Global_alignment = trace_back(Matrix, sequence1, sequence2)

    return Global_alignment



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 Needleman_Wunsch_algorithm.py sequence1 sequence2')
        sys.exit(1)
    
    Global_alignment = Needleman_Wunsch_algorithm(sys.argv[1], sys.argv[2])
    print(f'Global alignment: {Global_alignment[0]}\t{Global_alignment[1]}')