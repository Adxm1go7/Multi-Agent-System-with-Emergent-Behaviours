# Opinion Dynamics Simulator

An agent-based simulation of opinion dynamics using the **bounded confidence model**, where agents on a grid update their opinions based on interactions with nearby agents who hold sufficiently similar views. Includes a live, colour-coded visualisation of the simulation and a parameter-sweep mode for running controlled experiments and analysing convergence behaviour.

Built as my Final Year Project at Queen Mary University of London.


## How it works

- Agents are placed on a 50x50 grid, each holding an opinion value.
- On each simulation step, agents interact with neighbours; if the opinion difference is within a *confidence threshold*, both opinions shift closer together.
- 13 configurable parameters control the simulation, including grid size, confidence threshold, and the proportion of "stubborn" agents who resist opinion change.
- A parameter-sweep mode runs batches of experiments (360 configurations) and outputs results to CSV for convergence analysis.

## Tech stack

- **Simulation engine:** Python, [Mesa](https://mesa.readthedocs.io/)
- **Backend:** FastAPI, serving simulation state via a REST API
- **Frontend:** React, polling the backend at a configurable interval to render a live grid visualisation

## Getting started

# Frontend
cd frontend
npm install
```

### Run the simulator
Open two terminals:

```bash
# Terminal 1 — frontend
cd frontend
npm run dev
```

```bash
# Terminal 2 — backend
cd backend
uvicorn server:app --reload
```

Then open `http://localhost:5173` (or whichever port Vite reports) in your browser.

### Run experiments
Set parameter values in `backend/experiments.py`, then:

```bash
cd backend
python experiments.py    # runs the parameter sweep, outputs results to CSV
python analyse.py        # generates convergence graphs from the results
```

## Project structure
```
├── backend/
│   ├── server.py         # FastAPI app
│   ├── experiments.py    # parameter sweep runner
│   └── analyse.py        # results analysis & graphing
└── frontend/
    └── ...                # React app
```

## Author
Adam Ornoch — [LinkedIn](https://linkedin.com/in/adamornoch)
