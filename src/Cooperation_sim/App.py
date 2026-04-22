from mesa.visualization.components import AgentPortrayalStyle
from Model import OpinionDynamicsModel
from Agents import OpinionAgent
import solara
import matplotlib.pyplot as plt

from mesa.visualization.utils import update_counter

from mesa.visualization import (
    CommandConsole,
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)

def red_blue_gradient(value):
    #clamp value between 0.0 and 1.0
    value = max(0.0, min(1.0, value))
    r = int(255 * (1-value))
    g = 0
    b = int(255 * value)

    return "#"+str(hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2))

def OpinionAgent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = AgentPortrayalStyle(
        size=100,
        marker="s",
        color=red_blue_gradient(agent.opinion)
    )
    return portrayal


@solara.component
def VariancePlot(model):
    #solara.use_reactive(model)
    update_counter.get()


    df = model.datacollector.get_model_vars_dataframe()
    fig, ax = plt.subplots() # Unpack tuple

    if not df.empty:
        ax.plot(df["Opinion_variance"])

    ax.set_xlabel("Step")
    ax.set_ylabel("Variance")
    ax.set_title("Opinion Variance Over Time")

    ax.set_ylim(0, 1)  # 👈 FIXED Y-AXIS
    ax.set_xlim(0,10)

    solara.FigureMatplotlib(fig)

def post_process_lines(ax):
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.9))



variance_graph_component = make_plot_component(
    {"Opinion_variance": "tab:green"},
    post_process=post_process_lines,
)

model = OpinionDynamicsModel()

model_params = {
    "initial_agents": Slider("Number of Agents", model.scenario.initial_agents, 0, model.max_agents),
}

def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

renderer = SpaceRenderer(
    model,
    backend="matplotlib",
).setup_agents(OpinionAgent_portrayal)
renderer.post_process = post_process_space
renderer.draw_agents()

page = SolaraViz(
    model,
    renderer,
    components=[VariancePlot],
    model_params=model_params,
    name="Opinion Convergence",
)
page 
