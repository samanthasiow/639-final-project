import cv2
import numpy as np
from fftmatch import string_to_binary_array

def cv_match_index(texts, pattern):
    """
    This method uses Open CV's template matching algorithm to do substring
    matching inside of len(texts) genome strings for the specified pattern
    """

    texts = np.array([string_to_binary_array(i) for i in texts])\
        .astype(np.float32)
    template = np.array([string_to_binary_array(pattern)])\
        .astype(np.float32)

    matches = cv2.matchTemplate(texts, template, cv2.TM_SQDIFF)
    #matches = np.nonzero(abs(matches) < 1.0e-4)
    matches = np.where(abs(matches) < 1.0e-6)
    out = []
    for i in range(texts.shape[0]):
        out.append(matches[1][np.where(matches[0] ==i)])

    return np.array(out)

#texts = ["ABCDABCDABCDABCD"]*4
#expected = np.array([[0,4,8,12]]*4)
#print '\n'.join(texts)
#out = cv_match_index(texts, "ABCD")
#print out
#print expected
