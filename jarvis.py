import numpy as np
from sys import argv
import os

first_dir = argv[1]
second_dir = argv[2]
parameter = int(argv[3])

def Dist(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix [x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def GetSimilarity(first, second):
    with open(first_dir + '/' + first, 'r') as file:
        data = file.read().replace('\n', '')
        str1=data.replace(' ', '')
    with open(second_dir + '/' + second, 'r') as file:
        data = file.read().replace('\n', '')
        str2=data.replace(' ', '')
    if(len(str1)>len(str2)):
        length=len(str1)
    else:
        length=len(str2)

    return 100 - round((Dist(str1, str2) / length) * 100, 2)


identical = []
similar = []
dists = []
only_in_first = []
only_in_second = []


for first_filename in os.listdir(first_dir):
    is_in_second = False
    for second_filename in os.listdir(second_dir):
        similarity = GetSimilarity(first_filename, second_filename)
        if (similarity == 100):
            pair = [first_filename, second_filename]
            identical.append(pair)
            is_in_second = True
        elif (similarity > parameter):
            pair = [first_filename, second_filename]
            similar.append(pair)
            dists.append(similarity)
            is_in_second = True
    if not is_in_second:
        only_in_first.append(first_filename)


for second_filename in os.listdir(second_dir):
    is_in_first = False
    for pair in identical:
        if second_filename == pair[1]:
            is_in_first = True
            break
    for pair in similar:
        if second_filename == pair[1]:
            is_in_first = True
            break
    if not is_in_first:
        only_in_second.append(second_filename)


print('Identical files:')
for pair in identical:
    print(first_dir + '/' + pair[0] + ' - ' + second_dir + '/' + pair[1])

print()

print('Similar files:')
for i, pair in enumerate(similar):
    print(first_dir + '/' + pair[0] + ' - ' + second_dir + '/' + pair[1] + ' - ' + str(dists[i]))

print()

print('Only in first directory:')
for file in only_in_first:
    print(first_dir + '/' + file)

print()

print('Only in second directory:')
for file in only_in_second:
    print(second_dir + '/' + file)

