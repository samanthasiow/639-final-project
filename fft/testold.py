import numpy as np

f = open('1d.txt')

def string_to_binary_arrays(s, size=None):
    '''Converts the string s into arrays corresponding to nucleotides.  A
    nucleotide array has a 1 in a position p if that nucleotide is present at
    the corresponding index.'''
    #TODO: check dtype for the algorithm
    A,C,G,T = [np.zeros(len(s) if not size else size) for _ in range(4)]
    d = {'A': A, 'G': G, 'C': C, 'T': T}

    for index, val in enumerate(s):
        d[val][index] = 1

    assert sum(A+C+G+T) == len(s)
    return A,C,G,T

text = f.read().replace('\n', '')

A,C,G,T = string_to_binary_arrays(text)

template = 'ACG'
T_A,T_C,T_G,T_T = string_to_binary_arrays(template,size=len(text))

A_f, C_f, G_f, T_f = np.fft.fft(A),\
                     np.fft.fft(C),\
                     np.fft.fft(G),\
                     np.fft.fft(T)


T_A_f, T_C_f, T_G_f, T_T_f = np.fft.fft(T_A),\
                     np.fft.fft(T_C),\
                     np.fft.fft(T_G),\
                     np.fft.fft(T_T)

O_A, O_C, O_G, O_T = np.zeros(len(text)),\
                     np.zeros(len(text)),\
                     np.zeros(len(text)),\
                     np.zeros(len(text))

O_A = T_A_f **3 - 2 * T_A_f**2 * A_f + T_A_f * A_f**2
O_C = T_C_f **3 - 2 * T_C_f**2 * C_f + T_C_f * C_f**2
O_G = T_G_f **3 - 2 * T_G_f**2 * G_f + T_G_f * G_f**2
O_T = T_T_f **3 - 2 * T_T_f**2 * T_f + T_T_f * T_f**2

