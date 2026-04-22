from mesa.discrete_space import CellAgent, FixedAgent

class OpinionAgent(FixedAgent):

    def __init__(self, model, cell, opinion, convince_range):

        super().__init__(model)

        self.cell = cell

        #Value between 0.0 - 1.0, reflects opinion
        self.opinion = opinion

        self.convince_range = convince_range


    def talkToOneNeighbour(self): 
        cell = self.cell.get_neighborhood(include_center=False).select_random_cell()

        if cell.agents:
            neighborAgent = cell.agents[0]
            if (abs(self.opinion - neighborAgent.opinion) < self.convince_range):
                self.opinion = (neighborAgent.opinion + self.opinion)/2

    
    def step(self):
        self.talkToOneNeighbour()



