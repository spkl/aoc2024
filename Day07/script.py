import os
from collections import namedtuple
from itertools import product
from typing import Iterable
os.chdir(os.path.dirname(__file__))

Equation = namedtuple('Equation', ['result', 'operands'])

def can_solve(equation: Equation, operators: list[str]) -> bool:
    for perm in operator_permutations(len(equation.operands) - 1, operators):
        current = equation.operands[0]
        for operator, operand in zip(perm, equation.operands[1:]):
            if current > equation.result:
                break
            if operator == '+':
                current += operand
            elif operator == '*':
                current *= operand
            elif operator == '||':
                current = int(f'{current}{operand}')
            else:
                raise ValueError()
        if current == equation.result:
            return True
    return False

def operator_permutations(n: int, operators: list[str]) -> Iterable[str]:
    return product(operators, repeat=n)

def main():
    equations: list[Equation] = []
    with open('input.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            result, operands = line.split(': ')
            result = int(result)
            operands = [int(x) for x in operands.split()]
            equations.append(Equation(result, operands))

    calibration_result1 = 0
    calibration_result2 = 0
    for i, equation in enumerate(equations):
        print(i)
        if can_solve(equation, ['+', '*']):
            calibration_result1 += equation.result
        if can_solve(equation, ['+', '*', '||']):
            calibration_result2 += equation.result

    print(f'Calibration result 1: {calibration_result1}')
    print(f'Calibration result 2: {calibration_result2}')

if __name__ == '__main__':
    main()
