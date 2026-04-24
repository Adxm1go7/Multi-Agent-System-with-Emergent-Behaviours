from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Model import OpinionDynamicsModel, OpinionScenario

from pydantic import BaseModel

app = FastAPI()

# Allow React dev server to talk to this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single global model instance
model = OpinionDynamicsModel()

def serialize_grid(model):
    """Pull agent positions and opinions out of the Mesa model."""
    return {
        "step": model.steps,
        "grid_length": model.grid_length,
        "agents": [
            {
                "row": a.cell.coordinate[0],
                "col": a.cell.coordinate[1],
                "opinion": a.opinion,
                "is_stubborn": a.is_stubborn,
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


@app.post("/reset")
def reset(params: ResetParams):
    global model
    scenario = OpinionScenario(
        grid_length       = params.gridSize,
        convince_range    = params.convinceRange,
        converge_mult  = params.convergenceMult,
        opinion_type      = params.opinionType,
        stubborn_fraction = params.stubbornFrac,
    )
    model = OpinionDynamicsModel(scenario=scenario)
    return serialize_grid(model)

@app.post("/step")
def step():
    model.step()
    return serialize_grid(model)

@app.get("/state")
def state():
    return serialize_grid(model)