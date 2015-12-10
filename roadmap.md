# 639-final-project
EN 600.639: Final Project with Samantha Siow, Michael Norris, Aaron Lerner, and Isac Lee

[ ] October 29th - One-page project proposal due


## Michael's Roadmap
This is an attempt to validate the potential for my ideas as a project topic.

I think we can implement a O(nk log(n)) time algorithm for substring matching
with k unique DNA sequences of length n.  This is pretty technical, but it
amounts to running a simple image processing algorithm on a binary encoding of
the DNA sequences.

1-D matching (a single DNA sequence and a single template) can be done in 
O(n log m) time, which has been proven in Clifford's paper.  2-D matching 
(searching for a substring across multiple DNA sequences) uses the same theory 
and may not have been done before.  2-D matching will probably be O(nk log m)
time, where there are k DNA sequences of length n, and there's a single template
of length m

http://nar.oxfordjournals.org/content/10/1/133.short

http://bioinformatics.oxfordjournals.org/content/7/2/143.short

http://nar.oxfordjournals.org/content/30/14/3059.short

http://www.sciencedirect.com/science/article/pii/S002001900600250X

http://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TM-041.pdf

http://www.ncbi.nlm.nih.gov/pmc/articles/PMC326121/

http://dl.acm.org/citation.cfm?id=37191

http://www.ncbi.nlm.nih.gov/pmc/articles/PMC330830/

http://nar.oxfordjournals.org/content/18/21/6305.abstract

http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.123.1883

http://dl.acm.org/citation.cfm?id=1222507

Clifford's Paper http://www.cs.bris.ac.uk/Publications/Papers/2000602.pdf

[Best description of the 1D algorithm](http://stringpedia.bsmithers.co.uk/index.php?title=FFT_Algorithm_For_Solving_Exact_Pattern_Matching_With_Don%27t_Cares)

[ ] Find a sweet dataset or create fake testing dataset

1-D matching amounts to solving the match-index problem for a single DNA
sequence.

[x] Binary encode DNA strings into 1-D array (30 minutes)

[x] Do FFT's on the arrays, correlate with the template, and combine to create
the array with the indices (2-5 hours)

[ ] Make cool looking graphics showing matches for paper and presentation.

2-D matching amounts to solving the match-index problem for k DNA sequences and
a single template t
[ ] Binary encode DNA strings into 2-D arrays (30 minutes)

[ ] Use OpenCV's template matching algorithm

 [ ] Work out the math to determine how to combine the nucleotide arrays to get
     the same arrays for the 1-D case
 
 [ ] Figure out the approximate specificity of the filter based on the fact
     that we will have to threshold the matches to some level.  Tweak. Rinse
     repeat.
 

[ ] make a cool looking heat map for the locations of matches

[ ] Do the same thing as the previous step, but without OpenCV's template
    matching (simple, just use 2-D fft and do explicit cross-correlation between
    the text and the template)
