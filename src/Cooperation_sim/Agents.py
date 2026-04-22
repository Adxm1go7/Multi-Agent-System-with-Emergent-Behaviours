from mesa.discrete_space import CellAgent, FixedAgent

class OpinionAgent(FixedAgent):

    def __init__(self, model, cell, opinion):

        super().__init__(model)

        self.cell = cell

        #Value between 0.0 - 1.0, reflects opinion
        self.opinion = opinion


    def talkToOneNeighbour(self): 
        #print(self.random.choice(self.cell.neighborhood))
        cell = self.cell.get_neighborhood(include_center=False).select_random_cell()

        if cell.agents:
            neighborAgent = cell.agents[0]
        self.opinion = (neighborAgent.opinion + self.opinion)/2

    
    def step(self):
        self.talkToOneNeighbour()



