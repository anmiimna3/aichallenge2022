from typing import List
import src.model


def get_path(graph, src, dest):
    adj = [[] for i in range(len(graph) + 1)]
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if(graph[i][j] != float('inf')):
                adj[i].append(j)
                adj[j].append(i)
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


def get_point_thief_one(visible_agents, costs, node_id, opposite_team):
    POLICE = 1
    min_len = 1000000
    for i in visible_agents:
        i: src.model.Agent
        if i.team == opposite_team and i.agent_type == POLICE:
            ans = get_path(costs, node_id, i.node_id)
            if len(ans) < min_len:
                min_len = len(ans)
                print("agent " + str(i.id) + " is close!")
    return min_len


def get_point_thief_all(visible_agents, costs, opposite_team, graph: src.model.Graph):
    ans = [0] * (len(graph.nodes) + 1)
    for i in graph.nodes:
        i: src.model.Node
        ans[i.id] = get_point_thief_one(
            visible_agents, costs, i.id, opposite_team)
        print("this is point of " + str(i.id) + ": " + str(ans[i.id]))
    return ans


def get_cost_adj(paths, nodes_count: int) -> List[List[float]]:

    adj = [[float("inf") for _ in range(nodes_count)]
           for _ in range(nodes_count)]
    for path in paths:
        path: src.model.Path
        adj[path.first_node_id][path.second_node_id] = path.price
        adj[path.second_node_id][path.first_node_id] = path.price

    for i in range(nodes_count):
        adj[i][i] = 0

    return adj
