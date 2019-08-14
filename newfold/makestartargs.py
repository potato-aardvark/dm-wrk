import sys

start = float(sys.argv[1])
p0 = 0.714519699726
numatonce = 1
try:
    startargsname = sys.argv[2]
except IndexError:
    startargsname = 'startargs'

f = open(startargsname, 'w')
for i in range(10000000):
    curr = start + p0 * numatonce * i
    f.write(f'{curr}\n')
