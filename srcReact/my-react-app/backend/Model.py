from mesa import Model
from mesa.experimental.scenarios import Scenario
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.datacollection import DataCollector

import numpy as np

from Agents import OpinionAgent


class OpinionScenario(Scenario):
    grid_length: int = 10
    n_agents: int = grid_length ** 2
    convince_range: int = 0.25
    converge_mult: int = 0.3
    opinion_type: str = "continuous"
    stubborn_fraction: float = 0.0

    bias: float = 0.5
    bias_strength: float = 0.0


class OpinionDynamicsModel(Model):
    description = "A model for simulating opinion convergence"
    def __init__(self, scenario=None):

        if scenario is None:
            scenario = OpinionScenario()

        super().__init__(scenario=scenario)

        self.grid_length = scenario.grid_length

        self.n_agents = self.grid_length ** 2

        self.grid = OrthogonalMooreGrid(
            [self.grid_length, self.grid_length],
            torus=True,
            capacity=1,
            random=self.random,
        )

        model_reporters = {
            "Opinions": lambda m: [a.opinion for a in m.agents],

            "Opinion_variance": lambda m: float(np.var([a.opinion for a in m.agents])),
        }

        self.datacollector = DataCollector(model_reporters)

        OpinionAgent.create_agents(
            self,
            self.n_agents,
            self.random.sample(
                self.grid.all_cells.cells, k=self.n_agents
            ),
            [self.generate_opinion(scenario.opinion_type, scenario.bias, 
            scenario.bias_strength) for _ in range(self.n_agents)],
            scenario.convince_range,
            scenario.converge_mult,
            self.assign_stubborn(self.n_agents, scenario.stubborn_fraction)
        )

        self.datacollector.collect(self)

    def assign_stubborn(self, n_agents, stubborn_fraction):
        n_stubborn = round(n_agents * stubborn_fraction)
        flags = [True] * n_stubborn + [False] * (n_agents - n_stubborn)
        self.random.shuffle(flags)
        return flags
    """ 
    def generate_opinion(self, opinion_type):
        if opinion_type == "continuous":
            return self.random.uniform(0.0, 1.0)
        elif opinion_type == "binary":
            return self.random.choice([0.0, 1.0])
        elif opinion_type == "ternary":
            return self.random.choice([0.0, 0.5, 1.0])
        elif opinion_type == "quadrary":
            return self.random.choice([0.0, 0.33, 0.67, 1.0])
    """       

    def generate_opinion(self, opinion_type, bias, bias_strength):
        if bias_strength == 0.0:
            # No bias — purely uniform random as before
            raw = self.random.uniform(0.0, 1.0)
        else:
            # Beta distribution centred on bias
            # Higher bias_strength = tighter cluster around bias value
            strength = 1 + bias_strength * 19  # scale 0-1 → 1-20
            alpha = strength * bias + 1e-6
            beta  = strength * (1 - bias) + 1e-6
            raw = np.random.beta(alpha, beta)

        if opinion_type == "continuous":
            return raw
        elif opinion_type == "binary":
            return 0.0 if raw < bias else 1.0
        elif opinion_type == "ternary":
            return self.snap_to_nearest(raw, [0.0, 0.5, 1.0])
        elif opinion_type == "quadrary":
            return self.snap_to_nearest(raw, [0.0, 0.33, 0.67, 1.0])

    def snap_to_nearest(self, value, options):
        return min(options, key=lambda v: abs(v - value))

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        print(self.scenario.converge_mult)

