from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache

with open('input.txt', 'r') as f:
    data = [row.split(': ') for row in f.read().splitlines(keepends=False)]

devices_raw = {row[0]: row[1] for row in data}
devices: dict[str, list[str]] = {}
for _in, out in devices_raw.items():
    devices[_in] = out.split(' ')
devices['out'] = []

# print(devices)


@dataclass
class Node:
    name: str
    required_reached: list[str]
    paths_to_node: int


def dfs_paths_pruned(
        devices: dict[str, list[str]],
        start: str = 'you',
        end: str = 'out',
        devices_to_pass: list[str] = None
):
    if not devices_to_pass:
        devices_to_pass = set()
    else:
        devices_to_pass = set(devices_to_pass)

    # Vorberechnung: Welche required devices sind von jedem Knoten erreichbar?
    reachable_targets = precompute_reachable_targets(devices, devices_to_pass | {end})

    paths = 0
    required_count = len(devices_to_pass)

    def dfs(current: str, path: set, pass_count: int):
        nonlocal paths

        if current == end:
            if pass_count == required_count:
                paths += 1
                if paths % 1_000_000 == 0:
                    print(f'Paths: {paths}')
                    print(f'Path: {path}')
                    print(f'Path length: {len(path)}')
            return

        # Pruning: Welche required devices fehlen noch?
        if pass_count < required_count:
            remaining = devices_to_pass - path
            reachable_from_here = reachable_targets.get(current, set())
            if not remaining.issubset(reachable_from_here):
                return  # Abbruch – nicht alle required devices erreichbar

        # Pruning: Ist 'end' überhaupt noch erreichbar?
        if end not in reachable_targets.get(current, set()):
            return

        for next_device in devices[current]:
            if next_device not in path:
                new_pass_count = pass_count
                if next_device in devices_to_pass:
                    new_pass_count += 1
                dfs(next_device, path | {next_device}, new_pass_count)

    initial_pass = 1 if start in devices_to_pass else 0
    dfs(start, {start}, initial_pass)
    return paths


def precompute_reachable_targets(
        devices: dict[str, list[str]],
        targets: set[str]
) -> dict[str, set[str]]:
    """
    Berechnet für jeden Knoten, welche Ziele (targets) von dort erreichbar sind.
    Nutzt Rückwärts-BFS von jedem Target.
    """
    # Invertierter Graph: Wer zeigt auf wen?
    reverse_graph = {node: [] for node in devices}
    for source, neighbors in devices.items():
        for neighbor in neighbors:
            if neighbor in reverse_graph:
                reverse_graph[neighbor].append(source)

    reachable = {node: set() for node in devices}

    for target in targets:
        if target not in reverse_graph:
            continue

        # BFS rückwärts vom Target
        visited = {target}
        queue = [target]

        while queue:
            node = queue.pop(0)
            reachable[node].add(target)

            for predecessor in reverse_graph.get(node, []):
                if predecessor not in visited:
                    visited.add(predecessor)
                    queue.append(predecessor)

    return reachable





def solve(devices: dict[str, list[str]]):
    return dfs_paths_pruned(devices, 'you', 'out')

# Part 1
print('Solution for Part 1: ', solve(devices))
