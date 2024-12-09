import pytest
import argparse
import os.path
import re

# increase recusion limit
import sys
sys.setrecursionlimit(100000000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split('\n')[:-1]
    ROW = len(inp)
    COL = len(ROW[0])

    def search_patterns(G, R, C, r=0, c=0, ans=0):
        # Base case: if we've reached the end of the grid
        if r >= R:
            return ans
        
        # If we've reached the end of a row, move to next row
        if c >= C:
            return search_patterns(G, R, C, r + 1, 0, ans)

        current_ans = 0
        
        # Check horizontal XMAS
        if c+3 < C and G[r][c] == 'X' and G[r][c+1] == 'M' and G[r][c+2] == 'A' and G[r][c+3] == 'S':
            current_ans += 1
        
        # Check vertical XMAS
        if r+3 < R and G[r][c] == 'X' and G[r+1][c] == 'M' and G[r+2][c] == 'A' and G[r+3][c] == 'S':
            current_ans += 1
        
        # Check diagonal XMAS
        if r+3 < R and c+3 < C and G[r][c] == 'X' and G[r+1][c+1] == 'M' and G[r+2][c+2] == 'A' and G[r+3][c+3] == 'S':
            current_ans += 1
        
        # Check horizontal SAMX
        if c+3 < C and G[r][c] == 'S' and G[r][c+1] == 'A' and G[r][c+2] == 'M' and G[r][c+3] == 'X':
            current_ans += 1
        
        # Check vertical SAMX
        if r+3 < R and G[r][c] == 'S' and G[r+1][c] == 'A' and G[r+2][c] == 'M' and G[r+3][c] == 'X':
            current_ans += 1
        
        # Check diagonal SAMX
        if r+3 < R and c+3 < C and G[r][c] == 'S' and G[r+1][c+1] == 'A' and G[r+2][c+2] == 'M' and G[r+3][c+3] == 'X':
            current_ans += 1
        
        # Check diagonal up SAMX
        if r-3 >= 0 and c+3 < C and G[r][c] == 'S' and G[r-1][c+1] == 'A' and G[r-2][c+2] == 'M' and G[r-3][c+3] == 'X':
            current_ans += 1
        
        # Check diagonal up XMAS
        if r-3 >= 0 and c+3 < C and G[r][c] == 'X' and G[r-1][c+1] == 'M' and G[r-2][c+2] == 'A' and G[r-3][c+3] == 'S':
            current_ans += 1
        
        # Recursive call for next position
        return search_patterns(G, R, C, r, c + 1, ans + current_ans)

    result = search_patterns(data, ROW, COL)
    print(result)

    return result

INPUT_S = '''\
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
'''

EXPECTED = 18

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