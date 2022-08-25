from itertools import count
from typing import List
from src.model import GameView, Path, Agent, Node, Graph


def get_path(adj, src, dest) -> List[int]:
    v = len(adj)
    pred = [0 for i in range(v)]
    dist = [0 for i in range(v)]
    queue = []
    visited = [False for i in range(v)]
    for i in range(v):
        dist[i] = 1e5
        pred[i] = -1
    visited[src] = True
    dist[src] = 0
    queue.append(src)
    while (len(queue) != 0):
        u = queue[0]
        queue.pop(0)
        for i in range(len(adj[u])):
            if (visited[adj[u][i]] == False):
                visited[adj[u][i]] = True
                dist[adj[u][i]] = dist[u] + 1
                pred[adj[u][i]] = u
                queue.append(adj[u][i])
                if (adj[u][i] == dest):
                    path = []
                    crawl = dest
                    crawl = dest
                    path.append(crawl)
                    while (pred[crawl] != -1):
                        path.append(pred[crawl])
                        crawl = pred[crawl]
                    return path[::-1]
    return []


def get_point_thief(visible_agents, adj, node_id, opposite_team) -> int:
    POLICE = 1
    min_len = 1000000
    for i in visible_agents:
        i: Agent
        if i.team == opposite_team and i.agent_type == POLICE:
            ans = get_path(adj, node_id, i.node_id)
            if len(ans) < min_len:
                min_len = len(ans)
    return min_len


def get_cost_adj(paths, nodes_count: int) -> List[List[float]]:
    adj = [[float("inf") for _ in range(nodes_count)]
           for _ in range(nodes_count)]
    for path in paths:
        path: Path
        adj[path.first_node_id][path.second_node_id] = path.price
        adj[path.second_node_id][path.first_node_id] = path.price

    for i in range(nodes_count):
        adj[i][i] = 0

    return adj


def possible_place(adj: List[List[int]], node_id: int, number_of_rounds: int) -> List[int]:
    visited = [node_id]
    queue = [[node_id, 0]]
    while queue:
        temp = queue[0]
        queue.pop(0)
        if temp[1] == number_of_rounds:
            continue
        for i in adj[temp[0]]:
            if i not in visited:
                visited.append(i)
                ans = [i, temp[1] + 1]
                queue.append(ans)
    return visited


def update_thief_locations(view: GameView, prediction_values: List[int], adj: List[List[int]]):
    temp = []
    for i in range(1, len(view.config.graph.nodes)+1):
        if prediction_values[i] > 0:
            for j in adj[i]:
                if prediction_values[j] == 0:
                    temp.append(j)
            prediction_values[i] += 1
    for i in temp:
        prediction_values[i] += 1


def init_thief_locations(view: GameView, prediction_values):
    THIEF = 0
    opp_team = not view.viewer.team
    for i in view.visible_agents:
        i: Agent
        if i.agent_type == THIEF and i.team == opp_team:
            prediction_values[i.node_id] = 1
        else:
            prediction_values[i.node_id] = 0


def get_path_limited(adj, src, dest, money, costs) -> List[int]:
    v = len(adj)
    pred = [0 for _ in range(v)]
    dist = [0 for _ in range(v)]
    costs_from_src = [0 for _ in range(v)]
    queue = []
    visited = [False for i in range(v)]
    for i in range(v):
        dist[i] = 1e5
        pred[i] = -1
        costs_from_src[i] = 1e5
    costs_from_src[src] = 0
    visited[src] = True
    dist[src] = 0
    queue.append(src)
    while (len(queue) != 0):
        u = queue[0]
        queue.pop(0)
        for i in range(len(adj[u])):
            if (visited[adj[u][i]] == False and costs_from_src[u] + costs[u][adj[u][i]] <= money):
                visited[adj[u][i]] = True
                dist[adj[u][i]] = dist[u] + 1
                pred[adj[u][i]] = u
                costs_from_src[adj[u][i]] = costs_from_src[u] + costs[u][adj[u][i]]
                queue.append(adj[u][i])
                if (adj[u][i] == dest):
                    path = []
                    crawl = dest
                    crawl = dest
                    path.append(crawl)
                    while (pred[crawl] != -1):
                        path.append(pred[crawl])
                        crawl = pred[crawl]
                    return path[::-1]
    return []

def get_closest_thief(view: GameView, adj: List[int], costs: List[List[int]]) -> int:
    ans = 0
    ansList = [0]*1000
    temp = []
    for i in view.visible_agents:
        i: Agent
        if i.agent_type != view.viewer.agent_type and i.team != view.viewer.team and i.is_dead == False:
            temp = get_path_limited(adj, view.viewer.node_id, i.node_id, view.balance, costs)
            if 0 < len(temp) < len(ansList):
                ans = i.node_id
                ansList = temp
    return ans