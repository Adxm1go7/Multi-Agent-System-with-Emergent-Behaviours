import mesa
import numpy as np

import matplotlib.pyplot as plt

from agents import MyAgent


class MyModel(mesa.Model):
    def __init__(self, n_agents):
        super().__init__()
        self.grid = mesa.discrete_space.OrthogonalMooreGrid((10, 10), torus=False)
        initial_ages = self.rng.integers(0,100,size=n_agents)   
        positions = (self.rng.random(10))

        self.datacollector = mesa.DataCollector(
            model_reporters={"mean_age": lambda m: m.agents.agg("age", np.mean)},
            agent_reporters={"age": "age"}
        )

        MyAgent.create_agents(self, n_agents, initial_ages, position=positions)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

"""
model = MyModel(n_agents=5)
model.run_for(2)
model_df = model.datacollector.get_model_vars_dataframe()
agent_df = model.datacollector.get_agent_vars_dataframe()


print(model_df)
print(agent_df)
model_df["mean_age"].plot()
plt.show()
"""

