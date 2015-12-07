'''
Implementation of the FFT match-index problem for finding one substring inside
a source text (genome).
'''
import numpy as np

def string_to_binary_array(s, size=None):
    #TODO: check dtype for the algorithm
    #A,C,G,T = [np.zeros(len(s) if not size else size) for _ in range(4)]
    t = np.zeros(len(s) if not size else size)
    for index, val in enumerate(s):
        t[index] = float(ord(val))

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
    returns: a numpy array containing the 0-based indices of matches of pattern
             in text
    '''
    pattern_len = len(pattern)
    matches = []
    for i in range(len(text)-len(pattern)+1):
        if text[i:i+pattern_len] == pattern:
            matches.append(i)
    return np.array(matches)

def fft_match_index(text, pattern, n, m):
    '''Does the n log n FFT pattern matching algorithm.  This solves the match
    index problem by returning a list of indices where the pattern matches the
    text.

    Does cross-correlation solving the following equation:
    S_{i} = \sum_{j=1}^{m} (p_{j}^{3} t_{i+j-1} - 2p_{j}^{2}t_{i+j-1}^{2}
                              + p_{j}t_{i+j-1}^{3})
    This can be solved in Fourier space using FFT's of each of the three terms.

    S_{i} = 0 when there is a match between the pattern and text at that
    location.

    TODO: cite papers

    arguments:
      text: the text that you are interested in searching
      pattern: the pattern that may be contained in multiple locations inside
        the text
      n: the length of the text
      m: the length of the pattern
      indexOffset: offset to start from
    returns: a list containing the 0-based indices of matches of pattern in text
    '''

    #Note: len(rfft(something)) != len(something) for general case

    pattern = pattern[::-1]

    binary_encoded_text = string_to_binary_array(text)

    #TODO: for binary_encoded_text and pattern, if the char is equal to the
    # don't care character, then set the float value to 0.0
    text = binary_encoded_text
    text_sq = text * text
    text_cube = text_sq * text

    binary_encoded_pattern = string_to_binary_array(pattern,size=n)

    assert len(binary_encoded_text) == len(binary_encoded_pattern)

    pattern = binary_encoded_pattern
    pattern_sq = pattern * pattern
    pattern_cube = pattern_sq * pattern

    text_key = np.fft.rfft(text)
    text_sq_key = np.fft.rfft(text_sq)
    text_cube_key = np.fft.rfft(text_cube)

    pattern_key = np.fft.rfft(pattern)
    pattern_sq_key = np.fft.rfft(pattern_sq)
    pattern_cube_key = np.fft.rfft(pattern_cube)

    #there are three terms.  Since fft(key) is Linear, we will IFT each
    #individually
    out_term_1_key = pattern_cube_key * text_key
    out_term_2_key =  pattern_sq_key * text_sq_key
    out_term_3_key = pattern_key * text_cube_key

    out_term_1 = np.fft.irfft(out_term_1_key)
    out_term_2 = -2*np.fft.irfft(out_term_2_key)
    out_term_3 = np.fft.irfft(out_term_3_key)

    #TODO: may need to rotate this
    out = out_term_1 + out_term_2 + out_term_3

    #this should be 0 if match
    #TODO: figure out the difference between exact and inexact.
    #I think true matches where 0 and possible matches below this threshold
    matches = np.where(abs(out) < 1.0e-6)[0]

    #this is actually rotated based on the end of the string, so we need to
    #subtract m-i-1
    matches = np.subtract(matches, m-1)

    #since the FFT works on the unit circle, we can actually get matches that
    #start at the end of the string and end at the beginning.  This doesn't
    #make sense for DNA so we are going to remove all matches whose index
    #is less than 0.  These are the matches that span the end-start boundary
    return matches[matches >= 0]

def fft_match_index_n_log_n(text, pattern):
    '''Does the n log n FFT pattern matching algorithm.

    arguments:
      text: the text that you are interested in searching
      pattern: the pattern that may be contained in multiple locations inside
        the text
    returns: a list containing the 0-based indices of matches of pattern in text
    '''
    return fft_match_index(text, pattern, len(text), len(pattern))

def fft_match_index_n_log_m(text, pattern, chunk_size='m'):
    '''Does the n log m FFT pattern matching algorithm. If the length of the
    portion of the text that we're sampling is less than the length of the
    pattern, we pad the end with 0s. Change this if 0s are in the alphabet.

    Arguments
    ---------
      text: the text that you are interested in searching
      pattern: the pattern that may be contained in multiple locations inside
        the text
    chunk_size : type str or int
        if 'm', it will use the standard algorithm for the n log m algorithm,
            which breaks the string into 2m size chunks and performs the
            fft match index algorithm on those chunks
        if a positive integer, it will break up the string into size 
            2*chunk_size chunks

    returns: a list containing the 0-based indices of matches of pattern in text
    '''
    if not (chunk_size == 'm' or ((type(chunk_size) == int) and chunk_size>0)):
        raise Exception('fft_match_index_n_log_m chunk_size must be str or \
positive integer')
    n = len(text)
    m = len(pattern)

    if n == m:
       if text == pattern:
           return np.array([0])
       else:
           return np.array([])
    start = 0

    n_log_m_out = []

    if chunk_size == 'm':
        chunk_size = m

    while start < n-chunk_size:
        text_portion = text[:chunk_size*2].ljust(chunk_size*2,'0')
        index = fft_match_index(text_portion,pattern,chunk_size*2,chunk_size)
        for i in index:
            n_log_m_out.append(i+start)
        text = text[chunk_size:]
        start += chunk_size
    n_log_m_out = np.unique(np.asarray(n_log_m_out))
    return n_log_m_out

def fft_match_index_n_sq_log_n_naive(texts, pattern):
    '''Does the n_log_n match fft match index algorithm on k texts.

    The running time of this algorithm is k*n\log{n}

    arguments:
      text: a list of the texts that you are interested in searching
      pattern: the pattern that may be contained in multiple locations inside
        the text
    returns: a list containing the 0-based indices of matches of pattern in text

    '''
    return np.array([fft_match_index(i, pattern, len(i), len(pattern)) for i in texts])

def fft_match_index_n_sq_log_m(texts, pattern):
    '''Does the n log m FFT pattern matching algorithm on an array of text.

    arguments:
      texts: an array of the texts that you are interested in searching
      pattern: the pattern that may be contained in multiple locations inside
        the texts
    returns: an array of lists containing the 0-based indices of matches of the
        pattern in each text.
    '''
    return np.array([fft_match_index_n_log_m(i, pattern) for i in texts])

def fft_match_index_2d(texts, pattern):
    '''Does the n log n FFT pattern matching algorithm.  This solves the match
    index problem by returning a list of indices where the pattern matches the
    text.

    Does cross-correlation solving the following equation:
    S_{i} = \sum_{j=1}^{m} (p_{j}^{3} t_{i+j-1} - 2p_{j}^{2}t_{i+j-1}^{2}
                              + p_{j}t_{i+j-1}^{3})
    This can be solved in Fourier space using FFT's of each of the three terms.

    S_{i} = 0 when there is a match between the pattern and text at that
    location.

    TODO: cite papers

    arguments:
      text: the text that you are interested in searching
      pattern: the pattern that may be contained in multiple locations inside
        the text
      n: the length of the text
      m: the length of the pattern
      indexOffset: offset to start from
    returns: a list containing the 0-based indices of matches of pattern in text
    '''

    #Note: len(rfft(something)) != len(something) for general case

    pattern = pattern[::-1]

    binary_encoded_text = [string_to_binary_array(text) for text in texts]
    binary_encoded_text = np.array(binary_encoded_text)

    #TODO: for binary_encoded_text and pattern, if the char is equal to the
    # don't care character, then set the float value to 0.0
    text = binary_encoded_text
    text_sq = text * text
    text_cube = text_sq * text

    m = len(pattern)
    binary_encoded_pattern = np.zeros(binary_encoded_text.shape)
    binary_encoded_pattern[0,:] = string_to_binary_array(pattern,
                                        size=binary_encoded_text.shape[1])

    assert len(binary_encoded_text) == len(binary_encoded_pattern)

    pattern = binary_encoded_pattern
    pattern_sq = pattern * pattern
    pattern_cube = pattern_sq * pattern

    text_key = np.fft.rfft2(text)
    text_sq_key = np.fft.rfft2(text_sq)
    text_cube_key = np.fft.rfft2(text_cube)

    pattern_key = np.fft.rfft2(pattern)
    pattern_sq_key = np.fft.rfft2(pattern_sq)
    pattern_cube_key = np.fft.rfft2(pattern_cube)

    #there are three terms.  Since fft(key) is Linear, we will IFT each
    #individually
    out_term_1_key = pattern_cube_key * text_key
    out_term_2_key =  pattern_sq_key * text_sq_key
    out_term_3_key = pattern_key * text_cube_key

    out_term_1 = np.fft.irfft2(out_term_1_key)
    out_term_2 = -2*np.fft.irfft2(out_term_2_key)
    out_term_3 = np.fft.irfft2(out_term_3_key)

    #TODO: may need to rotate this
    out = out_term_1 + out_term_2 + out_term_3

    #this should be 0 if match
    matches = np.where(abs(out) < 1.0e-6)

    out = []
    #If our array is:
    # ACGTC
    # ACGTC
    # ACGTC
    # and the pattern is CAC, it will match unless we specifically prevent
    # it here.
    #Copies each matching row into a new array, and subtracts (m-1) to get
    # the correct index
    for i in range(text.shape[0]):
        temp = matches[1][np.where(matches[0] ==i)] - (m-1)
        out.append(temp[temp >= 0])
    matches = np.array(out)
    
    return matches

def fft_match_index_n_sq_log_n(texts, pattern):
    return fft_match_index_2d(texts, pattern)

if __name__ == '__main__':
    #f = open('1d.txt')
    #text = f.read().replace('\n', '')
    #pattern = 'ACG'
    #text = "ABCDABCDABCDABCD"
    #text = "AAABBACDDCDCBAADA"
    #pattern = 'DBB'

    #out = fft_match_index_n_log_m(text, pattern)
    #print out

    #print out, naive_string_match_index(text, pattern)
    #assert out == naive_string_match_index(text, pattern)

    texts = ["AAAB", "ABCD", "AAAB", "AAAB", "AAAB"]
    pattern = "AB"

    #print fft_match_index_2d(texts, pattern2)
    print fft_match_index_n_sq_log_n(texts, pattern)
