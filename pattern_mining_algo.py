"""
Author Lilian Bosc
"""

import os
import string_matcher
import data_treatment as dt
import string_object as so
import matplotlib.pyplot as plt
import numpy as np

# Association Rules functions
def count(pattern, sequence, alphabet):
    """
    give the number of iterances of pattern in sequence
    it is pattern matching
    """
    pattern = list(pattern.string)
    return len(string_matcher.boyer_moore_algo(pattern, sequence, alphabet))

def support(pattern, sequence, alphabet):
    """
    return the frequency of the pattern in the sequence
    """
    return count(pattern, sequence, alphabet)/len(sequence)*len(pattern)


# Apriori algorithm
def join(list1, list2):
    fusion = [p for p in list1]
    fusion.append(list2[-1])
    return fusion

def generate_1_itemsets(sequence, alphabet, minsup):
    visited = []
    frequent_char = []
    for char in sequence:
        if char not in visited:
            visited.append(char)
            if support([char], sequence, alphabet) > minsup:
                frequent_char.append([char])
    return frequent_char

def apriori(sequence, alphabet, minsup):
    """
    sequence is a list of characters
    minsup is the minimum frequency of an itemset (or pattern)
    """
    C_k = generate_1_itemsets(sequence, alphabet, minsup)
    print(C_k)
    result = []
    while C_k != []:
        for el in C_k:
            if el not in result:
                result.append(el)
        new_Ck = []
        for p in C_k:
            for q in C_k:
                if p != q:
                    if join(p,q) not in new_Ck and support(join(p,q), sequence, alphabet) > minsup:
                        new_Ck.append(join(p, q))
        C_k = new_Ck
        print(C_k)

    return result


"""
Personal algorithm: championship algorithm
"""
def make_ranking(champs_dic):
    return sorted(champs_dic.items(), key=lambda t:t[0])

def cleaning(champs_dic, rate_of_dirt=0.2):
    ranking = make_ranking(champs_dic)
    fmax = float(ranking[-1][0])
    x_cut = fmax*rate_of_dirt
    champs_dic = {}
    for el in ranking:
        if float(el[0]) > x_cut:
            champs_dic[el[0]] = el[1]
    return champs_dic
    
def eliminate_losers(champs_dic, rate_losers=0.2):
    ranking = make_ranking(champs_dic)

    N1 = int(len(ranking)*(1-rate_losers))
    champs = ranking[-N1:]
    champs_dic = {}
    for champ in champs:
        champs_dic[champ[0]] = champ[1]
    return champs_dic

def add_new_pattern(new_pattern, champs_dic, visited):
    new_string = new_pattern.string
    if new_string in visited:
        for el in champs_dic[str(new_pattern.frequency)]:
            if el.string == new_string:
                el.indexes.append(new_pattern.indexes[0])
    else:
        visited.append(new_string)
        if str(new_pattern.frequency) in champs_dic:
            champs_dic[str(new_pattern.frequency)].append(new_pattern)
        else:
            champs_dic[str(new_pattern.frequency)] = [new_pattern]

def make_a_lap(champs_dic, lap, txt, minchar, alphabet, visited, fr, mode=0):
    if mode == 1:
        all_patterns = []
        for key in champs_dic:
            for pattern in champs_dic[key]:
                all_patterns.append(pattern)
        to_remove = []
        for key in champs_dic:
            for pattern in champs_dic[key]:
                for patternbis in all_patterns:
                    if pattern != patternbis:
                        if pattern.similarity(patternbis) >= 0.9:
                            if pattern.frequency > patternbis.frequency:
                                to_remove.append(patternbis)
                                if patternbis not in pattern.similis:
                                    pattern.similis.append(patternbis)
                            else:
                                to_remove.append(pattern)
                                if pattern not in patternbis.similis:
                                    patternbis.similis.append(pattern)
        for pattern in to_remove:
            if str(pattern.frequency) in champs_dic and pattern in champs_dic[str(pattern.frequency)]:
                champs_dic[str(pattern.frequency)].remove(pattern)
                if champs_dic[str(pattern.frequency)] == []:
                    del champs_dic[str(pattern.frequency)]

    ranking = make_ranking(champs_dic)

    final_lap = True
    for el in ranking:
        for pattern in el[1]:
            for index in pattern.indexes:
                # We grow only the bigger ones
                if len(pattern.string) == minchar + lap and index + minchar + lap < len(txt):
                    final_lap = False
                    new_string = pattern.string + txt[index + minchar + lap]
                    new_pattern = so.Pattern(new_string, txt, alphabet, indexes=[index], frequency=fr)
                    add_new_pattern(new_pattern, champs_dic, visited)
    if final_lap:
        return -1
    else:
        lap +=1
        return lap

