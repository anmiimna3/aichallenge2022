import optparse
from src import model
from src.client import GameClient
from src.model import GameView, Team, Agent, AgentType, Node, Path
from src import simp


def get_thief_starting_node(view: GameView) -> int:
    # write your code here
    return 2


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
            self.adj = simp.get_cost_adj(view.config.graph.paths, len(view.config.graph.nodes) + 1)
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
        # write your code here       
        self.phone.send_message('00101001')
        return 1
