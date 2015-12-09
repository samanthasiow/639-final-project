import cv2
import cv
import numpy as np
from fftmatch import string_to_binary_array, texts_to_array

def texts_to_array(texts):
    """
    Converts texts into an array of floats of their ascii representation

    Arguments
    ---------
    texts : list of str
        texts has k rows, and the maximum length string is length N

    Returns
    -------
    arr : numpy array
        k X N array with the float ascii representation of all of the texts
    """
    n = max(map(len, texts))
    out = np.ndarray((len(texts), n))
    for index, row in enumerate(texts):
        out[index,0:len(row)] = string_to_binary_array(row)

    return out.astype(np.float32)

def cv_match(texts_arr, pattern_arr, alg=cv2.TM_SQDIFF):
    """
    Performs the cv_match_index algorithm on numpy arrays

    Arguments
    ---------
    texts_arr : numpy array
        array of the ascii values of the gene strings
    pattern_arr : numpy array
        array of the pattern to search for in the gene strings

    Returns
    -------
    """
    matches = cv2.matchTemplate(texts_arr, pattern_arr, cv2.TM_SQDIFF)
    #matches = np.nonzero(abs(matches) < 1.0e-4)
    matches = np.where(abs(matches) < 1.0e-6)
    out = []
    for i in range(texts_arr.shape[0]):
        out.append(matches[1][np.where(matches[0] ==i)])

    return np.array(out)

def cv_match_index(texts, pattern):
    """
    This method uses Open CV's template matching algorithm to do substring
    matching inside of len(texts) genome strings for the specified pattern
    """

    texts = texts_to_array(texts)
    pattern = np.array([string_to_binary_array(pattern)])\
        .astype(np.float32)

    return cv_match(texts, pattern)

def cv_match_index_chunk(texts, pattern, chunk_size='m'):
    """
    Performs the cv_match_index algorithm on chunks that are 'chunk_size' long.
    If the length of the portion of the text that we're sampling is less than 
    the length of the pattern, we pad the end with 0s. Change this if 0s are in 
    the alphabet.


    Arguments
    ---------
    texts : list of str
        the genomic strings to search
    pattern : str 
        the pattern that may be contained in multiple locations inside the text
    chunk_size : type str or int
        if 'm', it will use the standard algorithm for the n log m algorithm,
            which breaks the string into 2m size chunks and performs the
            fft match index algorithm on those chunks
        if a positive integer, it will break up the string into size 
            2*chunk_size chunks

    returns: a list containing the 0-based indices of matches of pattern in text
    """
    if not (chunk_size == 'm' or ((type(chunk_size) == int) and chunk_size>0)):
        raise Exception('fft_match_index_n_log_m chunk_size must be str or \
positive integer')
    n = max(map(len, texts))

    m = len(pattern)

    texts = texts_to_array(texts)

    pattern = np.array([string_to_binary_array(pattern)])\
        .astype(np.float32)


    start = 0

    if chunk_size == 'm':
        chunk_size = m

    indices = []
    while start < n-chunk_size:
        index = cv_match(texts[:,start:start+chunk_size*2], pattern)
        for i in index:
            indices.append(i+start)
        start += chunk_size
    return np.array(indices)

def cv_match_index_gpu(texts, pattern):
    texts = texts_to_array(texts)
    pattern = cv.fromarray(texts_to_array(pattern))
    texts = cv.fromarray(texts)

if __name__ == '__main__':
    texts = ["ABCDABCDABCDABCD"]*4
    expected = np.array([[0,4,8,12]]*4)
    #print '\n'.join(texts)
    #out = cv_match_index(texts, "ABCD")
    #out = cv_match_index_gpu(texts, "ABCD")
    out = cv_match_index_chunk(texts, "ABCD")
    print out
    print expected
