SMS_FILENAME = 'data/sms/sms.txt'
MADURAI_FILENAME = 'data/madurai/sample.txt'
KERNEL_FILENAME = 'data/linux/linux_kernel_3Maa'
PAULG_FILENAME = 'data/paulg/paulg.txt'
JHS_FILENAME = 'data/jhs/jhs.txt'
JHS_PATH = 'data/jhs'

MADURAI_PATH = 'data/madurai/'
SMS_PATH = 'data/sms/'
KERNEL_PATH = 'data/linux/'
PAULG_PATH = 'data/paulg/'



import csv
import numpy as np
import pickle as pkl

import sys




def read_lines_sms(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return [ row[-1] for row in list(reader) ]

def read_lines(filename):
    with open(filename, encoding='UTF=8') as f:
        #print(f.read())
        return f.read().split('\n')

def index_(lines):
    #lines2 = [line.encode('utf-8') for line in lines]
    #print(lines2)

    # set object 를 만들어라. 중복을 허용하지 않는다.
    # '\n'.join() 은 lines라는 리스트를 사이사이에 '\n\'을 넣어 문자열로 변환해준다

    temp = '\n'.join(lines)  # string 이다.  unicode 는 string
    #temp = '\n'.join(lines).encode('utf-8') # byte로 encoding 된 것이다
    print(type(temp))

    tempset = set('\n'.join(lines).encode('utf-8'))
    print(type(tempset))

    vocab = list(set('\n'.join(lines)))

    vocab2 = list(set('\n'.join(lines).encode('utf-8')))
    print(vocab2)

    ch2idx = { k:v for v,k in enumerate(vocab) }

    # for print
    temp_ch2idx = {k.encode('utf-8'): v for v, k in enumerate(vocab)}
    print(temp_ch2idx)
    print(type(ch2idx))
    return vocab, ch2idx

def to_array(lines, seqlen, ch2idx):
    # combine into one string
    raw_data = '\n'.join(lines)
    num_chars = len(raw_data)
    # calc data_len
    data_len = num_chars//seqlen
    # create numpy arrays
    X = np.zeros([data_len, seqlen])
    Y = np.zeros([data_len, seqlen])
    # fill in
    for i in range(0, data_len):
        X[i] = np.array([ ch2idx[ch] for ch in raw_data[i*seqlen:(i+1)*seqlen] ])
        Y[i] = np.array([ ch2idx[ch] for ch in raw_data[(i*seqlen) + 1 : ((i+1)*seqlen) + 1] ])
    # return ndarrays
    return X.astype(np.int32), Y.astype(np.int32)

def process_data(path, filename, seqlen=20):
    lines = read_lines(filename)
    print(type(lines), len(lines))
    idx2ch, ch2idx = index_(lines)
    X, Y = to_array(lines, seqlen, ch2idx)
    np.save(path+ 'idx_x.npy', X)
    np.save(path+ 'idx_y.npy', Y)
    with open(path+ 'metadata.pkl', 'wb') as f:
        pkl.dump( {'idx2ch' : idx2ch, 'ch2idx' : ch2idx }, f )

def test():
    a = ["hello my name is", "jhs. nice to meet you", "have a good day"]
    b = '\n'.join(a)
    c = set(b)
    d = list(c)
    print(a)
    print(b)
    print(c)
    print(d)

if __name__ == '__main__':
    print(sys.stdout.encoding)
    process_data(path = JHS_PATH,
            filename = JHS_FILENAME)
    #test()

'''
if __name__ == '__main__':
    process_data(path = PAULG_PATH,
            filename = PAULG_FILENAME)
'''



def load_data(path):
    # read data control dictionaries
    with open(path + 'metadata.pkl', 'rb') as f:
        metadata = pkl.load(f)
    # read numpy arrays
    X = np.load(path + 'idx_x.npy')
    Y = np.load(path + 'idx_y.npy')
    return X, Y, metadata['idx2ch'], metadata['ch2idx']


def test():
    a = ["hello my name is", "jhs. nice to meet you", "have a good day"]
    b = '\n'.join(a)
    c = set(b)
    d = list(c)
    print(a)
    print(b)
    print(c)
    print(d)