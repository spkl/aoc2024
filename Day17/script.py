from dataclasses import dataclass, field
import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        reg_a = int(f.readline().split(': ')[1])
        reg_b = int(f.readline().split(': ')[1])
        reg_c = int(f.readline().split(': ')[1])
        _ = f.readline()
        program = [int(i) for i in f.readline().split(': ')[1].split(',')]

    c = Computer(program, reg_a, reg_b, reg_c)
    c.run()
    print('Outputs:')
    print(','.join(str(o) for o in c.outputs))

@dataclass
class Computer:
    program: list[int]
    reg_a: int
    reg_b: int
    reg_c: int
    iptr: int = 0
    outputs: list[int] = field(default_factory=lambda: [])

    def run(self):
        while self.iptr < len(self.program):
            self.cycle()

    def cycle(self):
        instruction = self.program[self.iptr]
        literal_operand = self.program[self.iptr + 1]
        combo_operand = self.resolve_operand(literal_operand)
        increase_iptr = True
        match instruction:
            case 0: #adv
                self.reg_a = int(self.reg_a / 2**combo_operand)
            case 1: #bxl
                self.reg_b = self.reg_b ^ literal_operand
            case 2: #bst
                self.reg_b = combo_operand % 8
            case 3: #jnz
                if self.reg_a != 0:
                    self.iptr = literal_operand
                    increase_iptr = False
            case 4: #bxc
                self.reg_b = self.reg_b ^ self.reg_c
            case 5: #out
                self.outputs.append(combo_operand % 8)
            case 6: #bdv
                self.reg_b = int(self.reg_a / 2**combo_operand)
            case 7: #cdv
                self.reg_c = int(self.reg_a / 2**combo_operand)

        if increase_iptr:
            self.iptr += 2

    def resolve_operand(self, literal_operand):
        if 0 <= literal_operand <= 3:
            return literal_operand
        match literal_operand:
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                return None

if __name__ == '__main__':
    main()
