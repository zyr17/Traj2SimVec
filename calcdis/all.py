import os
import sys

dataset = 'porto'
algo = 't2vec_new'
dis = 'frechet'

mat = 'dis/%s/%s.txt' % (dataset, dis)

embfolder = 'data/%s/%s/' % (dataset, algo)

files = os.listdir(embfolder)
files.sort()

resultfolder = 'result/%s/%s_%s/' % (algo, dataset, dis)
if not os.path.exists(resultfolder):
    os.mkdir(resultfolder)

if len(sys.argv) == 2:
    files = files[:int(sys.argv[1])]
if len(sys.argv) == 3:
    files = files[int(sys.argv[1]):int(sys.argv[2])]

for file in files:
    cmd = './test %s %s%s %s%s > %s%s' % (mat, embfolder, file, embfolder, file, resultfolder, file)
    print(cmd)
    os.system(cmd)
