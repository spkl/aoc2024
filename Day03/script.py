import re
import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        memory = f.read()

    sum1 = 0
    for statement in re.findall('mul\((\d+),(\d+)\)', memory):
        sum1 += int(statement[0]) * int(statement[1])

    sum2 = 0
    enabled = True
    for statement in re.finditer('(mul\((?P<x>\d+),(?P<y>\d+)\))|do\(\)|don\'t\(\)', memory):
        match statement.group():
            case 'do()':
                enabled = True
            case 'don\'t()':
                enabled = False
            case _:
                if enabled:
                    sum2 += int(statement.group('x')) * int(statement.group('y'))

    print(sum1)
    print(sum2)

if __name__ == '__main__':
    main()
