from src import model

class Game:
    def __init__(self, view : model.GameView):
        self.view : model.GameView = view
    
    def get_status(self) -> model.GameStatus:
        return self.view.status
    
    def get_result(self) -> model.GameResult:
        return self.view.result
    
    def get_turn(self) -> model.Turn:
        return self.view.turn
    
    def get_config(self) -> model.GameConfig:
        return self.view.config
    
    def get_viewer(self) -> model.Agent:
        return self.view.viewer
    
    def get_balance(self) -> float:
        return self.view.balance
    
    def get_visible_agents(self) -> list(model.Agent):
        return self.view.visible_agents
    
    def get_chat_box(self) -> list(model.Chat):
        return self.view.chat_box
    
    def get_graph(self) -> model.Graph:
        return self.get_config().graph
    
    def get_paths(self) -> list(model.Path):
        return self.get_graph().paths
    
    def get_nodes(self) -> list(model.Node):
        return self.get_graph().nodes
    
    def get_nodes_count(self) -> int:
        return len(self.get_nodes())
    
    def get_cost_adj(self) -> list(float):
        nodes_count = self.get_nodes_count()
        adj = [[float("inf") for _ in range(nodes_count)] for _ in range(nodes_count)]
        for path in self.get_paths():
            adj[path.node1][path.node2] = path.price
            adj[path.node2][path.node1] = path.price
        
        for i in range(nodes_count):
            adj[i][i] = 0
        
        return adj
    
    def get_adj(self) -> list(int):
        nodes_count = self.get_nodes_count()
        adj = [[float("inf") for _ in range(nodes_count)] for _ in range(nodes_count)]
        for path in self.get_paths():
            adj[path.node1][path.node2] = 1
            adj[path.node2][path.node1] = 1
        
        for i in range(nodes_count):
            adj[i][i] = 0
        
        return adj
    
    def get_agent_by_id(self, id : int) -> model.Agent:
        for agent in self.get_visible_agents():
            if agent.id == id:
                return agent
        return None

