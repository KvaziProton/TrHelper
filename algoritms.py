def alg_first_imp(seq_0):
    seq = sorted(seq_0)
    for (i, x) in enumerate(seq):
        if x > i:
            return x-1


seq_0 = [18, 4, 8, 9, 16, 1, 14, 7, 19, 3, 0, 5, 2, 11, 6]
#print(alg_first_imp(seq))






def div_and_con(seq_0):
    seq_0 = sorted(seq_0)
    seq = list(enumerate(seq_0))
    div = len(seq) // 2
    while len(seq) > 1:
        if seq[div][1] > seq[div][0]:
            seq = seq[:div]
        else:
            seq = seq[div:]
    return seq_0[seq[0][1]] + 1

print(div_and_con(seq_0))
