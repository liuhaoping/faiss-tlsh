import numpy as np


def convert_to_array(X):
    a = np.zeros( len(X) , dtype = int)

    for i in range(a.size):
        a[i] = int(X[i], 16)
    return a


def to_hist(t, length):
    buckets = np.zeros(length, dtype=np.int32)
    for idx, (sixteen, one) in enumerate(zip(t[0::2], t[1::2])):
        buckets[4 * idx] = (int(sixteen,16) & 0x0C) >> 2
        buckets[4 * idx + 1] = (int(sixteen,16) & 0x03)
        buckets[4 * idx + 2] = (int(one,16) & 0x0C) >> 2
        buckets[4 * idx + 3] = (int(one,16) & 0x03)
    return buckets

 
def transform_idx_to_label(df, I):
    label_list = []
    for i in range(len(I)):
        label_list.append( df.loc[ I[i:][0], 'signature'] )
    return np.array(label_list)

def evaluate(I, df, k, chcekLabels=False):  
    # https://github.com/facebookresearch/faiss/blob/master/benchs/bench_hnsw.py
    # def evaluate(index):
    #     ....
    
    size = len(df)

    missing_rate = (I == -1).sum() / float(k * size)
    recall_at_index  = sum(list(map(lambda x: x[0] in x[1], zip(np.array(df.index)[:], I))))  / float(size)
    print(" recall at index:  %.4f,  missing rate: %.4f" % (
            ( recall_at_index , missing_rate)))
    
    if chcekLabels:
        ILabels = transform_idx_to_label(df, I) 
        recall_at_label  = sum(list(map(lambda x: x[0] in x[1], zip(np.array(df.signature)[:], ILabels))))  / float(size)
        print(" recall at label:  %.4f" % (
                 recall_at_label))
    
    
import secrets
def gen_data(N, d):
    hash_list = []
    for i in range(N):
        hash = secrets.token_hex(int(d/2))
        hash_list.append(convert_to_array(hash))
    return np.array(hash_list).astype('float32')
      