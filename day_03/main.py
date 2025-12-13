with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

print(data)

total_output = 0

for bank in data:
    digits = [int(d) for d in bank]
    max_first = max(digits[:-1])
    index_first = digits.index(max_first)
    max_second = max(digits[index_first + 1:])
    total_output += int(f'{max_first}{max_second}')

print(total_output)

total_output = 0

for bank in data:
    max_of_bank = ''
    current_index = 0
    digits = [int(d) for d in bank]
    for i in range(12):
        if 11 - i == 0:
            max_digit = max(digits[current_index:])
        else:
            max_digit = max(digits[current_index:-(11 - i)])
        max_of_bank += str(max_digit)
        current_index += digits[current_index:].index(max_digit) + 1
    total_output += int(max_of_bank)

print(total_output)