import os
import threading
import sys
import time
import random

threads = 1

if len(sys.argv) > 1:
    threads = int(sys.argv[1]) 

dataset = 'porto'
dis_type = 'dtw'
algo = 't2vec'
emb_folder = '../t2vec/porto_res/'
#emb_folder = '../learning_deep_representation/checkpoints/'
magic_num = 17295.77609804242

res_folder = 'result/%s/%s_%s/' % (algo, dataset, dis_type)
res_pkl = 'data/%s/dis_%s_test.pkl' % (dataset, dis_type)
if not os.path.exists(res_folder):
    os.makedirs(res_folder)

class mythread(threading.Thread):
    def __init__(self, number, emb_folder, res_folder, pkl, files, magic):
        super(mythread, self).__init__()
        self.number = number
        self.emb = emb_folder
        self.res = res_folder
        self.files = files
        self.pkl = pkl
        self.magic = magic
    def run(self):
        for file in self.files:
            cmd = 'CUDA_VISIBLE_DEVICES=%d python test.py %s%s %s %f > %s%s.txt' % (self.number % 4, self.emb, file, self.pkl, self.magic, self.res, file)
            print('thread %s:' % self.number, cmd)
            #time.sleep(random.random())
            os.system(cmd)


files = os.listdir(emb_folder)#[:10]
files.sort()

if threads > len(files):
    threads = len(files)

ths = []
for i in range(threads):
    ths.append(mythread(i, emb_folder, res_folder, res_pkl, files[i::threads], magic_num))
    ths[-1].start()

for th in ths:
    th.join()

print('main thread: end')
