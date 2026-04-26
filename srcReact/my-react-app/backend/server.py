from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Model import OpinionDynamicsModel, OpinionScenario

import numpy as np

from pydantic import BaseModel

from typing import Optional

app = FastAPI()

# Allow React dev server to talk to this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Global
model = OpinionDynamicsModel()

def serialize_grid(model):
    """Pull agent positions and opinions out of the Mesa model."""
    current_variance = float(np.var([a.opinion for a in model.agents]))

    return {
        "step": model.steps,
        "grid_length": model.grid_length,
        "seed": model.scenario.seed,
        "variance_history":model.variance_history,
        "agents": [
            {
                "row": a.cell.coordinate[0],
                "col": a.cell.coordinate[1],
                "opinion": a.opinion,
                "is_stubborn": a.is_stubborn,
                "is_broadcaster": getattr(a, "is_broadcaster", False),
            }
            for a in model.agents
        ]
    }

class ResetParams(BaseModel):
    gridSize:         int   = 10
    convinceRange:    float = 0.25
    convergenceMult:  float = 0.3
    opinionType:      str   = "continuous"
    stubbornFrac:     float = 0.0

    bias:            float = 0.5
    biasStrength:    float = 0.0

    nBroadcasters:    int   = 0
    broadcastOpinion: float = 1.0

    seed:            Optional[int] = None  # None = random, int = set, hence reproducible 

    interactionMode: str = "single"



@app.post("/reset")
def reset(params: ResetParams):
    global model
    scenario = OpinionScenario(
        grid_length       = params.gridSize,
        convince_range    = params.convinceRange,
        converge_mult  = params.convergenceMult,
        opinion_type      = params.opinionType,
        stubborn_fraction = params.stubbornFrac,
        bias           = params.bias,
        bias_strength  = params.biasStrength,

        n_broadcasters    = params.nBroadcasters,
        broadcast_opinion = params.broadcastOpinion,

        seed = params.seed if params.seed is not None else int(np.random.randint(0, 99999)),

        interaction_mode = params.interactionMode,
    )
    model = OpinionDynamicsModel(scenario=scenario)
    return serialize_grid(model)

@app.post("/step")
def step():
    global variance_history
    model.step()
    return serialize_grid(model)

@app.get("/state")
def state():
    return serialize_grid(model)