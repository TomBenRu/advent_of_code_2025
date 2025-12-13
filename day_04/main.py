with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

grid = set()
adjacent = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

for i, line in enumerate(data):
    for j, char in enumerate(line):
        if char == '@':
            grid.add((i, j))

sum_rolls = 0

for i, line in enumerate(data):
    for j, char in enumerate(line):
        if char == '@':
            if sum(neighbor in grid for neighbor in [(i + a[0], j + a[1]) for a in adjacent]) < 4:
                sum_rolls += 1

print(sum_rolls)

total_removed = 0

while True:
    removed = 0
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == '@' and (i, j) in grid:
                if sum(neighbor in grid for neighbor in [(i + a[0], j + a[1]) for a in adjacent]) < 4:
                    grid.remove((i, j))
                    removed += 1
                    total_removed += 1
    if not removed:
        break

print(total_removed)

