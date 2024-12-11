import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        stones = f.read().strip().split()

    blinks = 25
    for _ in range(blinks):
        new_stones = []
        for stone in stones:
            if stone == '0':
                new_stones.append('1')
            elif len(stone) % 2 == 0:
                new_stones.append(stone[:len(stone)//2])
                right_stone = stone[len(stone)//2:]
                while len(right_stone) > 1 and right_stone[0] == '0':
                    right_stone = right_stone[1:]
                new_stones.append(right_stone)
            else:
                new_stones.append(str(int(stone) * 2024))
        stones = new_stones

    print(len(stones))

#import cProfile
if __name__ == '__main__':
    #cProfile.run('main()')
    main()
