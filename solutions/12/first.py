import pytest
import argparse
import os.path
import re

from support import timing

from multiprocessing import Pool


from collections import deque
# increase recusion limit
import sys
sys.setrecursionlimit(100000000)
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from pprint import pprint

@timing()
def compute(data):
    inp = data.split('\n')[:-1]

    ret = 0
    heads = []

    def rules(inp_stone):

        # print('inp_stone', inp_stone)  
        if inp_stone == '0':
            return ['1']
        elif len(inp_stone)%2==0:
            left = int(inp_stone[:len(inp_stone)//2])
            right = int(inp_stone[len(inp_stone)//2:])

            return [str(left), str(right)]
        else:
            return [str(int(inp_stone)*2024)]
        
    inp = inp[0].split(' ')
    for i in range(75):
        new_inp = []
        for j in range(len(inp)):
            new_inp += rules(inp[j])

        inp = new_inp
        print('i', i, len(inp))
    
    ret = len(new_inp)
    return ret


INPUT_S = '''\
125 17
'''


EXPECTED = 55312

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