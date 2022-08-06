import model

def get_point_thief_one(visible_agents, costs, node_id, opposite_team):
    min_len = 1000000
    for i in visible_agents:
        if i.team == opposite_team and i.agent_type == model.AgentType.POLICE:
            ans = get_path(costs, node_id, i.node_id)
            if len(ans) > min_len:
                min_len = len(ans)
    return min_len



def get_point_thief_all(visible_agents, costs, opposite_team, graph):
    ans = [0] * len(graph.nodes)
    for i in graph.nodes:
        ans[i.id] = get_point_thief_one(visible_agents, costs, i.id, opposite_team)
    return ans