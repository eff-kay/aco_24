import pytest
import argparse
import os.path
import re

import sys
# limit
sys.setrecursionlimit(100000000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data
    matches = re.findall(r'mul\(\d+,\d+\)', inp, re.MULTILINE|re.DOTALL)
    define_mul = 'def mul(a,b): return a*b'
    context = {}
    exec(define_mul, context)
    ret = 0
    for match in matches:
        match = 'val = '+match
        exec(match, context)
        val = context['val']
        ret+=val

    G = data.split('\n')[:-1]
    R = len(G)
    C = len(G[0])
    ans=0
    p2 =0


    def search_patterns(G, R, C, r=0, c=0, p2=0):
        # Base case: if we've reached the end of the grid
        if r >= R:
            return p2
        
        # If we've reached the end of a row, move to next row
        if c >= C:
            return search_patterns(G, R, C, r + 1, 0, p2)
        
        # Check special patterns for p2
        if r+2 < R and c+2 < C:
            # Pattern 1
            if G[r][c]=='M' and G[r+1][c+1]=='A' and G[r+2][c+2]=='S' and G[r+2][c]=='M' and G[r][c+2]=='S':
                p2 += 1
            # Pattern 2
            if G[r][c]=='M' and G[r+1][c+1]=='A' and G[r+2][c+2]=='S' and G[r+2][c]=='S' and G[r][c+2]=='M':
                p2 += 1
            # Pattern 3
            if G[r][c]=='S' and G[r+1][c+1]=='A' and G[r+2][c+2]=='M' and G[r+2][c]=='M' and G[r][c+2]=='S':
                p2 += 1
            # Pattern 4
            if G[r][c]=='S' and G[r+1][c+1]=='A' and G[r+2][c+2]=='M' and G[r+2][c]=='S' and G[r][c+2]=='M':
                p2 += 1
        
        # Recursive call for next position
        return search_patterns(G, R, C, r, c + 1, p2)

    def solve(data):
        G = data.split('\n')[:-1]
        R = len(G)
        C = len(G[0])
        p2 = search_patterns(G, R, C)
        return p2

    # Example usage:
    p2 = solve(data)

    return p2

INPUT_S = '''\
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
'''

EXPECTED = 9

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