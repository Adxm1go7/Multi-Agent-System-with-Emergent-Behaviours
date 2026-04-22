import mesa
import mesa.visualization

from agents import MovingAgent
from model import MyModel

def agent_portrayal(agent):
    return mesa.visualization.components.AgentPortrayalStyle(color="tab:orange",size=50)

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 1,
        "label": "Number of Agents",
        "min": 1,
        "max": 10,
        "step": 1,
    },

}

newModel = MyModel()

renderer = (
    mesa.visualization.SpaceRenderer(newModel, backend="matplotlib")
    .setup_agents(agent_portrayal)
    .render()
)

page = mesa.visualization.SolaraViz(
    newModel,
    renderer,
    model_params=model_params,
    name="Test 1",
)
# This is required to render the visualization in the Jupyter notebook
page