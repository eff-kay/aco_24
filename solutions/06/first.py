import pytest
import argparse
import os.path
import re

from support import timing
# increase recusion limit
import sys
sys.setrecursionlimit(100000000)
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

@timing()
def compute(data):
    inp = data.split('\n')[:-1]


    print(len(inp), len(inp[0])) 

    def turn_90(g_pos, b_pos):
        diff = b_pos[0]-g_pos[0], b_pos[1]-g_pos[1]

        if diff == (-1, 0):
            # block is to the top
            # go right
            return 0, 1
        
        elif diff == (1, 0):
            # block is to the bottom
            # go left
            return 0, -1
        
        elif diff == (0, 1):
            # block is to the right
            # go down
            return 1, 0
        
        elif diff == (0, -1):
            # block is to the left
            # go up
            return -1, 0


    for i, x in enumerate(inp):
        for j, y in enumerate(x):
            if y == "^":
                g_pos = (i, j)
                break
        
    print(g_pos, 'g_pos')


    def traverse(pos, board, old_pos):
        # print(pos, )
        # for x in board:
        #     print(x)

        if pos[0]>=len(board) or pos[0]<0 or pos[1]>=len(board[0]) or pos[1]<0:
            return 
        
        elif board[pos[0]][pos[1]] == "#":
            g_pos = old_pos
            b_pos = pos
            new_diff = turn_90(g_pos, b_pos)
            new_pos = g_pos[0]+new_diff[0], g_pos[1]+new_diff[1]
            return traverse(new_pos, board, g_pos)
        
        elif board[pos[0]][pos[1]] == "^":
            # go up
            new_pos = pos[0]-1, pos[1]
        
        elif board[pos[0]][pos[1]] == "v":
            # go down
            new_pos = pos[0]+1, pos[1]
        
        elif board[pos[0]][pos[1]] == "<":
            # go left
            new_pos = pos[0], pos[1]-1
        
        elif board[pos[0]][pos[1]] == ">":
            # go right
            new_pos = pos[0], pos[1]+1

        else:
            diff = pos[0]-old_pos[0], pos[1]-old_pos[1]
            new_pos = pos[0]+diff[0], pos[1]+diff[1]

        board[pos[0]][pos[1]] = "X"
        return traverse(new_pos, board, pos)

    board = [list(x) for x in inp]
    result = traverse(g_pos, board, (0,0))

    # print
    result = 0
    for x in board:
        # print(''.join(x))
        for y in x:
            if y=="X":
                result+=1


    print(result)

    return result


@timing()
def compute_bfs(data):
    inp = data.split('\n')[:-1]
    for i, x in enumerate(inp):
        for j, y in enumerate(x):
            if y == "^":
                g_pos = (i, j)
                break


    result = 0
    r, c = g_pos[0], g_pos[1]
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    d = 0

    seen_cache = set() 

    while True:
        seen_cache.add((r,c))

        dr, dc = dir[d]

        rr = r + dr
        cc = c + dc

        if not (0 <= rr < len(inp) and 0 <= cc < len(inp[0])):
            result = len(seen_cache)
            break

        if inp[rr][cc] == '#':
            d = (d+1)%4
        else:
            r = rr
            c = cc

    print(result)

    return result



INPUT_S = '''\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''

EXPECTED = 41

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
    
    with open(args.data_file) as f:
        print(compute_bfs(f.read()))
