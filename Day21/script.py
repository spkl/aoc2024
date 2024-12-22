import os
from typing import Iterable
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

    def _type_key(self, key: str) -> Iterable[str]:
        src_x, src_y = self.pos
        dest_x, dest_y = self._find_key(key)
        if self.forbidden_pos != (dest_x, src_y): # assume forbidden key is in a corner
            if dest_x < src_x:
                for _ in range(src_x - dest_x):
                    yield '<'
            elif dest_x > src_x:
                for _ in range(dest_x - src_x):
                    yield '>'
            if dest_y < src_y:
                for _ in range(src_y - dest_y):
                    yield '^'
            elif dest_y > src_y:
                for _ in range(dest_y - src_y):
                    yield 'v'
        else:
            if dest_y < src_y:
                for _ in range(src_y - dest_y):
                    yield '^'
            elif dest_y > src_y:
                for _ in range(dest_y - src_y):
                    yield 'v'
            if dest_x < src_x:
                for _ in range(src_x - dest_x):
                    yield '<'
            elif dest_x > src_x:
                for _ in range(dest_x - src_x):
                    yield '>'
        yield 'A'
        self.pos = (dest_x, dest_y)

    def type_code(self, keys: str) -> str:
        typed_keys = ''
        for key in keys:
            for typed_key in self._type_key(key):
                typed_keys += typed_key
        return typed_keys

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
        for keypad in self.keypads:
            code = keypad.type_code(code)
        return code

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
