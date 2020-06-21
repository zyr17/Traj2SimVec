import os

files = os.listdir('test_results_dtw')
files = list(map(lambda x:'test_results_dtw/' + x, files))
files.sort()
for filename in files:
    last = map(float, open(filename).readlines()[-1].strip().split(' '))
    print(filename, ' '.join(map(str, last)))
