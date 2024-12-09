import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data

    matches = []
    curr = ''
    digit_count = 0

    do_curr = ''
    dont_curr = ''
    enable_mul = True
    for ind, i in enumerate(inp):
        if i in 'do()':
            if i=='d' and do_curr == '':
                do_curr+=i
            
            if i=='o' and do_curr == 'd':
                do_curr+=i
            
            if i=='(' and do_curr == 'do':
                do_curr+=i
                continue
            
            if i==')' and do_curr == 'do(':
                do_curr = ''
                enable_mul = True
                continue

        if i in "don't()":
            if i=='d' and dont_curr == '':
                dont_curr+=i
                continue

            if i=='o' and dont_curr == 'd':
                dont_curr+=i
                continue

            if i=="n" and dont_curr == 'do':

                dont_curr+=i
                do_curr = ''
                continue

            if i=="'" and dont_curr == 'don':
                dont_curr+=i
                do_curr = ''
                continue


            if i=='t' and dont_curr == "don'":
                dont_curr+=i
                do_curr = ''
                continue

            if i=='(' and dont_curr == "don't":
                dont_curr+=i
                do_curr = ''
                continue

            if i==')' and dont_curr == "don't(":
                dont_curr=''
                do_curr = ''
                enable_mul = False
                continue
    
        do_curr =''
        dont_curr = ''
        if i=='m' or i=='u' or i=='l' or i=='(' or i==')' or i==',' or i.isdigit() and enable_mul:
            if i.isdigit():
                if digit_count > 0 and re.match(r'mul\(\d+', curr):
                    digit_count+=1
                    curr+=i
                    continue

                if digit_count >0 and re.match(r'mul\(\d+,\d+', curr):
                    curr+=i
                    digit_count+=1
                    continue

                if curr == 'mul(':
                    curr+=i
                    digit_count+=1
                    continue
                

                if re.match(r'mul\(\d+,', curr):
                    curr+=i
                    digit_count+=1  
                    continue

            else:
                digit_count = 0

            if i == 'm' and curr == '':
                curr+=i
                continue
            
            if i=='u' and curr == 'm':
                curr+=i
                continue
            
            if i=='l' and curr == 'mu':
                curr+=i
                continue

            if i=='(' and curr == 'mul':
                curr+=i
                continue
            
            if i==',' and re.match(r'mul\(\d+', curr):
                curr+=i
                continue
            
            if i==')' and re.match(r'mul\(\d+,\d+', curr):
                curr+=i
                matches.append(curr)
                curr = ''
                continue
        else:
            curr = ''
            digit_count = 0

    def compute(matches):
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
    ret = compute(matches)
    return ret

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