#Smith and Waterman algorithm

import sys

# Matrix initialization function
# arguments: sequence1, sequence2
# return: Matrix
def matrix_init(sequence1, sequence2):
    Matrix = [[(0, 'n')] * (len(sequence2) + 1) for i in range(len(sequence1) + 1)]
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

            max_score = max(diagonal, up, left, 0)

            if max_score == diagonal:
                Matrix[i][j] = (max_score, 'd')
            elif max_score == up:
                Matrix[i][j] = (max_score, 'u')
            elif max_score == left:
                Matrix[i][j] = (max_score, 'l')
            else:
                continue

    return Matrix

#Funbction find max score
def find_max_score(Matrix, sequence1, sequence2):
    max_score = 0
    max_i = 0
    max_j = 0

    for x in range(len(sequence1) + 1):
        for y in range(len(sequence2) + 1):
            if Matrix[x][y][0] > max_score:
                max_score = Matrix[x][y][0]
                max_i = x
                max_j = y

    return (max_i, max_j)

# Function to trace back the path
# arguments: Matrix, sequence1, sequence2
# return: Local_alignment
def trace_back(Matrix, sequence1, sequence2):
    alignment1 = ''
    alignment2 = ''
    (i, j) = find_max_score(Matrix, sequence1, sequence2)


    while i > 0 and j > 0 and Matrix[i][j][0] != 0:

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

        if Matrix[i][j][1] == 'n' and Matrix[i-1][j][1] == 'n' and Matrix[i][j-1][1] == 'n':
            break

    return (alignment1, alignment2)

#Smith and Waterman algorithm functiion
# arguments: sequence1, sequence2
# return: Local_alignment
def smith_waterman(sequence1, sequence2):
    Matrix = matrix_init(sequence1, sequence2)
    Matrix = score_filler(Matrix, sequence1, sequence2)
    alignment = trace_back(Matrix, sequence1, sequence2)
    return alignment

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 Smith_Waterman_algorithm.py sequence1 sequence2')
        sys.exit(1)
    
    Global_alignment = smith_waterman(sys.argv[1], sys.argv[2])
    print(f'Local alignment: {Global_alignment[0]}\t{Global_alignment[1]}')



