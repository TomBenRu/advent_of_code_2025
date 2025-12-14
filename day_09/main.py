from functools import lru_cache
from itertools import combinations

with open('test_input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

data = [tuple(int(i) for i in row.split(',')) for row in data]

print(data)

max_x = max(p[0] for p in data)
max_y = max(p[1] for p in data)

all_edges = set()

for i, p_1 in enumerate(data):
    if i == len(data) - 1:
        p_2 = data[0]
    else:
        p_2 = data[i + 1]
    if p_1[0] == p_2[0]:
        all_edges |= {(p_1[0], c) for c in range(min(p_1[1], p_2[1]), max(p_1[1], p_2[1]) + 1)}
    elif p_1[1] == p_2[1]:
        all_edges |= {(c, p_1[1]) for c in range(min(p_1[0], p_2[0]), max(p_1[0], p_2[0]) + 1)}

def print_grid_with_edges(point: tuple[int, int] | None = None):
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if point and (x, y) == point:
                print('O', end='')
            elif (x, y) in all_edges:
                print('#', end='')
            else:
                print('.', end='')
        print()

# print_grid_with_edges()


def square_area_from_points(p_1, p_2):
    return (abs(p_2[0] - p_1[0] )+ 1) * (abs(p_2[1] - p_1[1]) + 1)


@lru_cache(maxsize=10000)
def check_if_corners_inside(p_1, p_2):
    points = (p_1[0], p_2[1]), (p_2[0], p_1[1])

    for point in points:
        if point in all_edges:
            # print('Point in edges!')
            continue
        crossings = 0
        for delta in range(max(max_x, max_y) + 1):
            new_point = (point[0] + delta, point[1] + delta)
            if new_point[0] > max_x or new_point[1] > max_y:
                break
            print_grid_with_edges(new_point)
            if new_point in all_edges:
                print('>>> Point in edges!')
                if (new_point in data
                        and (((new_point[0], new_point[1] - 1) in all_edges
                              and (new_point[0] + 1, new_point[1]) in all_edges))
                        or ((new_point[0] - 1, new_point[1]) in all_edges
                              and (new_point[0], new_point[1] + 1) in all_edges)):
                    print('>>> Fake crossing!')
                    continue
                print('>>> Real crossing!')
                crossings += 1
        if crossings % 2 == 0:
            return False
    return True


def max_square_area_from_points(points: list[tuple[int, int]], part: int = 1):
    max_area = 0
    all_duos = combinations(points, 2)
    print(f'>> {len(list(all_duos))} duos to check')
    all_duos = combinations(points, 2)
    for i, (p_1, p_2) in enumerate(all_duos):
        if i % 10000 == 0:
            print(f'>> {i} duos checked')
        if part == 2 and not check_if_corners_inside(p_1, p_2):
            continue
        max_area = max(max_area, square_area_from_points(p_1, p_2))
    return max_area

# print('Solution for Part 1: ', max_square_area_from_points(data))
# print('Solution for Part 2: ', max_square_area_from_points(data, part=2))

result = check_if_corners_inside((7, 0), (0, 1))
print(result)
