import model

def get_path(graph, src, dest):
    adj = [[] for i in range(len(graph))]
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
    min_len = 1e5
    for i in visible_agents:
        i: model.Agent
        if i.team == opposite_team and i.agent_type == model.AgentType.POLICE:
            ans = get_path(costs, node_id, i.node_id)
            if len(ans) > min_len:
                min_len = len(ans)
    return min_len


def get_point_thief_all(visible_agents, costs, opposite_team, graph: model.Graph):
    ans = [0] * len(graph.nodes)
    for i in graph.nodes:
        i: model.Node
        ans[i.id] = get_point_thief_one(
            visible_agents, costs, i.id, opposite_team)
    return ans
