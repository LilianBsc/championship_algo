"""
Author: Lilian Bosc
"""

from random import randint

# faire une classe suite pour faciliter l'utilisation

# create the environment
def generate_sequence(txt_lenght, alphabet):
    """
    Generate a random sequence of the item of alphabet
    param: int txt_lenght the size of the sequence
           list alphabet a list of items 
    """
    sequence = []
    for _ in range(txt_lenght) :
        sequence.append(alphabet[randint(0,len(alphabet)-1)])
    return sequence

def generate_indexes(nb_appart, nb_indexes, sequence_lenght):
    """
    Generate random indexes where to put the recurent pattern in the most efficient way possible
    param: int nb_appart the size of the pattern
           int nb_indexes number of indexes to generate
           int sequence_lenght lenght of the total sequence 
    """
    list_indexes = []
    max_index = sequence_lenght - nb_appart
    while len(list_indexes) < nb_indexes:
        if list_indexes == []:
            list_indexes.append(randint(0, max_index))
        else:
            index = randint(0, max_index)
            is_max = True
            for k in range(len(list_indexes)):
                if index < list_indexes[k]:
                    if abs(index - list_indexes[k]) > nb_appart and abs(index - list_indexes[k-1]) > nb_appart:
                        list_indexes.insert(k, index)
                        is_max = False
                        break
                    else:
                        is_max = False
                        break
            if is_max and abs(index - list_indexes[k]) > nb_appart and abs(index - list_indexes[k-1]) > nb_appart:
                list_indexes.append(index)
    return list_indexes

def insert_pattern(pattern, n_occurrence, sequence):
    """
    param: list pattern the sublist to insert
           int n_occurrence number of occurence of the pattern in the sequence
           list sequence the total sequence
    """
    list_indexes = generate_indexes(len(pattern), n_occurrence, len(sequence))
    for index in list_indexes:
        for k in range(len(pattern)):
            sequence[index+k] = pattern[k]
    return sequence

def stock_data(file_path, sequence):
    with open(file_path, 'w') as file:
        for el in sequence[:-1]:
            file.write(str(el)+";")
        file.write(str(sequence[-1]))

def data_reader_digit(file_path):
    """
    for a list of numbers separated by ;
    """
    with open(file_path, "r") as file:
        string = file.read()
    sequence = string.split(";")
    for k in range(len(sequence)):
        sequence[k] = int(sequence[k])
    return sequence

def data_reader(file_path):
    """
    for a .txt
    """
    with open(file_path, "r") as file:
        string = file.read()
    return string

def numbers_to_txt(list_of_numbers, alphabet):
    if max(list_of_numbers) > len(alphabet):
        print("The alphabet is not corresponding.")
        
    else:
        txt = ""
        for number in list_of_numbers:
            txt += alphabet[number]

        return txt

def txt_to_numbers_with_alphabet(txt, alphabet):
    """
    Non optimized
    """
    txt = list(txt)
    for el in txt:
        if el not in alphabet:
            print(f"The alphabet is not corresponding, {el} is unknown.")
            return None

    list_of_numbers = []
    for char in txt:
        list_of_numbers.append(alphabet.index(char))

    return list_of_numbers

def txt_to_numbers_no_alphabet(txt):
    """
    Non optimized
    """
    txt = list(txt)
    alphabet = []
    list_of_numbers = []
    for char in txt:
        if char not in alphabet:
            alphabet.append(char)
        list_of_numbers.append(alphabet.index(char))

    return list_of_numbers, alphabet

def make_alphabet(txt):
    alphabet = []
    for char in txt:
        if char not in alphabet:
            alphabet.append(char)
    return alphabet

def ASCII_alphabet(n=128):
    alphabet_list = [chr(i) for i in range(n)]
    return alphabet_list

DNA_alphabet = ["A", "C", "G", "U"]