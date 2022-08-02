from typing import List, Union


num = Union[int, float]

def get_floyd(graph : List[List[num]], V : int) -> List[List[num]]:

    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))

    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = min(dist[i][j],
                                 dist[i][k] + dist[k][j])

    return dist
