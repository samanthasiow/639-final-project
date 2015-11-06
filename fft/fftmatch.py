'''
Implementation of the FFT match-index problem for finding one substring inside
a source text (genome).
'''
import numpy as np

def string_to_binary_array(s, size=None):
    #TODO: check dtype for the algorithm
    A,C,G,T = [np.zeros(len(s) if not size else size) for _ in range(4)]
    t = np.zeros(len(s) if not size else size)
    for index, val in enumerate(s):
        t[index] = ord(val)

    return t

#TODO: replace this with one of our other faster match-index solving algs from
# lecture notes or homeworks
def naive_string_match_index(text, pattern):
    '''A naive string matching algorithm that solves the match-index problem.
    The match-index problem provides a list of indices where a pattern matches
    a text.
    arguments:
      text: the text that you are interested in find
      pattern: the pattern that may be contained in multiple locations inside
        the text
    returns: a list containing the 0-based indices of matches of pattern in text
    '''
    pattern_len = len(pattern)
    matches = []
    for i in range(len(text)-len(pattern)+1):
        if text[i:i+pattern_len] == pattern:
            matches.append(i)
    return matches

def fft_match_index_n_log_n(text, pattern):
    '''Does the n log n FFT pattern matching algorithm.  This solves the match
    index problem by returning a list of indices where the pattern matches the
    text.

    Does cross-correlation solving the following equation:
    S_{i} = \Sigma_{j=1}^{m} (p_{j}^{3} t_{i+j-1} - 2p_{j}^{2}t_{i+j-1}^{2}
                              + p_{j}t_{i+j-1}^{3})
    This can be solved in Fourier space using FFT's of each of the three terms.

    S_{i} = 0 when there is a match between the pattern and text at that
    location.

    TODO: cite papers

    arguments:
      text: the text that you are interested in find
      pattern: the pattern that may be contained in multiple locations inside
        the text
    returns: a list containing the 0-based indices of matches of pattern in text
    '''
    n = len(text)
    m = len(pattern)
    binary_encoded_text = string_to_binary_array(text)

    #TODO: for binary_encoded_text and pattern, if the char is equal to the
    # don't care character, then set the float value to 0.0
    text = binary_encoded_text
    textSq = text * text
    textCube = textSq * text

    binary_encoded_pattern = string_to_binary_array(pattern,size=len(text))

    pattern = binary_encoded_pattern
    patternSq = pattern * pattern
    patternCube = patternSq * pattern

    textKey = np.fft.fft(text)
    textSqKey = np.fft.fft(textSq)
    textCubeKey = np.fft.fft(textCube)

    patternKey = np.fft.fft(pattern)
    patternSqKey = np.fft.fft(patternSq)
    patternCubeKey = np.fft.fft(patternCube)

    #there are three terms.  Since fft(key) is Linear, we will IFT each
    #individually
    outTerm1Key = patternCubeKey * textKey
    #-2 * outTerm2Key?
    outTerm2Key =  patternSqKey * textSqKey
    outTerm3Key = patternKey * patternCubeKey

    outTerm1 = np.fft.ifft(outTerm1Key)
    outTerm2 = -2*np.fft.ifft(outTerm2Key)
    outTerm3 = np.fft.ifft(outTerm3Key)

    #1D
    #for i in range(out.shape[0]):
    #    i = out[i]
    #    if abs(i.imag) < 1.0e-6 and abs(i.real) < 1.0e-6:
    #        print i
    #may need to rotate?
    out = outTerm1 + outTerm2 + outTerm3

    #this should be 0 if match
    print min(abs(out))

    return out
    #for i in range(n-m):
    #    index = m+i-1
    #    temp = outTerm1[index] + outTerm2[index] + outTerm3[index]
    #    print temp
    #    if abs(temp) < 1.0e-6:
    #        print i,temp

    #return out

if __name__ == '__main__':
    f = open('1d.txt')
    text = f.read().replace('\n', '')
    pattern = 'ACG'

    out = fft_match_index_n_log_n(text, pattern)
    print out, naive_string_match_index(text, pattern)
    assert out == naive_string_match_index(text, pattern)
    #print(out)
