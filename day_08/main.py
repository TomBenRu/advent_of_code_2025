from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int
    z: int

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

with open('input.txt', 'r') as f:
    data = f.read().splitlines(keepends=False)

data = [Coordinate(*[int(i) for i in row.split(',')]) for row in data]

distances: list[tuple[tuple[tuple[int, int, int], tuple[int, int, int]], float]] = []

for i, c_1 in enumerate(data):
    for j, c_2 in enumerate(data[i + 1:]):
        distances.append((((c_1.x, c_1.y, c_1.z), (c_2.x, c_2.y, c_2.z)), c_1.distance(c_2)))

distances.sort(key=lambda x: x[1])
# print(f'distances: {distances}')


def connect_clusters(distances: list[tuple[tuple[tuple[int, int, int], tuple[int, int, int]], float]],
                     part: int = 1):
    clusters: list[set[tuple[int, int, int]]] = []
    connected = 0
    last_connected: tuple[tuple[int, int, int], tuple[int, int, int]] | None = None
    for i, ((c_1, c_2), dist) in enumerate(distances):
        # print(f'>> Checking {(c_1, c_2)} with distance {dist}')
        # if i % 1000 == 0:
        #     print(f'Schritt {i}')
        found_clusters = []
        already_connected = False
        for i, cluster in enumerate(clusters):
            if c_1 in cluster and c_2 in cluster:
                # print(f'{c_1} and {c_2} already in cluster {cluster}')
                already_connected = True
                break
            if c_1 in cluster or c_2 in cluster:
                found_clusters.append(i)
                if len(found_clusters) == 2:
                    break

        connected += 1
        if already_connected:
            continue
        last_connected = (c_1, c_2)
        if len(found_clusters) == 1:
            # print(f'{(c_1, c_2)} added to cluster {clusters[found_clusters[0]]}')
            clusters[found_clusters[0]] |= {c_1, c_2}
        elif len(found_clusters) == 2:
            # print(f'{(c_1, c_2)} merged clusters {clusters[found_clusters[0]]} and {clusters[found_clusters[1]]}')
            clusters[found_clusters[0]].update(clusters[found_clusters[1]])
            clusters[found_clusters[0]] |= {c_1, c_2}
            del clusters[found_clusters[1]]
        if len(found_clusters) == 0:
            clusters.append({c_1, c_2})
            # print(f'{(c_1, c_2)} created new cluster')
        if part == 1 and connected == 1000:
            break

    if part == 2:
        # print(f'last_connected: {last_connected}')
        solution = last_connected[0][0] * last_connected[1][0]
        return solution

    # print(clusters)
    cluster_sizes = sorted([len(c) for c in clusters], reverse=True)
    solution = cluster_sizes[0] * cluster_sizes[1] * cluster_sizes[2]
    return solution

# Part 1
solution = connect_clusters(distances)
print('Solution for Part 1: ', solution)

# Part 2
solution = connect_clusters(distances, part=2)
print('Solution for Part 2: ', solution)