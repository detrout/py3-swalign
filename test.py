#from swalign import cswalign
from swalign import swalign
from swalign import cswalign
import numpy as np
import math
import string

import pstats, cProfile

import timeit
seq1 = 'HEAGAWGEE'
seq2 = 'PAWHEAE'

seq1 = b'SSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENL'

seq2 = b'SCAVPSTDDYAGKYGLQLDFQQNGTAKSVTCTYSPELNKLFCQLAKTCPLLVRVESPPPRGSILRATAVYKKSEHVAEVVKRCPHHERSVEPGEDAAPPSHLMRVEGNLQAYYMEDVNSGRHSVCVPYEGPQVGTECTTVLYNYMCNSSCMGGMNRRPILTIITLETPQGLLLGRRCFEVRVCACPGRDRRTEEDNY'

result1 = b'SSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSD-SDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEEN'
result2 = b'SCAVPSTDDYAGKYGLQLDFQQNGTAKSVTCTYSPELNKLFCQLAKTCPLLVRVESPPPRGSILRATAVYKKSEHVAEVVKRCPHHERSVEPGEDAAPPSHLMRVEGNLQAYYMEDVNSGRHSVCVPYEGPQVGTECTTVLYNYMCNSSCMGGMNRRPILTIITLETPQGLLLGRRCFEVRVCACPGRDRRTEEDN'

SIM = swalign.readBLOSUM50('blosum50.txt')
CSIM = cswalign.read_matrix('blosum50.txt')

def test_matrix():
    for pair in sim:
        pair_score = sim[pair]
        cscore = csim[ord(pair[0]), ord(pair[1])]
        assert pair_score == cscore

def test():
    pa1, pa2 = swalign.computeFMatrix(seq1, seq2, -10, CSIM)
    ca1, ca2 = cswalign.local_align(seq1, seq2, -10, CSIM)

    # is it right?
    assert ca1[0] == result1
    assert ca2[0] == result2
    # compare aligned
    assert pa1[0] == ca1[0]
    assert pa2[0] == ca2[0]
    # compare start
    assert pa1[1] == ca1[1]
    assert pa2[1] == ca2[1]
    # compare end
    assert pa1[2] == ca1[2]
    assert pa2[2] == ca2[2]


def time():
    setup = 'from __main__ import  swalign, cswalign, seq1, seq2, CSIM'
    cmds = { 'py': 'swalign.computeFMatrix(seq1, seq2, -10, CSIM)',
    'cy': 'cswalign.local_align(seq1, seq2, -10, CSIM)',
            }
    seconds = 5
    for name in cmds:
        t0 = timeit.timeit(cmds[name], setup,  number=1)
        count = int(math.ceil(seconds / (max(t0, .0000001) * 3)))
        print(name, t0, count)
        trial = timeit.repeat(cmds[name], setup, repeat=3, number=count)
        normalized_trial = [ t / count for t in trial ]
        print (name, normalized_trial)

        cProfile.runctx(cmds[name], globals(), locals(), name+'.prof')

    for name in cmds:
        print('-----', name, '-----')
        s = pstats.Stats(name + '.prof')
        s.strip_dirs().sort_stats('time').print_stats()

if __name__ == '__main__':
    test()
    time()
