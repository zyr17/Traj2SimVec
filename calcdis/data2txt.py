import pickle
import h5py
import os
import sys
import torch

def getfile(filename):
    if filename[-3:] == '.h5':
        a = h5py.File(filename, 'r')
        b = a['layer3']
    elif filename[-3:] == '.pt':
        pt = torch.load(filename)
        if 'test_result' in pt.keys():
            b = pt['test_result']
    c = ['%d' % len(b)]
    for i in b:
        c.append(' '.join(list(['%.12f' % x for x in i])))
    return '\n'.join(c)

src = sys.argv[1]
dest = sys.argv[2]
files = os.listdir(src)
files.sort()

if not os.path.exists(dest):
    os.makedirs(dest)

for file in files:
    print(file)
    s = getfile(src + '/' + file)
    open(dest + '/' + file + '.txt', 'w').write(s)
