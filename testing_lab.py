"""
Author: Lilian Bosc
We will conduct a study of all the algorithms to search an already known pattern
"""

import statistics
import time
import string_matcher as algo
from data_treatment import *
import random
import matplotlib.pyplot as plt

# Function for graphs
def evaluate(N, K, M, n_pattern=10):
    """
    N = txt
    K = pattern
    M = alphabet
    """
    alphabet = range(M)
    pattern = [random.choice(alphabet) for _ in range(K)]
    txt = insert_pattern(pattern, n_pattern, generate_sequence(N, alphabet))
    print(txt, pattern)
    measures_naive = []
    for i in range(100):
        start = time.time()
        
        locations = algo.naive_algo(pattern, txt)
        
        end = time.time()
        measures_naive.append(end - start)

    mean_naive = statistics.mean(measures_naive)
    print("naive")
    measures_KMP = []
    for i in range(100):
        start = time.time()
        
        locations = algo.KMP_algorithm(pattern, txt)
        
        end = time.time()
        measures_KMP.append(end - start)

    mean_KMP = statistics.mean(measures_KMP)
    print("KMP")
    measures_BMH = []
    for i in range(100):
        start = time.time()
        
        locations = algo.boyer_moore_algo(pattern, txt, alphabet)
        
        end = time.time()
        measures_BMH.append(end - start)

    mean_BMH = statistics.mean(measures_BMH)
    print("BMH")
    return mean_naive, mean_KMP, mean_BMH

def graph(n_ech=50):
    """
    N_max, K_max, M_max, 
    N = txt
    K = pattern
    M = alphabet
    """
    med = n_ech//2
    Ns = [1000+10*k for k in range(n_ech)]
    Ks = [1+k for k in range(n_ech)]
    Ms = [2+2*k for k in range(n_ech)]

    results = []
    for k in range(n_ech):
        print(f"epoch: {k}/{n_ech}")
        results.append(evaluate(1000, 5, Ms[k], n_pattern=5))

    naive = []
    for k in range(n_ech):
        naive.append(results[k][0])
    KMP = []
    for k in range(n_ech):
        KMP.append(results[k][1])
    BMH = []
    for k in range(n_ech):
        BMH.append(results[k][2])

    plt.plot(Ms, naive, label="Naive")
    plt.plot(Ms, KMP, label="KMP")
    plt.plot(Ms, BMH, label="BMH")
    plt.xlabel("M")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.show()

    return naive, KMP, BMH


    
results = graph()



# Parameters
# ALPHABET = list("azertyuiopqsdfghjklmwxcvbn")
# TXT_LENGHT = 100

# # Generate data
# pattern = list("abc")
# sequence = insert_pattern(pattern, 10, generate_sequence(100000, ALPHABET))

# Test lab






# print("Naive algorithm:")
# measures = []
# for i in range(100):
#     start = time.time()
    
#     locations = algo.naive_algo(pattern, sequence)
    
#     end = time.time()
#     measures.append(end - start)

# mean = statistics.mean(measures)
# stdev = statistics.stdev(measures)

# print(len(locations))
# print('Temps d\'exécution :')
# print(f' - Moyenne : {mean:.1}ms')
# print(f' - Écart-type : {stdev:.1}ms')

# print("\nKnuth-Morris-Pratt algorithm")
# measures = []
# for i in range(100):
#     start = time.time()
    
#     locations = algo.KMP_algorithm(pattern, sequence)
    
#     end = time.time()
#     measures.append(end - start)

# mean = statistics.mean(measures)
# stdev = statistics.stdev(measures)

# print(len(locations))
# print('Temps d\'exécution :')
# print(f' - Moyenne : {mean:.1}ms')
# print(f' - Écart-type : {stdev:.1}ms')

# print("\nBoyer Moore algorithm without table")
# measures = []
# for i in range(100):
#     start = time.time()
    
#     locations = algo.bm_no_table_algo(pattern, sequence)
    
#     end = time.time()
#     measures.append(end - start)

# mean = statistics.mean(measures)
# stdev = statistics.stdev(measures)

# print(len(locations))
# print('Temps d\'exécution :')
# print(f' - Moyenne : {mean:.1}ms')
# print(f' - Écart-type : {stdev:.1}ms')

# print("\nBoyer-Moore algorithm")
# measures = []
# for i in range(100):
#     start = time.time()
    
#     locations = algo.boyer_moore_algo(pattern, sequence, ALPHABET)
    
#     end = time.time()
#     measures.append(end - start)

# mean = statistics.mean(measures)
# stdev = statistics.stdev(measures)

# print(len(locations))
# print('Temps d\'exécution :')
# print(f' - Moyenne : {mean:.1}ms')
# print(f' - Écart-type : {stdev:.1}ms')
