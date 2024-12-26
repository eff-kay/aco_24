import pytest
import argparse
import os.path
import re

from support import timing

from multiprocessing import Pool


# increase recusion limit
import sys
sys.setrecursionlimit(100000000)
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from pprint import pprint

@timing()
def compute(data):
    inp = data.split('\n')[:-1]
    inp = inp[0]

    print(inp)
    fs = []
    j=0
    sub_fs= []
    for i in range(len(inp)):
        print('j',j)
        if i%2==0:
            for _ in range(int(inp[i])):
                fs.append(j)
                sub_fs+= f'{j}'
            j+=1
        else:
            for _ in range(int(inp[i])): 
                fs.append('.')

    # print(fs)
    print(len(fs), len(sub_fs))
    size = len(sub_fs)
    # fs = fs[:size]
    # find the first non '.' character
    for i in reversed(range(len(fs))):
        if fs[i]!='.':
            break

    j = 0
    new_fs = []
    while i>=j:
        if fs[j] == '.':
            new_fs.append(fs[i])
            i-=1
            while fs[i]=='.':
                i-=1
        else:
            new_fs.append(fs[j])
        j+=1
    
    print(new_fs)
    # print(list(map(int, list(new_fs))))
    # new_fs += '.'*(len(fs)-len(new_fs))

    # print(len(new_fs))
    # print(len(fs))
    run_sum = 0
    for i,n in enumerate(new_fs):
        if n=='.':
            break
        run_sum += i*int(n)

    # 022111222...... 
    ret = run_sum
    return ret


INPUT_S = '''\
2333133121414131402
'''


EXPECTED = 1928

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))