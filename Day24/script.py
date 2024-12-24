import os
from dataclasses import dataclass
os.chdir(os.path.dirname(__file__))

@dataclass
class Gate:
    input1: str
    input2: str
    operation: str
    output: str

class MonitoringDevice:
    def __init__(self, initial_values: dict[str, bool], gates: list[Gate]):
        self.values = initial_values
        self.pending_gates = gates
        self.complete_gates: list[Gate] = []

    def process(self):
        while self.pending_gates:
            for gate in self.pending_gates:
                if gate.input1 in self.values and gate.input2 in self.values:
                    v1, v2 = self.values[gate.input1], self.values[gate.input2]
                    match gate.operation:
                        case 'AND':
                            result = v1 and v2
                        case 'XOR':
                            result = v1 != v2
                        case 'OR':
                            result = v1 or v2
                    self.values[gate.output] = bool(result)
                    self.pending_gates.remove(gate)
                    self.complete_gates.append(gate)
                    break

    def get_result(self):
        binary_str = ''
        for wire in reversed(sorted(self.values.keys())):
            if not wire.startswith('z'):
                break
            binary_str += '1' if self.values[wire] else '0'
        result = int(binary_str, 2)
        return result

def main():
    initial_values: dict[str, bool] = {}
    gates: list[Gate] = []
    with open('input.txt', 'r', encoding='utf-8') as f:
        while (line := f.readline().strip()):
            wire, value = line.split(': ')
            initial_values[wire] = value == '1'
        for line in f.readlines():
            line = line.strip()
            input1, operation, input2, _, output = line.split(' ')
            gates.append(Gate(input1, input2, operation, output))

    md = MonitoringDevice(initial_values, gates)
    md.process()
    print(md.get_result())

if __name__ == '__main__':
    main()
