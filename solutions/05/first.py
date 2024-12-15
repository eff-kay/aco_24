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

    def fetch_befores(number):
        befores = []
        for order in orders:
            if order[1] == number:
                befores.append(order[0])
        
        return befores

    def fetch_afters(number):
        afters = []
        for order in orders:
            if order[0] == number:
                afters.append(order[1])
        
        return afters

    valid_order = []
    for update in updates:
        valid = True
        for i, page in enumerate(update):
            befores = fetch_befores(page) 
            afters = fetch_afters(page)

            rest = update[i+1:]
            for r in rest:
                if r in befores:
                    valid = False
                    # this should appear before page
                    break
                    
            if not valid:
                break
                
            prev = updates[:i]

            for p in prev:
                if p in afters:
                    valid = False
                    # this should appear after page
                    break
            
            if not valid:
                break

        if valid:
            valid_order.append(update)


    result = sum([valid[len(valid)//2] for valid in valid_order])
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

EXPECTED = 143

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