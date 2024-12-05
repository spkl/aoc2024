import os
os.chdir(os.path.dirname(__file__))

class ErrorInfo:
    error_value: int
    must_come_after: int

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        order_lines: list[str] = []
        update_lines: list[str] = []
        state = 0
        for line in f.readlines():
            line = line.strip()
            if state == 0:
                if not line:
                    state = 1
                    continue
                order_lines.append(line)
            if state == 1:
                update_lines.append(line)

    key_after_values: dict[int, list[int]] = {}
    for line in order_lines:
        before, after = tuple(int(n) for n in line.split('|'))
        if after in key_after_values:
            key_after_values[after].append(before)
        else:
            key_after_values[after] = [before]

    updates = [[int(n) for n in update_line.split(',')] for update_line in update_lines]
    correct_updates: list[list[int]] = []
    incorrect_updates: list[list[int]] = []
    for update in updates:
        if is_correct(key_after_values, update):
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)

    sum = 0
    for correct_update in correct_updates:
        middle_value = correct_update[int(len(correct_update)/2)]
        sum += middle_value

    print(sum)

    for incorrect_update in incorrect_updates:
        error_info = ErrorInfo()
        while not is_correct(key_after_values, incorrect_update, error_info):
            error_index = incorrect_update.index(error_info.error_value)
            must_come_after_index = incorrect_update.index(error_info.must_come_after)
            del incorrect_update[error_index]
            incorrect_update.insert(must_come_after_index, error_info.error_value)

    sum = 0
    for incorrect_update in incorrect_updates:
        middle_value = incorrect_update[int(len(incorrect_update)/2)]
        sum += middle_value

    print(sum)

def is_correct(key_after_values, update, error_info: ErrorInfo = None):
    seen = set()
    for number in update:
        if not is_correct:
            break
        if number in key_after_values:
            values_coming_before = key_after_values[number]
            for value_coming_before in values_coming_before:
                if value_coming_before in update and value_coming_before not in seen:
                    if error_info:
                        error_info.error_value = number
                        error_info.must_come_after = value_coming_before
                    return False
        seen.add(number)
    return True

if __name__ == '__main__':
    main()
