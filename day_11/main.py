from functools import lru_cache

with open('input.txt', 'r') as f:
    data = [row.split(': ') for row in f.read().splitlines(keepends=False)]

devices = {row[0]: row[1] for row in data}
for _in, out in devices.items():
    devices[_in] = out.split(' ')

# print(devices)


def precompute_reachable(devices: dict[str, list[str]], targets: set[str]) -> dict[str, set[str]]:
    """Für jeden Knoten: Welche targets sind von dort erreichbar?"""
    reachable = {node: set() for node in devices}

    # Rückwärts-BFS von jedem Target
    for target in targets:
        visited = {target}
        queue = [target]
        while queue:
            node = queue.pop(0)
            for source, neighbors in devices.items():
                if node in neighbors and source not in visited:
                    visited.add(source)
                    queue.append(source)

        for node in visited:
            reachable[node].add(target)

    return reachable





def dfs_paths_from_start_to_end(devices: dict[str, list[str]], start: str = 'you', end: str = 'out',
                                devices_to_pass: list[str] = None):
    paths = 0

    def dfs(current_device, path):
        nonlocal paths
        if current_device == end:
            if devices_to_pass is None or all(d in path for d in devices_to_pass):
                paths += 1
                if paths % 100000 == 0:
                    print(f'Paths: {paths}')
                    print(f'Path: {path}')
                    print(f'Path length: {len(path)}')
            return
        if not devices.get(current_device):
            return
        for next_device in devices[current_device]:
            if next_device in path:
                print(f'Cycle detected: {current_device} -> {next_device}, path length: {len(path)}')
                continue
            dfs(next_device, path | {next_device})
    dfs(start, {start})
    return paths


def solve(devices: dict[str, list[str]], part: int = 1):
    if part == 1:
        return dfs_paths_from_start_to_end(devices, 'you', 'out')
    if part == 2:
        return dfs_paths_from_start_to_end(devices, 'svr', 'out', devices_to_pass=['dac', 'fft'])

# Part 1
# print('Solution for Part 1: ', solve(devices))

# Part 2
# print('Solution for Part 2: ', solve(devices, part=2))


print(reachable := precompute_reachable(devices, {'dac', 'fft'}))
print({k: v for k, v in reachable.items() if not {'dac', 'fft'} - v})
