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
        FlagSolo = True
        FlagMin = True
        for i in view.visible_agents:
            i: Agent
            if i.agent_type == view.viewer.agent_type and i.team == view.viewer.team:
                if i.node_id == view.viewer.node_id:
                    FlagSolo = False
                    if i.id < view.viewer.id:
                        FlagMin = False
        if(view.turn in view.config.visible_turns):
            self.destination = get_closest_thief(view, self.adj, self.costs)
        elif(self.destination == view.viewer.node_id):
            self.destination = 0

        if(self.destination == 0 or (FlagSolo == False and FlagMin == True)):
            candidate = random.choice(self.adj[view.viewer.node_id])
            while self.costs[view.viewer.node_id][candidate] > view.balance:
                candidate = random.choice(self.adj[view.viewer.node_id])
            return candidate

        else:
            temp = get_path_limited(self.adj, view.viewer.node_id, self.destination, view.balance, self.costs)
            if len(temp):
                return temp[1]
        return view.viewer.node_id