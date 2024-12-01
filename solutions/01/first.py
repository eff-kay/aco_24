import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split('\n')[:-1]
    inp = [list(map(int, x.split())) for x in inp]
    inp  = list(zip(*inp))
    inp = [sorted(x) for x in inp]
    inp = [abs(x[0] - x[1]) for x in zip(*inp)]
    return sum(inp)

INPUT_S = '''\
3   4
4   3
2   5
1   3
3   9
3   3'''

EXPECTED = 11

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