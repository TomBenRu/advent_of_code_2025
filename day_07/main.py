from collections import defaultdict
from pprint import pprint

with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

grid = {(i, j): c for i, line in enumerate(data) for j, c in enumerate(line)}

start = next((i, j) for i, j in grid if grid[i, j] == 'S')

current_nodes = {start}
nodes_at_end = set()
beam_splits = set()

while True:
    new_nodes = set()
    for node in current_nodes:
        if grid[node] in {'S', '.'}:
            if (new_node := (node[0] + 1, node[1])) in grid:
                new_nodes.add(new_node)
            else:
                nodes_at_end.add(new_node)
        if grid[node] == '^':
            new_nodes |= {(node[0], node[1] - 1), (node[0], node[1] + 1)}
            beam_splits.add(node)
    current_nodes = new_nodes
    if not current_nodes:
        break

print(nodes_at_end)

print(len(beam_splits))

paths = 0
current_nodes = defaultdict(int, {start: 1})
while True:
    print(len(current_nodes))
    new_nodes = defaultdict(int)
    for node in current_nodes:
        if grid[node] in {'S', '.'}:
            if (new_node := (node[0] + 1, node[1])) in grid:
                new_nodes[new_node] += current_nodes[node]
            else:
                paths += current_nodes[node]
        if grid[node] == '^':
            new_nodes[(node[0], node[1] - 1)] += current_nodes[node]
            new_nodes[(node[0], node[1] + 1)] += current_nodes[node]
    current_nodes = new_nodes
    if not current_nodes:
        break



print(paths)
