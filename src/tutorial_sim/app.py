from matplotlib.markers import MarkerStyle

from mesa.examples.basic.boid_flockers.model import BoidFlockers, BoidsScenario
from mesa.visualization import Slider, SolaraViz, SpaceRenderer, make_space_component, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

from model import MyModel

def agent_portrayal(agent):
    return AgentPortrayalStyle(color="blue", size=50)

model_params = {
    "n_agents": Slider(
        label="Number of agents:",
        value=50,
        min=1,
        max=100,
        step=1
    )
}

def draw_agents(agent):
    agent_style = AgentPortrayalStyle(
        color = "blue", size=20, marker="o"
    )

    return agent_style


model = MyModel(n_agents=5)

renderer = (
    SpaceRenderer(
        model,
        backend="matplotlib",
    )
    .setup_agents(draw_agents)
    .render()
)


page = SolaraViz(
    model,
    renderer,
    model_params=model_params,
    name="Test",
)
page