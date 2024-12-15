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


    print(len(inp), len(inp[0])) 

    def turn_90(dir):
        if dir=="^":
            # block is to the top
            # go right
            return ">"
        
        elif dir=="v":
            # block is to the bottom
            # go left
            return "<"
        
        elif dir==">":
            # block is to the right
            # go down
            return "v"
        
        elif dir=="<":
            # block is to the left
            # go up
            return "^"


    for i, x in enumerate(inp):
        for j, y in enumerate(x):
            if y == "^":
                g_pos = (i, j)
                break
        
    print(g_pos, 'g_pos')


    # this takes a really long time
    def traverse(new_obs, pos, board, seen_cache, dir):

        if (pos[0], pos[1], dir) in seen_cache:
            return True, dir

        elif dir == "^":
            # go up
            new_pos = pos[0]-1, pos[1]
        
        elif dir == "v":
            # go down
            new_pos = pos[0]+1, pos[1]
        
        elif dir == "<":
            # go left
            new_pos = pos[0], pos[1]-1
        
        elif dir == ">":
            # go right
            new_pos = pos[0], pos[1]+1


        # print('cache', pos, dir)
        seen_cache.append((pos[0], pos[1], dir))        

        if new_pos[0]>=len(board) or new_pos[0]<0 or new_pos[1]>=len(board[0]) or new_pos[1]<0:
            return None

        elif board[new_pos[0]][new_pos[1]] == "#" or (new_pos[0] == new_obs[0] and new_pos[1] == new_obs[1]):
            dir = turn_90(dir)
            new_pos = pos[0], pos[1]

        ret = traverse(new_obs, new_pos, board, seen_cache=seen_cache, dir=dir)

        return ret

    result = 0


    for i, x in enumerate(inp):
        for j,y in enumerate(x):
            board = [list(x) for x in inp]
            new_obs = (i, j)
            print(i,j, result)
            loop = traverse(new_obs, g_pos, board, seen_cache=list(), dir="^")

            if loop and loop[0]:
                result+=1

    # result = 0
    # for i in range(len(inp)):
    #     for j in range(len(inp[0])):
    #         r, c = g_pos[0], g_pos[1]
    #         dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    #         d = 0

    #         seen_cache = set() 
    #         while True:
    #             if (r,c,d) in seen_cache:
    #                 result+=1
    #                 break

    #             seen_cache.add((r,c,d))

    #             dr, dc = dir[d]

    #             rr = r + dr
    #             cc = c + dc

    #             if not (0 <= rr < len(inp) and 0 <= cc < len(inp[0])):
    #                 break

    #             if inp[rr][cc] == '#' or rr==i and cc==j:
    #                 d = (d+1)%4
    #             else:
    #                 r = rr
    #                 c = cc

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

EXPECTED = 6

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