#uvicorn server:app --reload

t = [1,2,3,4]
print(range(len(t)))


t = -1
print(abs(t))




"""
"Opinion_mean": lambda m: float(np.mean([a.opinion for a in m.agents])),

            "Polarisation": lambda m: float(
                np.mean([1 for a in m.agents if a.opinion < 0.2 or a.opinion > 0.8])
                / max(len(list(m.agents)), 1)
            ),

            # Grid snapshot: list of (row, col, opinion) for heatmap
            "Grid_opinions": lambda m: [
                (a.cell.coordinate[0], a.cell.coordinate[1], a.opinion)
                for a in m.agents
            ],


            
@solara.component
def PolarisationPlot(model):
    update_counter.get()
    
    df = model.datacollector.get_model_vars_dataframe()

    fig, ax = plt.subplots(figsize=(5, 2.8))
    ax.set_facecolor("#f7f7f7")

    if not df.empty and "Polarisation" in df.columns:
        steps = range(len(df))
        pol = df["Polarisation"]
        ax.plot(steps, pol, color="#d62728", linewidth=1.8)
        ax.fill_between(steps, pol, alpha=0.12, color="#d62728")

        # Also overlay mean opinion as a secondary line (right y-axis)
        if "Opinion_mean" in df.columns:
            ax2 = ax.twinx()
            ax2.plot(steps, df["Opinion_mean"], color="#1f77b4",
                     linewidth=1.2, linestyle="--", alpha=0.7)
            ax2.set_ylim(0, 1)
            ax2.set_ylabel("Mean opinion", fontsize=8, color="#1f77b4")
            ax2.tick_params(labelsize=7, colors="#1f77b4")

    ax.set_xlabel("Step", fontsize=9)
    ax.set_ylabel("Polarisation index", fontsize=9)
    ax.set_title("Polarisation & Mean Opinion Over Time", fontsize=10)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=8)
    fig.tight_layout()

    solara.FigureMatplotlib(fig)
    plt.close(fig)





@solara.component
def HeatmapPlot(model):
    update_counter.get()

    df = model.datacollector.get_model_vars_dataframe()

    solara.use_reactive(len(df))

    fig, ax = plt.subplots(figsize=(5, 5))

    # Build opinion matrix; NaN = empty cell
    grid_data = np.full((model.height, model.width), np.nan)

    if not df.empty and "Grid_opinions" in df.columns:
        snapshot = df["Grid_opinions"].iloc[-1]
        for row, col, opinion in snapshot:
            grid_data[row][col] = opinion

    # Custom colourmap: grey for NaN, red→blue for opinions
    rb_cmap = mcolors.LinearSegmentedColormap.from_list(
        "rb", ["#d62728", "#9467bd", "#1f77b4"]
    )
    rb_cmap.set_bad(color="#e0e0e0")   # empty cells → light grey

    im = ax.imshow(
        grid_data,
        cmap=rb_cmap,
        vmin=0.0,
        vmax=1.0,
        interpolation="nearest",
        origin="upper",
    )

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Opinion", fontsize=10)
    cbar.ax.tick_params(labelsize=9)

    ax.set_title("Spatial Opinion Map (current step)", fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()

    solara.FigureMatplotlib(fig)
    plt.close(fig)
    
    """