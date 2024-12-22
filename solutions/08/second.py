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

    print(len(inp), len(inp[0]))

    ret = 0

    seen = {}

    # for inp in inps:
    for i, x in enumerate(inp):
        for j, y in enumerate(x):
            if y != '.' and y!='#':
                an = y

                if an not in seen:
                    seen[an] = [(i,j)]
                else:
                    seen[an].append((i,j))
                
    # pprint(seen)

    antinodes = set()
    for an, locs in list(seen.items()):
        for i in range(len(locs)):
            for j in range(i+1, len(locs)):
                # print(i, locs[i], j, locs[j])
                an1, an2 = locs[i], locs[j]
                an0 = tuple(x-y for x,y in zip(an1, an2))
                an0 = tuple(x+y for x,y in zip(an0, an1))

                x,y = an0
                while 0<=x<len(inp) and 0<=y<len(inp[0]):
                    antinodes.add((an0))
                    
                    an2 = an1
                    an1 = an0
                    an0 = tuple(x-y for x,y in zip(an1, an2))
                    an0 = tuple(x+y for x,y in zip(an0, an1))

                    x,y = an0

                an1, an2 = locs[i], locs[j] 
                an3 = tuple(x-y for x,y in zip(an2, an1))
                an3 = tuple(x+y for x,y in zip(an2, an3))

                x,y = an3
                while 0<=x<len(inp) and 0<=y<len(inp[0]):
                    # print('an3', an3)
                    antinodes.add((an3))

                    an1 = an2
                    an2 = an3
                    an3 = tuple(x-y for x,y in zip(an2, an1))
                    an3 = tuple(x+y for x,y in zip(an2, an3))

                    x,y = an3
    for i, locs in list(seen.items()):
        for j in locs:
            antinodes.add(j)
    # pprint(antinodes)
    ret = len(antinodes)
    # print(seen)
    return ret


INPUT_S = '''\
##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
'''

EXPECTED = 34

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