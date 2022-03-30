"""
Author: Lilian Bosc
We want to create an objet easy to manipulate in order to mine and match pattern on it
This objet will be affiliatded with an alphabet.
"""
from sre_constants import JUMP
import string_matcher

class String_Object:
    def __init__(self, alphabet, string=""):
        """
        alphabet is a list of possible characters in string
        string is a string with the characters of alphabet only
        """
        for el in string:
            if el not in alphabet:
                print(f"Error: This object is impossible because {el} is not in the alphabet.")
                self.string = "no object"
                self.alphabet = "no object"
                return None
        self.alphabet = alphabet
        self.string = string
        self.string_list = list(string)

    def __repr__(self):
        return self.string

    def support_count(self, char):
        count = 0
        for el in self.string:
            if el == char:
                count += 1
        return count

    def support(self, char):
        return self.support_count(char)/len(self.string)

    # Pattern matcher algorithms
    def matcher_naive_algo(self, pattern):
        pattern_locations = []
        pattern = list(pattern)
        for i in range(len(self.string)-len(pattern)+1):
            part = []
            for k in range(len(pattern)):
                part.append(self.string_list[i+k])
            if part == pattern:
                pattern_locations.append(i)
        return pattern_locations

    def KMP_prefix(self, pattern):
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

    def KMP_algorithm(self, pattern):
        """
        The idea
        """
        pattern = list(pattern)
        sequence = self.string
        output = []
        prefix = self.KMP_prefix(pattern)
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
    

# 1. Definition of the frequency
def psi(x):
    return x**2.9


def phi(x):
    return 0

def count(pattern, sequence, alphabet):
    """
    give the number of iterances of pattern in sequence
    it is pattern matching
    """
    pattern = list(pattern.string)
    return len(string_matcher.boyer_moore_algo(pattern, sequence, alphabet))

def frequency(pattern, txt, alphabet):
    N_pattern = count(pattern, txt, alphabet)
    for simili in pattern.similis:
        N_pattern += phi(pattern.similarity(simili))
    return N_pattern/len(txt)*psi(pattern.length)

class Pattern:
    def __init__(self, string, txt, alphabet, indexes=None, frequency=frequency):
        self.string = string
        self.length = len(self.string)
        self.txt = txt
        self.alphabet = alphabet
        self.similis = []
        self.frequency = frequency(self, txt, alphabet)
        self.indexes = indexes
        

    def __repr__(self):
        return self.string

    def similarity(self, patternbis):        
        champ = 0
        for i in range(self.length):
            for j in range(patternbis.length):
                c = 0
                k = 0
                while self.string[i+k] == patternbis.string[j+k] and c < patternbis.length - j -1 and i+k < self.length-1 and j+k < patternbis.length-1:
                    k += 1
                    c += 1
                if c+1 > champ:
                    champ = c+1
        return champ/max(patternbis.length, self.length)


# p1 = Pattern("espÃ", "espÃÃ¨re", "espÃÃ¨re")
# p2 = Pattern("Ã¨re", "espÃÃ¨re", "espÃÃ¨re")
# print(p1.similis)
# print(p1.similarity(p2))