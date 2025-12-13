with open('input.txt', 'r') as f:
    fresh_ingredients, available = f.read().strip().split('\n\n')

fresh_ingredients_ranges = [(int(r.split('-')[0]), int(r.split('-')[1])) for r in fresh_ingredients.split('\n')]

available = [int(r) for r in available.split('\n')]

print(f'{fresh_ingredients_ranges=}')
print(f'{available=}')

total_available_fresh_ingredients = 0

for available_ingredient in available:
    for fresh_ingredient in fresh_ingredients_ranges:
        if fresh_ingredient[0] <= available_ingredient <= fresh_ingredient[1]:
            total_available_fresh_ingredients += 1
            break

# Part 1
print(total_available_fresh_ingredients)

def cut_range_out_of_range(range_to_cut_out_of, range_to_cut_out) -> list[tuple[int, int]]:
    if range_to_cut_out[0] > range_to_cut_out_of[1]:
        return [range_to_cut_out_of]
    if range_to_cut_out_of[0] > range_to_cut_out[1]:
        return [range_to_cut_out_of]
    if (range_to_cut_out_of[0] < range_to_cut_out[0] < range_to_cut_out_of[1]
        and range_to_cut_out_of[0] < range_to_cut_out[1] < range_to_cut_out_of[1]):
        return [(range_to_cut_out_of[0], range_to_cut_out[0] - 1), (range_to_cut_out[1] + 1, range_to_cut_out_of[1])]
    if range_to_cut_out_of[0] < range_to_cut_out[0] < range_to_cut_out_of[1]:
        return [(range_to_cut_out_of[0], range_to_cut_out[0] - 1)]
    if range_to_cut_out_of[0] >= range_to_cut_out[0] and range_to_cut_out[1] < range_to_cut_out_of[1]:
        return [(range_to_cut_out[1] + 1, range_to_cut_out_of[1])]
    return []

total_possible_fresh_ingredients = 0
refactored_fresh_ingredients_ranges = []

for fresh_ingredient in fresh_ingredients_ranges:
    if not refactored_fresh_ingredients_ranges:
        refactored_fresh_ingredients_ranges.append(fresh_ingredient)
        continue
    split_fresh_ingredients_ranges = [fresh_ingredient]
    new_split_fresh_ingredients_ranges = []
    for refactored_fresh_ingredient in refactored_fresh_ingredients_ranges:
        print(f'{refactored_fresh_ingredient=}')
        for split_fresh_ingredient in split_fresh_ingredients_ranges:
            print(f'{split_fresh_ingredient=}')
            new_split_fresh_ingredients_ranges.extend(
                cut_range_out_of_range(split_fresh_ingredient, refactored_fresh_ingredient))
            print(f'{new_split_fresh_ingredients_ranges=}')
        split_fresh_ingredients_ranges = new_split_fresh_ingredients_ranges
        new_split_fresh_ingredients_ranges = []
    refactored_fresh_ingredients_ranges.extend(split_fresh_ingredients_ranges)

print(f'{refactored_fresh_ingredients_ranges=}')

# Part 2
print(sum(b - a + 1 for a, b in refactored_fresh_ingredients_ranges))
