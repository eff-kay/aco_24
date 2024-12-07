
import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split('\n')[:-1]
    inp = [list(map(int, x.split())) for x in inp]

    safe_count = 0

    for row in inp:
        def check_row_safe(row):    
            trend = None
            prev = row[0]
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
                    trend = 'pos' if diff > 0 else 'neg' if diff < 0 else trend
                    if diff == 0:
                        trend_continue = True

                prev = curr
                if 1<=adiff<=3:
                    pass
                else:
                    break
                
                if trend_continue:
                    pass
                else:
                    break
            
            if i == len(row)-1 and trend_continue and 1<= adiff <= 3:
                return True
            else:
                return False

        if check_row_safe(row):
            safe_count += 1
            continue

        good1 = False
        good2 = False
        for j in range(len(row)-1):
            if 1<= row[j+1] - row[j] <= 3:
                continue
            else:
                if check_row_safe(row[:j] + row[j+1:]) or check_row_safe(row[:j+1] + row[j+2:]):
                    good1 = True
                    break
        
        row = list(reversed(row))

        for j in range(len(row)-1):
            if 1<= row[j+1] - row[j] <= 3:
                continue
            else:
                if check_row_safe(row[:j] + row[j+1:]) or check_row_safe(row[:j+1] + row[j+2:]):
                    good2 = True
                    break
        
        if good1 or good2:
            safe_count += 1
            
    return safe_count

INPUT_S = '''\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
1 1 2 3 4
2 5 4 3 2
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