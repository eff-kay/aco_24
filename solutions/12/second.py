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

#import cache
from functools import lru_cache

@timing()
def compute(data):
    inp = data.split('\n')[:-1]

    ret = 0
    heads = []

    def rules(inp_stone, counts):

        # print('inp_stone', inp_stone)  
        if inp_stone == '0':
            counts[0]+=1
            return ['1'], counts 
        elif len(inp_stone)%2==0:
            counts[1]+=1
            left = int(inp_stone[:len(inp_stone)//2])
            right = int(inp_stone[len(inp_stone)//2:])

            return [str(left), str(right)], counts
        else:
            counts[2]+=1
            return [str(int(inp_stone)*2024)], counts
        
    inp = inp[0].split(' ')
    for i in range(25):
        new_inp = []
        counts = [0,0,0]
        for j in range(len(inp)):
            rets, counts = rules(inp[j], counts)
            new_inp += rets
            counts = counts
        
        print('i', i+1, len(new_inp), counts)
        ret = len(new_inp)
        inp = new_inp
        # ret = counts[0] + (counts[1]*2) + counts[2]

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