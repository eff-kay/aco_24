import pytest
import argparse
import os.path
import re

from multiprocessing import Pool
from support import timing
# increase recusion limit
import sys
sys.setrecursionlimit(100000000)
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from pprint import pprint

@timing()
def compute(data):
    inp = data.split('\n')[:-1]

    print(len(inp))
    ops = ['+', '*', '||']

    inps = [x.split(': ') for x in inp]
    inps = [[int(x[0]), list(map(int, x[1].split()))] for x in inps]

    print(len(inps))
    ret = []
    for i, inp in enumerate(inps):
        print('inp', i)
        exp_res = inp[0]
        nums = inp[1]

        run_sum = 0

        poss = len(nums)-1

        combinations = []

        def calc_comb(ind, comb, combinations):
            if ind == poss:
                combinations.append(comb)
                return combinations

            for i in range(len(ops)):
                new_comb = comb.copy()
                new_comb.append(ops[i])
                combinations = calc_comb(ind+1, new_comb, combinations)
            return combinations

        combinations = calc_comb(0, [], combinations)

        for comb in combinations:
            # print('res', nums[0], comb[0], nums[1])
            if comb[0] == '||':
                run_sum = int(f'{nums[0]}{nums[1]}')
            else:
                run_sum = eval(f'{nums[0]}{comb[0]}{nums[1]}')
            ci = 1
            for n in range(2, len(nums)):
                if comb[ci] == '||':
                    run_sum = int(f'{run_sum}{nums[n]}')
                    ci+=1
                    if run_sum>exp_res:
                        break
                    continue
                # print('res', run_sum, comb[ci], nums[n])
                run_sum = eval(f'{run_sum}{comb[ci]}{nums[n]}')
                ci+=1
                if run_sum>exp_res:
                    break
            # print('run_sum', run_sum) 
            if run_sum == exp_res:
                ret.append(run_sum)
                break
        
    print('ret', ret)
    return sum(ret)



@timing()
def compute_optimized(data):
    inp = data.split('\n')[:-1]

    print(len(inp))
    ops = ['+', '*', '||']

    inps = [x.split(': ') for x in inp]
    inps = [[int(x[0]), list(map(int, x[1].split()))] for x in inps]

    print(len(inps))
    ret = []
    for i, inp in enumerate(inps):
        print('inp', i)
        exp_res = inp[0]
        nums = inp[1]

        run_sum = 0

        poss = len(nums)-1

        combinations = []

        def calc_comb(ind, comb, combinations):
            if ind == poss:
                combinations.append(comb)
                return combinations

            for i in range(len(ops)):
                new_comb = comb.copy()
                new_comb.append(ops[i])
                combinations = calc_comb(ind+1, new_comb, combinations)
            return combinations

        combinations = calc_comb(0, [], combinations)

        for comb in combinations:
            # print('res', nums[0], comb[0], nums[1])
            if comb[0] == '||':
                run_sum = int(f'{nums[0]}{nums[1]}')
            else:
                if comb[0] == '+':
                    run_sum = nums[0] + nums[1]
                else:  # '*'
                    run_sum = nums[0] * nums[1]

            ci = 1
            for n in range(2, len(nums)):
                if comb[ci] == '||':
                    run_sum = int(f'{run_sum}{nums[n]}')
                    ci+=1
                    if run_sum>exp_res:
                        break
                    continue
                if comb[ci] == '+':
                    run_sum = run_sum + nums[n]
                else:  # '*'
                    run_sum = run_sum * nums[n]
                ci+=1
                if run_sum>exp_res:
                    break
            # print('run_sum', run_sum) 
            if run_sum == exp_res:
                ret.append(run_sum)
                break
        
    print('ret', ret)
    return sum(ret)




def cal_res(inp):
    exp_res = inp[0]
    nums = inp[1]

    run_sum = 0

    poss = len(nums)-1

    combinations = []
    ops = ['+', '*', '||']

    def calc_comb(ind, comb, combinations):
        if ind == poss:
            combinations.append(comb)
            return combinations

        for i in range(len(ops)):
            new_comb = comb.copy()
            new_comb.append(ops[i])
            combinations = calc_comb(ind+1, new_comb, combinations)
        return combinations

    combinations = calc_comb(0, [], combinations)

    for comb in combinations:
        # print('res', nums[0], comb[0], nums[1])
        if comb[0] == '||':
            run_sum = int(f'{nums[0]}{nums[1]}')
        else:
            if comb[0] == '+':
                run_sum = nums[0] + nums[1]
            else:  # '*'
                run_sum = nums[0] * nums[1]

        ci = 1
        for n in range(2, len(nums)):
            if comb[ci] == '||':
                run_sum = int(f'{run_sum}{nums[n]}')
                ci+=1
                if run_sum>exp_res:
                    break
                continue
            if comb[ci] == '+':
                run_sum = run_sum + nums[n]
            else:  # '*'
                run_sum = run_sum * nums[n]
            ci+=1
            if run_sum>exp_res:
                break
        # print('run_sum', run_sum) 
        if run_sum == exp_res:
            return run_sum
    
    return 0


@timing()
def compute_parallel(data):
    inp = data.split('\n')[:-1]

    print(len(inp))
    inps = [x.split(': ') for x in inp]
    inps = [[int(x[0]), list(map(int, x[1].split()))] for x in inps]

    ret = []
    with Pool() as p:
        ret = p.map(cal_res, inps)

    return sum(ret)


INPUT_S = '''\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

EXPECTED = 11387

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute_optimized(input_s) == expected

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute_parallel(f.read()))