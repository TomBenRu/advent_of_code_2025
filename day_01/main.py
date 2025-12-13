

with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

next_number = 50
number_of_zeros = 0

for i in data:
    n = int(i[1:])
    if i[0] == 'L':
        next_number -= n
    else:
        next_number += n
    next_number %= 100
    if next_number == 0:
        number_of_zeros += 1

print(number_of_zeros)

next_number = 50
number_of_zeros = 0

for i in data:
    n = int(i[1:])
    if i[0] == 'L':
        if next_number == 0:
            number_of_zeros -= 1
        next_number -= n
        while next_number < 0:
            number_of_zeros += 1
            next_number += 100
        if next_number == 0:
            number_of_zeros += 1
    else:
        next_number += n
        while next_number > 100:
            next_number -= 100
            number_of_zeros += 1
        if next_number == 100:
            number_of_zeros += 1
            next_number = 0

print(number_of_zeros)
