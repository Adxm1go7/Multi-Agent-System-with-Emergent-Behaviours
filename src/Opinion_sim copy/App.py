import solara
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from mesa.visualization.utils import update_counter

from mesa.visualization.components import AgentPortrayalStyle
from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
)

from Model import OpinionDynamicsModel
from Agents import OpinionAgent


model = OpinionDynamicsModel()

# COMPONENTS

@solara.component
def VariancePlot(model):
    update_counter.get() # Updates graph with step


    df = model.datacollector.get_model_vars_dataframe()

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_facecolor("white")

    if not df.empty and "Opinion_variance" in df.columns:
        steps = range(len(df))
        ax.plot(steps, df["Opinion_variance"], color="red", linewidth=2)
        ax.fill_between(steps, df["Opinion_variance"], alpha=0.15, color="red")

    ax.set_xlabel("Step", fontsize=12)
    ax.set_ylabel("Variance", fontsize=12)
    ax.set_title("Opinion Variance Over Time", fontsize=12)
    ax.set_ylim(0, 0.2)          # theoretical max variance for uniform [0,1] = 0.083
    ax.tick_params(labelsize=10)

    fig.tight_layout()

    solara.FigureMatplotlib(fig)
    plt.close(fig)



@solara.component
def HistogramPlot(model):
    update_counter.get()

    df = model.datacollector.get_model_vars_dataframe()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_facecolor("white")

    if not df.empty and "Opinions" in df.columns:
        # Use the most recent row
        opinions = df["Opinions"].iloc[-1]

        # Build a red to blue colormap for the bars
        cmap = mcolors.LinearSegmentedColormap.from_list(
            "rb", ["#d62728", "#9467bd", "#1f77b4"]
        )
        n_bins = 20
        counts, bin_edges = np.histogram(opinions, bins=n_bins, range=(0, 1))
        bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
        bar_colours = [cmap(c) for c in bin_centres]

        ax.bar(
            bin_centres,
            counts,
            width=1 / n_bins * 0.9,
            color=bar_colours,
            edgecolor="white",
            linewidth=0.4,
        )

    ax.set_xlabel("Opinion (0 = red, 1 = blue)", fontsize=9)
    ax.set_ylabel("Agent count", fontsize=9)
    ax.set_title("Opinion Distribution (current step)", fontsize=10)
    ax.set_xlim(0, 1)
    ax.tick_params(labelsize=8)
    fig.tight_layout()

    solara.FigureMatplotlib(fig)
    plt.close(fig)


def red_blue_gradient(value):
    # Map opinion [0,...,1] to hex colour: 0 = red, 1 = blue
    value = max(0.0, min(1.0, value))
    r = int(255 * (1 - value))
    g = 0
    b = int(255 * value)
    return "#" + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

def OpinionAgent_portrayal(agent):
    if agent is None:
        return


    return AgentPortrayalStyle(
        size=model.display_size,
        marker="s",
        color=red_blue_gradient(agent.opinion),
    )

def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    #ax.imshow(model.grid, interpolation="nearest", aspect="equal")

    ax.figure.set_size_inches(model.fig_width, model.fig_height)

model_params = {
    "grid_length": Slider(
        "Grid Size",
        model.grid_length,
        10, 
        100,
        10
    )
}

renderer = SpaceRenderer(
    model,
    backend="matplotlib",
)
renderer.setup_agents(OpinionAgent_portrayal)
renderer.post_process = post_process_space
renderer.draw_agents()

page = SolaraViz(
    model,
    renderer,
    components=[
        (HistogramPlot, 1),
        (VariancePlot, 1), 
    ],
    model_params=model_params,
    name="Opinion Convergence",
)

page
