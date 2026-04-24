from mesa import Model
from mesa.experimental.scenarios import Scenario
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.datacollection import DataCollector

import numpy as np

from Agents import OpinionAgent


class OpinionScenario(Scenario):
    grid_length: int = 80
    initial_agents: int = grid_length
    convince_range: int = 0.25


class OpinionDynamicsModel(Model):
    description = "A model for simulating opinion convergence"
    def __init__(self, scenario=None):

        if scenario is None:
            scenario = OpinionScenario()

        super().__init__(scenario=scenario)
        # Size of simulation component
        self.fig_height = 6
        self.fig_width = 6

        self.grid_length = scenario.grid_length

        self.cell_size_multipliers = [2970, 1300, 570, 430, 380, 340, 280, 240, 200, 170]
        self.display_size = (self.fig_width * self.cell_size_multipliers[(self.grid_length//10) - 1] / self.grid_length)

        self.initial_agents = self.grid_length ** 2

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
            self.initial_agents,
            self.random.sample(
                self.grid.all_cells.cells, k=self.initial_agents
            ),
            [self.random.uniform(0.0, 1.0) for _ in range(self.initial_agents)],
            scenario.convince_range
        )

        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        print(self.cell_size_multipliers[(self.grid_length//10) - 1])
        print(self.grid_length)
        print(self.display_size)
