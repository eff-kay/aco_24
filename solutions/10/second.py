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
from collections import defaultdict
@timing()
def compute(data):
    inp = data.split('\n')[:-1]

    print("inp", inp, len(inp), len(inp[0]))

    ret = 0
    heads = []

    for i in range(len(inp)):
        for j in range(len(inp[i])):
            if inp[i][j] == '0':
                heads.append((i, j))

    print('heads', len(heads))

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    trail_reached = defaultdict(int)
    total_trails = 0
    for head in heads:
        print('trying head', head)                    
        route_count = 0
        queue = deque([head])

        while queue:
            i, j = queue.popleft()
            # print('path', i, j, route_count, inp[i][j])
            c_val = inp[i][j]

            if inp[i][j] == '0':
                start_head = (i, j)

            for n_diff in neighbors:
                ni, nj = n_diff
                ni += i
                nj += j

                if ni < 0 or ni >= len(inp) or nj < 0 or nj >= len(inp[0]):
                    continue
                    
                if inp[ni][nj] == '.':
                    continue

                if inp[ni][nj] == '9' and int(inp[ni][nj]) - int(c_val) == 1:
                    # si, sj = start_head
                    route_count += 1
                    # print("end reached", ni, nj, route_count)
                    continue

                if int(inp[ni][nj]) - int(c_val) == 1:
                    queue.append((ni, nj))

        print("route_count", route_count)
        total_trails += route_count
    ret = total_trails
    return ret


INPUT_S = '''\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
'''


INPUT_S = '''\
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
'''



INPUT_S = '''\
012345
123456
234567
345678
4.6789
56789.
'''

# INPUT_S = '''\
# 10..9..
# 2...8..
# 3...7..
# 4567654
# ...8..3
# ...9..2
# .....01
# '''

INPUT_S = '''\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''


EXPECTED = 81

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