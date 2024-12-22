import os
os.chdir(os.path.dirname(__file__))

class Buyer():
    def __init__(self, current: int):
        self.current = current

    def next(self) -> int:
        self.current = ((self.current * 64) ^ self.current) % 16777216
        self.current = (int(self.current / 32) ^ self.current) % 16777216
        self.current = ((self.current * 2048) ^ self.current) % 16777216
        return self.current

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        buyers = [Buyer(int(line.strip())) for line in f.readlines()]

    secret_sum = 0
    for buyer in buyers:
        for _ in range(2000):
            secret = buyer.next()
        print(secret)
        secret_sum += secret
    print(f'Sum = {secret_sum}')

if __name__ == '__main__':
    main()
