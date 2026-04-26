from mesa.discrete_space import CellAgent, FixedAgent

class OpinionAgent(FixedAgent):

    def __init__(self, model, cell, opinion, convince_range, converge_mult, is_stubborn, interaction_mode):

        super().__init__(model)

        #Grid coordinate
        self.cell = cell

        #Value between 0.0 - 1.0, reflects opinion
        self.opinion = opinion

        #Max difference between agents for opinion to converge
        self.convince_range = convince_range

        #When convinced, how much cells converge
        self.converge_mult = converge_mult
        
        #Agents opinion wont change if True
        self.is_stubborn = is_stubborn

        #Broadcasters always reflect their opinions but never converge
        self.is_broadcaster = False

        self.interaction_mode = interaction_mode


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

    def talkToAllNeighboursHK(self):
        """
        Hegselmann-Krause rule.
        Agent averages opinions of ALL neighbours within convince_range equally.
        No weighting.
        """
        if self.is_stubborn:
            return

        eligible = []
        for cell in self.cell.get_neighborhood(include_center=False).cells:
            if cell.agents:
                neighbour = cell.agents[0]
                if abs(self.opinion - neighbour.opinion) <= self.convince_range:
                    eligible.append(neighbour)

        if not eligible:
            return

        # Simple unweighted average of all in-range neighbours
        avg = sum(n.opinion for n in eligible) / len(eligible)
        new_opinion = self.opinion + self.converge_mult * (avg - self.opinion)

        if self.model.scenario.opinion_type != "continuous":
            new_opinion = self.snap_to_discrete(new_opinion)

        self.opinion = new_opinion


    def talkToAllNeighboursWeighted(self):
        """
        Weighted neighbour averaging (My idea).
        Neighbours with closer opinions have more influence.
        Agents outside convince_range are still ignored entirely (HK boundary).
        Weight = 1 / (distance + epsilon) so identical opinions have highest weight.
        """
        if self.is_stubborn:
            return

        eligible   = []
        weights    = []

        for cell in self.cell.get_neighborhood(include_center=False).cells:
            if cell.agents:
                neighbour = cell.agents[0]
                diff = abs(self.opinion - neighbour.opinion)
                if diff <= self.convince_range:
                    eligible.append(neighbour)
                    # Closer opinions = higher weight
                    weights.append(1.0 / (diff + 1e-6)) # Prevent / 0 by adding really small number

        if not eligible:
            return

        # Normalise so weights sum to 1
        total      = sum(weights)
        normalised = [w / total for w in weights]

        # Weighted average
        weighted_avg = sum(n.opinion * w for n, w in zip(eligible, normalised))
        new_opinion  = self.opinion + self.converge_mult * (weighted_avg - self.opinion)

        if self.model.scenario.opinion_type != "continuous":
            new_opinion = self.snap_to_discrete(new_opinion)

        self.opinion = new_opinion



        
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
        mode = self.interaction_mode

        if mode == "single":
            self.talkToOneNeighbour()
        elif mode == "all_hk":
            self.talkToAllNeighboursHK()
        elif mode == "all_weighted":
            self.talkToAllNeighboursWeighted()




class BroadcastAgent(OpinionAgent):
    """
    A stubborn broadcaster that pushes its opinion to all neighbours
    every step. Never updates its own opinion.
    """

    def __init__(self, model, cell, opinion, convince_range, converge_mult):
        # is_stubborn=True so it never updates its own opinion
        super().__init__(model, cell, opinion, convince_range, converge_mult, is_stubborn=True)
        self.is_broadcaster = True

    def broadcast(self):
        # Push opinion to all neighbours within range
        neighborhood = self.cell.get_neighborhood(include_center=False)

        for cell in neighborhood.cells:
            if cell.agents:
                neighbour = cell.agents[0]
                # Broadcasters bypass convince_range
                if not neighbour.is_stubborn and not neighbour.is_broadcaster:
                    neighbour.opinion = neighbour.opinion + self.converge_mult * (self.opinion - neighbour.opinion)

                    if self.model.scenario.opinion_type != "continuous":
                        neighbour.opinion = neighbour.snap_to_discrete(neighbour.opinion)

    def step(self):
        self.broadcast()