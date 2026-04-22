from mesa import Model
from mesa.experimental.scenarios import Scenario
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.datacollection import DataCollector

import numpy as np

from Agents import OpinionAgent


class OpinionScenario(Scenario):
    width: int = 20
    height: int = 20
    initial_agents: int = 400
    convince_range: int = 0.25


class OpinionDynamicsModel(Model):
    description = "A model for simulating opinion convergence"

    def __init__(self, scenario=None):

        if scenario is None:
            scenario = OpinionScenario()

        super().__init__(scenario=scenario)

        self.height = scenario.height
        self.width = scenario.width
        self.max_agents = self.height * self.width

        self.grid = OrthogonalMooreGrid(
            [self.height, self.width],
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
            scenario.initial_agents,
            self.random.sample(
                self.grid.all_cells.cells, k=scenario.initial_agents
            ),
            [self.random.uniform(0.0, 1.0) for _ in range(scenario.initial_agents)],
            scenario.convince_range
        )

        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
