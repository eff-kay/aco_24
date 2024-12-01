import pytest
import argparse
import os.path

from collections import Counter

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split('\n')[:-1]
    inp = [list(map(int, x.split())) for x in inp]

    inp = list(zip(*inp))

    sim_list = []
    for x in inp[0]:
        count = Counter(inp[1])
        if x in count:
            sim_list.append(x*count[x])
        else:
            sim_list.append(0)
    
    print(sim_list)
    return sum(sim_list)

INPUT_S = '''\
3   4
4   3
2   5
1   3
3   9
3   3
'''

EXPECTED = 31

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