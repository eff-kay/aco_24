import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data
    matches = re.findall(r'mul\(\d+,\d+\)', inp, re.MULTILINE|re.DOTALL)
    print(len(matches))
    define_mul = 'def mul(a,b): return a*b'
    context = {}
    exec(define_mul, context)
    ret = 0
    for match in matches:
        match = 'val = '+match
        exec(match, context)
        val = context['val']
        ret+=val

    return ret

INPUT_S = '''\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''

EXPECTED = 161

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