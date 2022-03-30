"""
Author: Lilian Bosc
We will conduct a study of all the algorithms to search an already known pattern
"""
from data_treatment import *


# The algorithms
def naive_algo(pattern, sequence):
    """
    The idea is to verify one by one every possible location of the pattern
    """
    pattern_locations = []
    for i in range(len(sequence)-len(pattern)+1):
        part = []
        for k in range(len(pattern)):
            part.append(sequence[i+k])
        if part == pattern:
            pattern_locations.append(i)
    return pattern_locations

def KMP_prefix(pattern):
    """
    Construct the table of the repetition of the prefix of the pattern in
    the pattern itself.
    """
    length = len(pattern)
    prefix = [-1 for _ in pattern]
    prefix[0] = 0
    a = 0
    for b in range(1, length):
        while a > 0 and pattern[a] != pattern[b]:
            a = prefix[a]
        if pattern[a] == pattern[b]:
            a += 1
        prefix[b] = a
    return prefix

def KMP_algorithm(pattern, sequence):
    """
    The idea
    """
    output = []
    prefix = KMP_prefix(pattern)
    i=0
    j=0
    k=0
    n = len(sequence)
    m = len(pattern)
    while n-k >= m:
        while j < m and sequence[i] == pattern[j]:
            i += 1
            j += 1
        if j > m-1:
            output.append(k)
        if j > 0 and prefix[j-1] > 0:
            k = i-prefix[j-1]
        else:
            if i == k:
                i += 1
            k = i
        if j > 0:
            j = prefix[j-1]-1 +1
    return output

def bm_no_table_algo(pattern, sequence):
    """
    The idea
    """
    pattern_el = list(set(pattern))
    output = []
    n = len(sequence)
    m = len(pattern)
    i = 0
    while i < n-m:
        j = m-1
        k = i + m-1
        while j >= 0 and pattern[j] == sequence[k]:
            j -= 1
            k -= 1
        if j < 0:
            # We have a match
            output.append(i)
            i += m
        else:
            # We have a mismatch at the char pattern[j] and sequence[i+k]
            if sequence[k] not in pattern_el:
                jump = j+1
            else:
                jump = 1
                for _ in range(len(pattern)):
                    # If the goal is to reduce the time, it is better to stock a jump table
                    if sequence[k] != pattern[m-1-jump]:
                        jump += 1
                    else:
                        break
            i += jump
    return output
            

def compute_table(pattern, alphabet):
    table = {}
    for el in alphabet:
        table[el] = len(pattern)
    for k in range(len(pattern)-1):
        if len(pattern)-k-1 < table[pattern[k]]:
            table[pattern[k]] = len(pattern)-k-1
    return table

def boyer_moore_algo(pattern, sequence, alphabet):
    table = compute_table(pattern, alphabet)
    output = []
    n = len(sequence)
    m = len(pattern)
    i = 0 # index that will browse the sequence
    while i < n-m:
        j = m-1 # index of observation on the pattern
        k = m-1 # index of observation on the sequence
        while j >= 0 and pattern[j] == sequence[i+k]:
            j -= 1
            k -= 1
        if j < 0:
            # We have a match
            output.append(i)
            jump = m
        else:
            # We have a mismatch at the position j on the pattern and i+k on the sequence
            # on the character sequence[i+k]
            jump = table[sequence[i+m-1]]
        i += jump
    return output


# # Parameters
# ALPHABET = [1,2,3,4,5,6,7,8,9,0]


# # Generate data
# pattern = [1,2,3,2,3]
# sequence = insert_pattern(pattern, 1, generate_sequence(20, ALPHABET))
# location1 = boyer_moore_algo(pattern, sequence, ALPHABET)
# location2 = KMP_algorithm(pattern, sequence)
# print(location1)
# print(location2)
# print(sequence)




