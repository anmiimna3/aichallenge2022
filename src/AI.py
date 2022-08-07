import random
from src import model
from src.client import GameClient
from src.hide_and_seek_pb2 import THIEF
from src.model import GameView, Team, Agent, AgentType, Node, Path
from src import simp


def get_thief_starting_node(view: GameView) -> int:
    adj = [[] for _ in range(len(view.config.graph.nodes) + 1)]
    for j in view.config.graph.paths:
        j: Path
        adj[j.first_node_id].append(j.second_node_id)
        adj[j.second_node_id].append(j.first_node_id)
    FIRST = 0
    SECOND = 1
    THIEF = 0
    POLICE = 1
    ans = [1] * (len(view.config.graph.nodes) + 1)
    ans[0] = 0
    opp_team = FIRST if view.viewer.team == SECOND else SECOND
    for i in view.visible_agents:
        i: Agent
        if i.agent_type == THIEF and i.team == 1 - opp_team:
            ans[i.node_id] = 0
        if i.agent_type == POLICE and i.team == opp_team:
            k = simp.possible_place(adj, i.node_id, 6)
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
        self.init = False

    def thief_move_ai(self, view: GameView) -> int:
        # write your code here
        FIRST = 0
        SECOND = 1
        opp_team = FIRST if view.viewer.team == SECOND else SECOND
        if not self.init:
            self.init = True
            self.adj = [[] for _ in range(len(view.config.graph.nodes) + 1)]
            for j in view.config.graph.paths:
                j: Path
                self.adj[j.first_node_id].append(j.second_node_id)
                self.adj[j.second_node_id].append(j.first_node_id)

        ans = view.viewer.node_id
        dist = simp.get_point_thief_one(view.visible_agents, self.adj, view.viewer.node_id, opp_team)
        for j in view.config.graph.paths:
            j: Path
            if j.first_node_id == view.viewer.node_id:
                k = simp.get_point_thief_one(view.visible_agents, self.adj, j.second_node_id, opp_team)
                if k >= dist:
                    dist = k
                    ans = j.second_node_id
            if j.second_node_id == view.viewer.node_id:
                k = simp.get_point_thief_one(view.visible_agents, self.adj, j.first_node_id, opp_team)
                if k >= dist:
                    dist = k
                    ans = j.first_node_id
        return ans

    def police_move_ai(self, view: GameView) -> int:
        ans = []
        for i in view.config.graph.paths:
            i: Path
            if i.first_node_id == view.viewer.node_id:
                ans.append(i.second_node_id)
            if i.second_node_id == view.viewer.node_id:
                ans.append(i.first_node_id)
        return random.choice(ans)