def championship_algorithm(txt, alphabet, minchar, fr=so.frequency, maxlap=12):
    # First we scan the txt
    txt_scan = {}
    visited = []
    for k in range(len(txt)-minchar):
        string = ""
        for i in range(minchar):
            string += txt[k+i]
        pattern = so.Pattern(string, txt, alphabet, indexes=[k], frequency=fr) # can be optimized here
        add_new_pattern(pattern, txt_scan, visited)

    # Precleaning
    champs_dic = cleaning(txt_scan)
    
    # Now we start the race
    lap = 0
    while 0 <= lap < maxlap:
        lap = make_a_lap(champs_dic, lap, txt, minchar, alphabet, visited, fr)
        champs_dic = eliminate_losers(champs_dic)
    
    final_txt = ""
    final_dic = {}
    for key in champs_dic:
        for ptrn in champs_dic[key]:
            final_txt += ptrn.string

    for key in champs_dic:
        for pattern in champs_dic[key]:
            c = count(pattern, final_txt, alphabet=dt.make_alphabet(final_txt))
            if str(c) not in final_dic:
                final_dic[str(c)] = [pattern]
            else:
                final_dic[str(c)].append(pattern)

    to_remove=[]
    to_add=[]
    for key1 in final_dic:
        for pattern1 in final_dic[key1]:
            for key2 in final_dic:
                for pattern2 in final_dic[key2]:
                    if 0.8<pattern1.similarity(pattern2)<1:
                        key_u = str(max(int(key1), int(key2)))
                        new_key = str(int(key1)+int(key2))
                        to_remove.append([key1, pattern1])
                        to_remove.append([key2, pattern2])
                        if key1 == key_u:
                            to_add.append([new_key, pattern1])
                        if key2 == key_u:
                            to_add.append([new_key, pattern2])
                            
    for couple in to_remove:
        if couple[1] in final_dic[couple[0]]:
            final_dic[couple[0]].remove(couple[1])
    for couple in to_add:
        if couple[0] not in final_dic:
            final_dic[couple[0]] = [couple[1]]
        else:
            final_dic[couple[0]].append(couple[1])
                    
    results = make_ranking(final_dic)
    return results

def extract_string(results):
    final_string = ""
    for el in results:
        for pattern in el[1]:
            final_string += pattern.string
    return final_string

"""
Testing area
"""
# jaguar_str = dt.data_reader(".//data//jaguar.txt")
# tigre_str = dt.data_reader(".//data//tigre.txt")
# lion_str = dt.data_reader(".//data//lion.txt")

# alphabet_jaguar = dt.make_alphabet(jaguar_str)
# alphabet_tigre = dt.make_alphabet(tigre_str)
# alphabet_lion = dt.make_alphabet(lion_str)

# results_jaguar = extract_string(championship_algorithm(jaguar_str, alphabet_jaguar, 4, 12))
# print(results_jaguar)
# results_tigre = championship_algorithm(tigre_str, alphabet_tigre, 4, 12)
# print(results_tigre)
# results_lion = championship_algorithm(lion_str, alphabet_lion, 4, 12)
# print(results_lion)

def score(pattern, txt, alphabet):
    N_pattern = count(pattern, txt, alphabet)
    return N_pattern/len(txt)*(pattern.length**0.5)

list_files = os.listdir("data")
list_names = []
for file_name in list_files:
    if ".txt" in file_name:
        list_names.append(file_name[:-4])


exponents = [0.5+5*k/10 for k in range(10)]
accuracies = []
for exponent in exponents:
    score = lambda pattern, txt, alphabet : count(pattern, txt, alphabet)/len(txt)*(pattern.length**exponent)
    
    results = []
    for file_name in list_files:
        if ".txt" in file_name:
            print(file_name)
            txt = dt.data_reader(".//data//"+file_name)
            alphabet = dt.make_alphabet(txt)
            results.append(extract_string(championship_algorithm(txt, alphabet, 3, fr=score)))
            
    foundit = 0
    for k in range(len(results)):
        if list_names[k] in results[k]:
            foundit += 1
    accuracies.append(foundit)

    print(f"with exponent {exponent}, found: {foundit}/{len(results)}")

print(accuracies)

x = np.asarray(exponents)  # the label locations
width = 0.1  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, accuracies, width, label='Number of findings (on 20 trials).')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Number of findings by exponent')
ax.set_xticks(x)
ax.legend()

ax.bar_label(rects1, padding=3)

fig.tight_layout()

plt.show()