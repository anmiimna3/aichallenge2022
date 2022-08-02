from src import model
from typing import List, Set

class Agent:
    def __init__(self, agent: model.Agent, my_type: model.AgentType, turn : int):
        self.messages : Set[model.Chat] = {None}
        self.id : int = agent.id
        self.nodes_id : list[int] = turn - 1 *[None] + [agent.node_id]
        self.balance : List[float] = turn * [None]
        self.estimated_balance : List[float] = turn * [None] # not done yet
        self.is_dead : bool = False
        self.type : model.AgentType = agent.agent_type
        self.my_type : model.AgentType = my_type
        self.round_salary : int = 10
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.id == other.id
    
    def get_messages(self) -> List[model.Chat]:
        return self.messages
    
    def get_id(self) -> int:
        return self.id
    
    def get_nodes_id(self) -> List[int]:
        return self.nodes_id
    
    def get_balance(self) -> List[float]:
        return self.balance
    
    def get_estimated_balance(self) -> List[float]:
        return self.estimated_balance
    
    def add_message(self, message: model.Chat) -> None:
        self.messages.add(message)

    def get_last_balance(self) -> tuple:
        length = len(self.balance)
        for i in range(-1, -length - 1, -1):
            if self.balance[i] != None:
                return self.balance[i], length - i
        return None

    def get_second_last_balance(self) -> tuple:
        is_second = False
        length = len(self.balance)
        for i in range(-1, -len(self.balance) - 1, -1):
            if self.balance[i] != None:
                if is_second:
                    return self.balance[i], length - i
                else:
                    is_second = True
        return None

    
    def update_balance(self, floyd_adj : List[List[float]], round_salary : float) -> None:
        if(len(self.balance) >= 2 and self.balance[-1] != None and 
              (self.nodes_id[-1] != None and self.nodes_id[-2] != None)):

            
            self.balance.append(self.balance[-1] - floyd_adj[self.nodes_id[-1]][self.nodes_id[-2]] + round_salary)
        
        else:
            self.balance.append(None)
        
        self.estimated_balance.append(None)

    
        

    def update_all(self, view: model.GameView, floyd_adj : List[List[float]]) -> None:
        new_data : model.Agent = None
        for agent in view.visible_agents:
            if agent.id == self.id:
                new_data = agent
                break
        
        if new_data == None:
            if self.my_type == self.type:
                self.is_dead = True
                return
            
            self.nodes_id.append(None)
            
            self.update_balance(floyd_adj, self.round_salary)
        
            return 
        
        self.nodes_id.append(new_data.node_id)
        self.update_balance(floyd_adj, self.round_salary)
        for message in view.chat_box:
            if message.sender_id == self.id:
                message.turn = view.turn.turn_number
                self.messages.add(message)
        
        
            

        





        