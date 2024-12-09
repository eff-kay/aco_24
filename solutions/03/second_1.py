import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    enable_mul = True
    run_sum = 0
    for i,_ in enumerate(data):
        if data[i:i+len('do()')] == 'do()':
            enable_mul = True
        
        elif data[i:i+len("don't()")] == "don't()":
            enable_mul = False
        
        elif enable_mul:
            prod = re.match(r'mul\((\d+),(\d+)\)', data[i:])
            if prod:
                run_sum += int(prod.group(1))*int(prod.group(2))

    return run_sum 

INPUT_S = '''\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''

EXPECTED = 48

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