import os
from collections import namedtuple
from typing import Iterable
os.chdir(os.path.dirname(__file__))

operators = ['+', '*']
Equation = namedtuple('Equation', ['result', 'operands'])

def can_solve(equation: Equation) -> bool:
    perm_list = list(operator_permutations(len(equation.operands)-1))
    for perm in perm_list:
        current = equation.operands[0]
        for operator, operand in zip(perm, equation.operands[1:]):
            if operator == '+':
                current += operand
            elif operator == '*':
                current *= operand
            else:
                raise ValueError()
        if current == equation.result:
            return True
    return False

def operator_permutations(n_operands: int) -> Iterable[str]:
    for i in range(2**n_operands):
        bitfield = format(i, '0' + str(n_operands) + 'b')
        bitfield = bitfield.replace('0', '+').replace('1', '*')
        yield bitfield

def main():
    equations: list[Equation] = []
    with open('input.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            result, operands = line.split(': ')
            result = int(result)
            operands = [int(x) for x in operands.split()]
            equations.append(Equation(result, operands))

    calibration_result = 0
    for equation in equations:
        if can_solve(equation):
            calibration_result += equation.result

    print(f'Calibration result: {calibration_result}')

if __name__ == '__main__':
    main()
