import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split('\n')[:-1]
    inp = [list(map(int, x.split())) for x in inp]

    safe_count = 0

    for row in inp:
        prev = row[0]
        trend = None
        for i in range(1, len(row)):
            curr = row[i]

            diff = curr - prev
            adiff = abs(diff)

            if trend is None:
                # set the trend for the first time
                trend = 'pos' if diff > 0 else 'neg' if diff < 0 else None

            if trend == 'pos' and diff > 0:
                trend_continue = True
            elif trend == 'neg' and diff < 0:
                trend_continue = True 
            else:
                trend_continue = False

            prev = curr
            if 1<=adiff<=3 and trend_continue:
                continue
            else:
                # print('diff', diff, 'trend', trend, 'trend_continue', trend_continue)
                break
        
        # print('row', row, i, len(row)-1)
        if i == len(row)-1 and trend_continue and 1<= adiff <= 3:
            # print('safe is', row)
            safe_count += 1

    return safe_count

INPUT_S = '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''

EXPECTED = 2

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