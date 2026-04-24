from mesa.discrete_space import CellAgent, FixedAgent

class OpinionAgent(FixedAgent):

    def __init__(self, model, cell, opinion, convince_range, converge_mult, is_stubborn):

        super().__init__(model)

        self.cell = cell

        #Value between 0.0 - 1.0, reflects opinion
        self.opinion = opinion
        #Max difference when opinion converges
        self.convince_range = convince_range
        #When convinced, how much cells converge
        self.converge_mult = converge_mult

        self.is_stubborn = is_stubborn


    def talkToOneNeighbour(self): 
        cell = self.cell.get_neighborhood(include_center=False).select_random_cell()

        if cell.agents:
            neighborAgent = cell.agents[0]

            if (abs(self.opinion - neighborAgent.opinion) <= self.convince_range):
                if not self.is_stubborn:
                    if self.model.scenario.opinion_type == "continuous":
                        self.opinion = self.opinion + self.converge_mult * (neighborAgent.opinion - self.opinion)

                    else:
                        new_opinion = self.opinion + self.converge_mult * (neighborAgent.opinion - self.opinion)
                        self.opinion = self.snap_to_discrete(new_opinion)
        
    def snap_to_discrete(self, value):
        valid = {
            "binary":    [0.0, 1.0],
            "ternary":   [0.0, 0.5, 1.0],
            "quadrary":  [0.0, 0.33, 0.67, 1.0],
        }
        options = valid[self.model.scenario.opinion_type]

        closest = options[0]
        for x in range(1, len(options)):
            if (abs(options[x] - value) == abs(closest - value)):
                closest = self.random.choice([options[x], closest])
            elif (abs(options[x] - value) < abs(closest - value)):
                closest = options[x]

        return closest

    
    def step(self):
        self.talkToOneNeighbour()



