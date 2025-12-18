from collections import defaultdict, deque


# Graph parsen
def parse_input(text: str) -> dict[str, list[str]]:
    graph = {}
    for line in text.strip().split('\n'):
        node, targets = line.split(': ')
        graph[node] = targets.split()
    return graph


def get_reachable_subgraph(graph: dict[str, list[str]], start: str, end: str) -> set[str]:
    """Findet alle Knoten, die von start erreichbar sind UND end erreichen können."""
    # Vorwärts-BFS: Was ist von start erreichbar?
    forward_reachable = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in forward_reachable:
            continue
        forward_reachable.add(node)
        for neighbor in graph.get(node, []):
            queue.append(neighbor)

    # Rückwärts-Graph bauen
    reverse_graph = defaultdict(list)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reverse_graph[neighbor].append(node)

    # Rückwärts-BFS: Was kann end erreichen?
    backward_reachable = set()
    queue = deque([end])
    while queue:
        node = queue.popleft()
        if node in backward_reachable:
            continue
        backward_reachable.add(node)
        for neighbor in reverse_graph.get(node, []):
            queue.append(neighbor)

    # Schnittmenge: Knoten auf gültigen Pfaden
    return forward_reachable & backward_reachable


def topological_sort(graph: dict[str, list[str]], nodes: set[str]) -> list[str]:
    """Topologische Sortierung für Subgraph."""
    in_degree = defaultdict(int)
    for node in nodes:
        for neighbor in graph.get(node, []):
            if neighbor in nodes:
                in_degree[neighbor] += 1

    # Knoten ohne eingehende Kanten
    queue = deque([n for n in nodes if in_degree[n] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph.get(node, []):
            if neighbor in nodes:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return result


def count_paths(graph: dict[str, list[str]], start: str, end: str) -> int:
    """Zählt alle Pfade von start nach end mittels DP."""
    if start == end:
        return 1

    # Relevanten Subgraph finden
    relevant_nodes = get_reachable_subgraph(graph, start, end)

    if start not in relevant_nodes or end not in relevant_nodes:
        return 0

    # Topologische Sortierung
    topo_order = topological_sort(graph, relevant_nodes)

    # DP: Pfadanzahl berechnen
    paths = defaultdict(int)
    paths[start] = 1

    for node in topo_order:
        for neighbor in graph.get(node, []):
            if neighbor in relevant_nodes:
                paths[neighbor] += paths[node]

    return paths[end]


def solve_part2(graph: dict[str, list[str]]) -> int:
    """Löst Teil 2: Pfade von svr→out über dac UND fft."""
    # Fall 1: svr → dac → fft → out
    case1 = (count_paths(graph, "svr", "dac")
             * count_paths(graph, "dac", "fft")
             * count_paths(graph, "fft", "out"))

    # Fall 2: svr → fft → dac → out
    case2 = (count_paths(graph, "svr", "fft")
             * count_paths(graph, "fft", "dac")
             * count_paths(graph, "dac", "out"))

    return case1 + case2





with open('input.txt', 'r') as f:
    puzzle_input = f.read()
graph = parse_input(puzzle_input)
result = solve_part2(graph)
print(result)