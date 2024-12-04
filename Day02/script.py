import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        reports = [[int(level) for level in line.strip().split()] for line in f.readlines()]

    n_safe = 0
    n_safe_dampened = 0

    for report in reports:
        if is_safe(report):
            n_safe += 1
            n_safe_dampened += 1
        else:
            for index in range(len(report)):
                copy = report.copy()
                del copy[index]
                if is_safe(copy):
                    n_safe_dampened += 1
                    break

    print(n_safe)
    print(n_safe_dampened)

def is_safe(report):
    inc, dec = True, True
    for previous, current in zip(report, report[1:]):
        if previous >= current or current - previous > 3:
            inc = False
        if current >= previous or previous - current > 3:
            dec = False
    return inc or dec

if __name__ == '__main__':
    main()
