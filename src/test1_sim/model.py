import mesa
from agents import MovingAgent

class MyModel(mesa.Model):
    def __init__(self, n=1):
        super().__init__()
        self.num_agents=n
        self.space= mesa.experimental.continuous_space.ContinuousSpace(
            [[0, 10], [0, 10]],
            torus=True,
            random=self.random,
            n_agents=n,
        )

        agents = MovingAgent.create_agents(self, self.num_agents,[0,0], "blue")
    

    def step(self):
        self.agents.shuffle_do("step")



