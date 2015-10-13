import numpy as np

f = open('1d.txt')

def string_to_binary_array(s, size=None):
    #TODO: check dtype for the algorithm
    A,C,G,T = [np.zeros(len(s) if not size else size) for _ in range(4)]
    t = np.zeros(len(s) if not size else size)
    for index, val in enumerate(s):
        t[index] = ord(val)

    return t

text = f.read().replace('\n', '')

encoded_text = string_to_binary_array(text)

template = 'ACG'
encoded_pattern = string_to_binary_array(template,size=len(text))

encoded_txt = np.fft.fft(encoded_text)
encoded_pat = np.fft.fft(encoded_pattern)

out_term1 = encoded_pat**3 * encoded_txt 
out_term2 = encoded_pat**2 * encoded_txt**2
out_term3 = encoded_pat * encoded_txt**3

out_term1 = np.fft.ifft(out_term1)
out_term2 = np.fft.ifft(out_term2)
out_term3 = np.fft.ifft(out_term3)


out = out_term1/(len(text)) + out_term2/(len(text)) + out_term3/len(text)
