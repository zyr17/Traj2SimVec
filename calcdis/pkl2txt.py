import pickle
import sys

filename = sys.argv[1]
dest = filename[:-3] + 'txt'

a = pickle.load(open(filename, 'rb'))
open(dest, 'w').write('%d\n' % len(a) + '\n'.join([' '.join(['%.10f' % y for y in x]) for x in a]))
