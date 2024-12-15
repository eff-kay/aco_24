import pytest
import argparse
import os.path
import re

# increase recusion limit
import sys
sys.setrecursionlimit(100000000)

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    orders, updates = data.split('\n\n')

    orders  = [list(map(int, x.split('|'))) for x in orders.split('\n')]
    updates = [list(map(int, x.split(','))) for x in updates.split('\n')[:-1]]

    # create a grid of before and afters based on the oder
    grid = {}
    for order in orders:
        if order[0] not in grid:
            grid[order[0]] = []
        grid[order[0]].append(order[1])
    
    list_ordered_pages = []
    for invalid in invalid_order:
        ordered_pages = list(invalid)
        for i in range(len(ordered_pages)):
            min = ordered_pages[i]
            for key,value in grid.items():
                if key in ordered_pages:
                    if min in value and key not in ordered_pages[:i]:
                        # swap
                        min = key

            ch_index = ordered_pages.index(min)
            ordered_pages[i], ordered_pages[ch_index] = min, ordered_pages[i]

        list_ordered_pages.append(ordered_pages)

    print(list_ordered_pages)
    result = sum([valid[len(valid)//2] for valid in list_ordered_pages])
    return result

INPUT_S = '''\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

EXPECTED = 123

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