from src.memory import agent
from typing import Set, List

from src import game, model
from src import algorithms

class Memory:
    def __init__(self):
        self.agents : Set[agent.Agent] = set()

        self.is_setup : bool =   False
        self.nodes_count : int

        self.adj : List[List[float]] = []
        self.cost_adj : List[List[float]] = []

        self.floyd_adj : List[List[float]] = []
        self.floyd_cost_adj : List[List[float]] = []

        self.my_type : model.AgentType = None


    def setup(self, game : game.Game):
        if not self.is_setup:
            self.nodes_count = game.get_nodes_count()

            self.adj = game.get_adj(self.nodes_count)
            self.cost_adj = game.get_cost_adj(self.nodes_count)

            self.floyd_adj = algorithms.get_floyd(self.adj, self.nodes_count)
            self.floyd_cost_adj = algorithms.get_floyd(self.cost_adj, self.nodes_count)

            self.my_type = game.view.viewer.agent_type
            self.is_setup = True

    def update(self, game : game.Game):
        self.setup()
        for age in game.get_visible_agents():
            age = agent.Agent(age,self.my_type , game.get_turn().turn_number)
            self.agents.add(age)

        for age in self.agents:
            age.update_all(game.view, self.floyd_cost_adj)





