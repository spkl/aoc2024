import os
os.chdir(os.path.dirname(__file__))

lefts = []
rights = []

with open('input.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        (left, right) = line.strip().split()
        lefts.append(int(left))
        rights.append(int(right))

lefts.sort()
rights.sort()

distance = 0
similarity = 0
for (left, right) in zip(lefts, rights):
    distance += max(left, right) - min(left, right)
    similarity += left * rights.count(left)

print(distance)
print(similarity)
