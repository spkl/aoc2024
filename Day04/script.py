import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    word = 'XMAS'
    n = 0
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == word[0]:
                # horizontal
                try:
                    if grid[i][j : j + len(word)] == list(word):
                        n += 1
                except IndexError:
                    pass
                # horizontal backwards
                try:
                    if grid[i][j - (len(word) - 1) : j + 1] == list(reversed(word)):
                        n += 1
                except IndexError:
                    pass
                # vertical
                try:
                    found = True
                    for word_idx, word_char in enumerate(word):
                        if grid[i + word_idx][j] != word_char:
                            found = False
                            break
                    if found:
                        n += 1
                except IndexError:
                    pass
                # vertical backwards
                try:
                    found = True
                    for word_idx, word_char in enumerate(word):
                        if i - word_idx < 0 or grid[i - word_idx][j] != word_char:
                            found = False
                            break
                    if found:
                        n += 1
                except IndexError:
                    pass
                # diagonal ↘
                try:
                    found = True
                    for word_idx, word_char in enumerate(word):
                        if grid[i + word_idx][j + word_idx] != word_char:
                            found = False
                            break
                    if found:
                        n += 1
                except IndexError:
                    pass
                # diagonal ↖
                try:
                    found = True
                    for word_idx, word_char in enumerate(word):
                        if i - word_idx < 0 or j - word_idx < 0 or grid[i - word_idx][j - word_idx] != word_char:
                            found = False
                            break
                    if found:
                        n += 1
                except IndexError:
                    pass
                # diagonal ↗
                try:
                    found = True
                    for word_idx, word_char in enumerate(word):
                        if i - word_idx < 0 or grid[i - word_idx][j + word_idx] != word_char:
                            found = False
                            break
                    if found:
                        n += 1
                except IndexError:
                    pass
                # diagonal ↙
                try:
                    found = True
                    for word_idx, word_char in enumerate(word):
                        if j - word_idx < 0 or grid[i + word_idx][j - word_idx] != word_char:
                            found = False
                            break
                    if found:
                        n += 1
                except IndexError:
                    pass
    print(n)

    m = 0
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == 'A' and i > 0 and j > 0 and i < len(grid) - 1 and j < len(line) - 1:
                if grid[i-1][j-1] == 'M' and grid[i+1][j+1] == 'S' or grid[i-1][j-1] == 'S' and grid[i+1][j+1] == 'M':
                    if grid[i+1][j-1] == 'M' and grid[i-1][j+1] == 'S' or grid[i+1][j-1] == 'S' and grid[i-1][j+1] == 'M':
                        m += 1
    print(m)


if __name__ == '__main__':
    main()
