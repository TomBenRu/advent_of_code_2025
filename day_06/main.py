from functools import reduce

with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=True)
    numbers_with_spaces_raw = [list(n) for n in data[:-1]]
    print(f'numbers_with_spaces_raw: {numbers_with_spaces_raw}')
    data = [[v for v in i.split(' ') if v] for i in data]
    numbers = [[int(i) for i in row if i.isdigit()] for row in data[:-1]]
    operators = data[-1]

# numbers werden gedreht
numbers = [[row[i] for row in numbers] for i in range(len(numbers[0]))]
numbers_with_spaces_raw = [[row[i] for row in numbers_with_spaces_raw] for i in range(len(numbers_with_spaces_raw[0]))]
print(f'numbers_with_spaces_raw: {numbers_with_spaces_raw}')

numbers_with_spaces = [[]]
for row in numbers_with_spaces_raw:
    if all(i == ' ' for i in row):
        numbers_with_spaces.append([])
        continue
    print(f'row: {row}')
    if all(i == '\n' for i in row):
        continue
    numbers_with_spaces[-1].append(int(''.join(row)))

print(f'numbers_with_spaces: {numbers_with_spaces}')

print(data)
print(numbers)
print(operators)

result = 0

for i, row in enumerate(numbers):
    if operators[i] == '+':
        result += sum(row)
    elif operators[i] == '*':
        result += reduce(lambda x, y: x * y, row)

print(result)

result = 0

for i, row in enumerate(numbers_with_spaces):
    if operators[i] == '+':
        result += sum(row)
    elif operators[i] == '*':
        result += reduce(lambda x, y: x * y, row)


print(result)