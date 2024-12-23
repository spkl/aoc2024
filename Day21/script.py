import os
import itertools
os.chdir(os.path.dirname(__file__))

class Keypad:
    start_key: str = None
    forbidden_key: str = None
    layout: list[list[str]] = None

    def __init__(self):
        self.pos = self._find_key(self.start_key)
        self.forbidden_pos = self._find_key(self.forbidden_key)

    def _find_key(self, key: str) -> tuple[int, int]:
        for y, line in enumerate(self.layout):
            for x, char in enumerate(line):
                if char == key:
                    return (x, y)
        assert False

    def _type_key(self, key: str) -> list[str]:
        '''Returns all possible paths to type the key from the current position.'''
        src_x, src_y = self.pos
        dest_x, dest_y = self._find_key(key)
        required_keys = '<' * (src_x - dest_x) \
            + '>' * (dest_x - src_x) \
            + '^' * (src_y - dest_y) \
            + 'v' * (dest_y - src_y)
        paths = set(itertools.permutations(required_keys, len(required_keys)))
        possible_paths = [''.join(path) + 'A' for path in paths if self._path_is_possible(path)]
        self.pos = (dest_x, dest_y)
        return possible_paths

    def _path_is_possible(self, path: str) -> bool:
        x, y = self.pos
        for step in path:
            match step:
                case '<':
                    x -= 1
                case '>':
                    x += 1
                case '^':
                    y -= 1
                case 'v':
                    y += 1
            if (x, y) == self.forbidden_pos:
                return False
        return True

    def type_code(self, keys: str) -> list[str]:
        '''Returns all possible paths to type the code (keys) from the current position.'''
        path_possibilities = []
        for key in keys:
            path_possibilities.append(self._type_key(key))
        result = Keypad.recombine(path_possibilities)
        return result

    @staticmethod
    def recombine(options):
        result = []
        result.extend(options[0])
        for option in options[1:]:
            result = [item for item in result for _ in range(len(option))]
            option_cycle = itertools.cycle(option)
            for i, x in enumerate(result):
                result[i] = x + next(option_cycle)
        return result

class NumericKeypad(Keypad):
    start_key = 'A'
    forbidden_key = ' '
    layout = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [' ', '0', 'A']
    ]

class DirectionalKeypad(Keypad):
    start_key = 'A'
    forbidden_key = ' '
    layout = [
        [' ', '^', 'A'],
        ['<', 'v', '>']
    ]

class KeypadChain:
    def __init__(self, keypads: list[Keypad]):
        self.keypads = keypads

    def type(self, code: str) -> str:
        options = [code]
        for keypad in self.keypads:
            new_options = []
            for option in options:
                new_options.extend(keypad.type_code(option))
            options = new_options
        min_option = options[0]
        for option in options:
            if len(option) < len(min_option):
                min_option = option
        return min_option

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        codes = [line.strip() for line in f.readlines()]

    print()
    complexity_sum = 0
    for code in codes:
        chain = KeypadChain([NumericKeypad(), DirectionalKeypad(), DirectionalKeypad()])
        keypresses = chain.type(code)
        complexity = int(code[:-1]) * len(keypresses)
        complexity_sum += complexity
        print(code, len(keypresses), keypresses)

    print(complexity_sum)

if __name__ == '__main__':
    main()
