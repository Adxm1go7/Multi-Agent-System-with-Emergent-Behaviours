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

        self.is_broadcaster = False


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




class BroadcastAgent(OpinionAgent):
    """
    A stubborn broadcaster that pushes its opinion to all neighbours
    every step. Never updates its own opinion.
    Models media influence or opinion leaders.
    """

    def __init__(self, model, cell, opinion, convince_range, converge_mult):
        # is_stubborn=True so it never updates its own opinion
        super().__init__(model, cell, opinion, convince_range, converge_mult, is_stubborn=True)
        self.is_broadcaster = True

    def broadcast(self):
        """Push opinion to all neighbours within range."""
        neighborhood = self.cell.get_neighborhood(include_center=False)

        for cell in neighborhood.cells:
            if cell.agents:
                neighbour = cell.agents[0]
                # Broadcasters bypass convince_range — always influence
                if not neighbour.is_stubborn and not neighbour.is_broadcaster:
                    neighbour.opinion = neighbour.opinion + self.converge_mult * (self.opinion - neighbour.opinion)

                    # Snap if discrete mode
                    if self.model.scenario.opinion_type != "continuous":
                        neighbour.opinion = neighbour.snap_to_discrete(neighbour.opinion)

    def step(self):
        # Broadcast to all neighbours instead of talking to one
        self.broadcast()