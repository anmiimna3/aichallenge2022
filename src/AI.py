import random
from src.client import GameClient
from src.model import GameView, Agent, Path
from src.simp import get_path_limited, possible_place, get_point_thief, init_thief_locations, get_cost_adj, update_thief_locations, get_path


def get_thief_starting_node(view: GameView) -> int:
    adj = [[] for _ in range(len(view.config.graph.nodes) + 1)]
    for j in view.config.graph.paths:
        j: Path
        adj[j.first_node_id].append(j.second_node_id)
        adj[j.second_node_id].append(j.first_node_id)
    THIEF = 0
    POLICE = 1
    ans = [1] * (len(view.config.graph.nodes) + 1)
    ans[0] = 0
    opp_team = not view.viewer.team
    for i in view.visible_agents:
        i: Agent
        if i.agent_type == THIEF and i.team == view.viewer.team:
            ans[i.node_id] = 0
        if i.agent_type == POLICE and i.team == opp_team:
            k = possible_place(adj, i.node_id, 6)
            for j in k:
                ans[j] = 0
    final = []
    for i in range(len(ans)):
        if ans[i] == 1:
            final.append(i)
    return random.choice(final)


class Phone:
    def __init__(self, client: GameClient):
        self.client = client

    def send_message(self, message):
        self.client.send_message(message)


class AI:
    def __init__(self, phone: Phone):
        self.phone = phone
        self.adj = [[]]
        self.costs = [[]]
        self.prediction_values = []
        self.init = False

    def thief_move_ai(self, view: GameView) -> int:
        # write your code here
        opp_team = not view.viewer.team
        if not self.init:
            self.init = True
            self.adj = [[] for _ in range(len(view.config.graph.nodes) + 1)]
            for j in view.config.graph.paths:
                j: Path
                self.adj[j.first_node_id].append(j.second_node_id)
                self.adj[j.second_node_id].append(j.first_node_id)
            self.costs = get_cost_adj(
                view.config.graph.paths, len(view.config.graph.nodes)+1)
        ans = view.viewer.node_id
        dist = get_point_thief(
            view.visible_agents, self.adj, view.viewer.node_id, opp_team)
        for j in view.config.graph.paths:
            j: Path
            if j.first_node_id == view.viewer.node_id:
                k = get_point_thief(
                    view.visible_agents, self.adj, j.second_node_id, opp_team)
                if k >= dist:
                    dist = k
                    ans = j.second_node_id
            if j.second_node_id == view.viewer.node_id:
                k = get_point_thief(
                    view.visible_agents, self.adj, j.first_node_id, opp_team)
                if k >= dist:
                    dist = k
                    ans = j.first_node_id
        return ans

    def police_move_ai(self, view: GameView) -> int:
        if not self.init:
            self.init = True
            self.adj = [[] for _ in range(len(view.config.graph.nodes) + 1)]
            for j in view.config.graph.paths:
                j: Path
                self.adj[j.first_node_id].append(j.second_node_id)
                self.adj[j.second_node_id].append(j.first_node_id)
            self.prediction_values = [0] * (len(view.config.graph.nodes) + 1)
            self.costs = get_cost_adj(
                view.config.graph.paths, len(view.config.graph.nodes)+1)

        answer = view.viewer.node_id
        if(view.turn.turn_number < view.config.visible_turns[0]):
            THIEF = 0
            POLICE = 1
            ans = [1] * (len(view.config.graph.nodes) + 1)
            ans[0] = 0
            opp_team = not view.viewer.team
            for i in view.visible_agents:
                i: Agent
                if i.agent_type == THIEF and i.team == view.viewer.team:
                    ans[i.node_id] = 0
                if i.agent_type == POLICE and i.team == opp_team:
                    k = possible_place(self.adj, i.node_id, 6)
                    for j in k:
                        ans[j] = 0
            self.prediction_values = ans
        elif(view.turn.turn_number in view.config.visible_turns):
            init_thief_locations(view, self.prediction_values)
        else:
            update_thief_locations(view, self.prediction_values, self.adj)
        flag = False
        while not flag:
            for i in self.adj[view.viewer.node_id]:
                if(self.prediction_values[i] == 0):
                    continue
                else:
                    flag = True
                if(self.prediction_values[i] > self.prediction_values[answer] and view.balance > self.costs[i][view.viewer.node_id]):
                    answer = i
                elif(self.prediction_values[i] == self.prediction_values[answer]):
                    if(self.costs[view.viewer.node_id][i] < self.costs[view.viewer.node_id][answer]):
                        answer = i
            if(not flag):
                update_thief_locations(view, self.prediction_values, self.adj)
        return answer
