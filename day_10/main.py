import re

# set the recursion limit to 1000000
import sys
from collections import deque

from ortools.sat.python import cp_model

sys.setrecursionlimit(1000000)

with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

cleaned_data = []
for line in data:
    # find all signs enclosed in [], all numbers enclosed in (), all numbers enclosed in {}
    line_data = re.findall(r'\[([^\[\]]+)\]|\(([^\(\)]+)\)|\{([^\{\}]+)\}', line)
    lights, *buttons, voltages = line_data
    lights = [[0 if i == '.' else 1 for i in l] for l in lights if l] [0]
    buttons = [[int(i) for i in b[1].split(',')] for b in buttons]
    voltages = [int(j) for j in voltages[2].split(',')]
    cleaned_data.append((lights, buttons, voltages))

print(cleaned_data)


def find_min_toggles(lights: list[int], buttons: list[list[int]]):
    """
    Find the minimum number of button presses to turn on the lights in the given pattern.
    The order of the button presses does not matter.
    Each button press toggles the lights of the given indexes.
    Uses breath first search.

    :param lights: list of 0s and 1s
    :param buttons: list of lists of indexes

    :return: minimum number of button presses
    """

    state_lights_at_start = tuple(0 for _ in range(len(lights)))
    state_lights_at_end = tuple(lights)
    queue = deque([(state_lights_at_start, 0)])
    visited = {state_lights_at_start}
    while queue:
        current_lights, toggles = queue.popleft()
        if current_lights == state_lights_at_end:
            return toggles
        for button in buttons:
            new_lights = [l for l in current_lights]
            for i in button:
                new_lights[i] = 1 - new_lights[i]
            new_lights = tuple(new_lights)
            if new_lights in visited:
                continue
            visited.add(new_lights)
            queue.append((new_lights, toggles + 1))


def find_min_toggles_to_get_voltage_ineffective(buttons: list[list[int]], voltage: list[int]):
    """
    Find the minimum number of button presses to get the given voltage.
    The order of the button presses does not matter.
    The initial state of the voltage is 0 for each index.
    Each button press increments the voltage of the given indexes.
    Uses breath first search.

    :param buttons: list of lists of indexes
    :param voltage: target voltage

    :return: minimum number of button presses
    """

    state_voltage_at_start = tuple(0 for _ in range(len(voltage)))
    state_voltage_at_end = tuple(voltage)
    queue = deque([(state_voltage_at_start, 0)])
    visited = {state_voltage_at_start}
    while queue:
        current_voltage, toggles = queue.popleft()
        if current_voltage == state_voltage_at_end:
            return toggles
        for button in buttons:
            new_voltage = [v for v in current_voltage]
            for i in button:
                new_voltage[i] += 1
            new_voltage = tuple(new_voltage)
            if new_voltage in visited:
                continue
            if any(v > voltage[i] for i, v in enumerate(new_voltage)):
                continue
            visited.add(new_voltage)
            queue.append((new_voltage, toggles + 1))


def find_min_toggles_to_get_voltage_more_ineffective(buttons: list[list[int]], voltage: list[int]):
    """
    Find the minimum number of button presses to get the given voltage.
    The order of the button presses does not matter.
    The initial state of the voltage is 0 for each index.
    Each button press increments the voltage of the given indexes.
    Uses depth first search.

    :param buttons: list of lists of indexes
    :param voltage: target voltage

    :return: minimum number of button presses
    """

    min_toggles = float('inf')
    state_voltage_at_start = tuple(0 for _ in range(len(voltage)))
    state_voltage_at_end = tuple(voltage)
    visited = {state_voltage_at_start}
    def dfs(current_voltage, toggles):
        nonlocal min_toggles
        if current_voltage == state_voltage_at_end:
            min_toggles = min(min_toggles, toggles)
            return
        if toggles >= min_toggles:
            return
        for button in buttons:
            new_voltage = [v for v in current_voltage]
            for i in button:
                new_voltage[i] += 1
            new_voltage = tuple(new_voltage)
            if new_voltage in visited:
                continue
            if any(v > voltage[i] for i, v in enumerate(new_voltage)):
                continue
            visited.add(new_voltage)
            dfs(new_voltage, toggles + 1)
            visited.remove(new_voltage)
    dfs(state_voltage_at_start, 0)
    return min_toggles


def find_min_toggles_to_get_voltage(buttons: list[list[int]], voltage: list[int]):
    """
    Find the minimum number of button presses to get the given voltage.
    The order of the button presses does not matter.
    The initial state of the voltage is 0 for each index.
    Each button press increments the voltage of the given indexes.
    Uses ortools.

    :param buttons: list of lists of indexes
    :param voltage: target voltage

    :return: minimum number of button presses
    """

    model = cp_model.CpModel()
    button_presses = [model.NewIntVar(0, max(voltage), f'button_{i}') for i in range(len(buttons))]
    voltage_to_button = {i: [] for i in range(len(voltage))}
    for i, v in enumerate(voltage):
        for j, b in enumerate(buttons):
            for v_index in b:
                if v_index == i:
                    voltage_to_button[i].append(button_presses[j])

    for i in range(len(voltage)):
        model.Add(sum(b for b in voltage_to_button[i]) == voltage[i])

    model.Minimize(sum(button_presses))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        return sum(solver.Value(b) for b in button_presses)
    return -1




def find_solution(cleaned_data, part: int = 1):
    if part == 1:
        min_toggles = []
        for i, (lights, buttons, voltages) in enumerate(cleaned_data):
            min_toggles.append(find_min_toggles(lights, buttons))
        return sum(min_toggles)
    if part == 2:
        min_toggles = []
        for i, (lights, buttons, voltages) in enumerate(cleaned_data):
            min_toggles.append(find_min_toggles_to_get_voltage(buttons, voltages))
        return sum(min_toggles)


# Part 1
print('Solution for Part 1: ', find_solution(cleaned_data))

# Part 2
print('Solution for Part 2: ', find_solution(cleaned_data, part=2))
