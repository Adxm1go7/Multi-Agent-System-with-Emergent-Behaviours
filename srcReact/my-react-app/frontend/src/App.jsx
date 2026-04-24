import { useState, useEffect, useRef, useCallback } from "react";
import './App.css'

import Navbar from "./components/Navbar"
import Sidebar from "./components/Sidebar"
import SimGrid from "./components/SimGrid"

const API = "http://localhost:8000";

function App() {
  // Grid state — comes back from the backend on every step/reset
  const [simState, setSimState] = useState({ agents: [], grid_length: 10, step: 0 })

  const [gridSize, setGridSize]               = useState(10);
  const [convinceRange, setConvinceRange]     = useState(1.0);
  const [convergenceMult, setConvergenceMult] = useState(0.5);
  const [opinionType, setOpinionType]         = useState("continuous");
  const [stubbornFrac, setStubbornFrac]       = useState(0.0);
  const [playInterval, setPlayInterval]       = useState(200);
  const [isPlaying, setIsPlaying]             = useState(false);
  const [bias, setBias]               = useState(0.5);
  const [biasStrength, setBiasStrength] = useState(0.0);

  const [seed, setSeed] = useState(""); // empty string = random

  const [maxSteps, setMaxSteps]             = useState("");      // blank = no limit
  const [varianceThreshold, setVarianceThreshold] = useState(""); // blank = no limit

  // Check stopping conditions after every step
  useEffect(() => {
    if (!simState || !isPlaying) return;

    const currentVariance = simState.variance_history?.at(-1);
    const currentStep     = simState.step;

    // Stop if variance is below threshold
    if (varianceThreshold !== "" && currentVariance !== undefined) {
      if (currentVariance <= parseFloat(varianceThreshold)) {
        setIsPlaying(false);
        console.log(`Stopped: variance ${currentVariance} below threshold ${varianceThreshold}`);
        return;
      }
    }

    // Stop if max steps reached
    if (maxSteps !== "" && currentStep >= parseInt(maxSteps)) {
      setIsPlaying(false);
      console.log(`Stopped: reached max steps ${maxSteps}`);
      return;
    }

  }, [simState, isPlaying, varianceThreshold, maxSteps]);

  const stoppedReason = () => {
    if (!simState) return null;
    const v = simState.variance_history?.at(-1);
    if (varianceThreshold !== "" && v <= parseFloat(varianceThreshold)) return "Converged";
    if (maxSteps !== "" && simState.step >= parseInt(maxSteps)) return "Max steps reached";
    return null;
  };

  const info = {
    "Step":        simState?.step ?? 0,
    "Variance":    simState?.variance_history?.at(-1)?.toFixed(4) ?? "—",
    "Active Seed": simState?.seed ?? "—",
    "Status":      stoppedReason() ?? (isPlaying ? "Running" : "Paused"),
  };

  const doReset = useCallback(async () => {
    setIsPlaying(false);  // ← stop playing on reset
    const res = await fetch(`${API}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gridSize, 
        convinceRange,
         convergenceMult, 
         opinionType, 
         stubbornFrac, 
         bias, 
         biasStrength, 
         seed: seed === "" ? null : parseInt(seed),
      }),
    });
    setSimState(await res.json());
  }, [gridSize, convinceRange, convergenceMult, opinionType, stubbornFrac, bias, biasStrength, seed]);

  // ── Step: advance the model one tick, update grid ────────────────────────
  const doStep = useCallback(async () => {
    const res = await fetch(`${API}/step`, { method: "POST" });
    setSimState(await res.json());
  }, []);

  // Toggle play/pause
  const doPlay = useCallback(() => {
    setIsPlaying(p => !p);
  }, []);

  const intervalRef = useRef(null);

  // Whenever isPlaying or playInterval changes, start/stop the interval
  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(doStep, playInterval);
    } else {
      clearInterval(intervalRef.current);
    }
    // Cleanup on unmount or before next effect runs
    return () => clearInterval(intervalRef.current);
  }, [isPlaying, doStep, playInterval]);

  // Init on mount
  useEffect(() => { doReset(); }, []);

  const params = [
    {
      key: "gridSize", label: "Grid Size",
      type: "select",
      value: gridSize, onChange: setGridSize,
      options: [10, 20, 30, 40, 50, 60],
    },
    {
      key: "convinceRange", label: "Max Difference to Converge",
      type: "slider",
      value: convinceRange, onChange: setConvinceRange,
      min: 0.05, max: 1.0, step: 0.05,
    },
    {
      key: "convergenceMult", label: "Convergence Multiplier",
      type: "slider",
      value: convergenceMult, onChange: setConvergenceMult,
      min: 0.05, max: 1.0, step: 0.05,
    },
    {
      key: "opinionType", label: "Opinion Type",
      type: "select",
      value: opinionType, onChange: setOpinionType,
      options: ["continuous", "binary", "ternary", "quadrary"],
    },
    {
      key: "stubbornFrac", label: "Stubborn Agent Fraction",
      type: "slider",
      value: stubbornFrac, onChange: setStubbornFrac,
      min: 0.0, max: 0.5, step: 0.05,
    },
    {
      key: "bias", label: "Opinion Bias (0=red, 1=blue)",
      type: "slider",
      value: bias, onChange: setBias,
      min: 0.0, max: 1.0, step: 0.05,
    },
    {
      key: "biasStrength", label: "Bias Strength (0=uniform)",
      type: "slider",
      value: biasStrength, onChange: setBiasStrength,
      min: 0.0, max: 1.0, step: 0.05,
    },
    {
      key: "maxSteps", label: "Max Steps (blank = unlimited)",
      type: "numberinput",
      value: maxSteps, onChange: setMaxSteps,
      placeholder: "e.g. 500",
    },
    {
      key: "varianceThreshold", label: "Stop at Variance ≤ (blank = never)",
      type: "numberinput",
      value: varianceThreshold, onChange: setVarianceThreshold,
      placeholder: "e.g. 0.001",
    },
  ];

  return (
    <div className="app-container">
      <Navbar title="Cellular Automata Simulator"/>
      <div className="app-body">
        <Sidebar
          params={params}
          onReset={doReset}
          onStep={doStep}
          onPlay={doPlay}
          isPlaying={isPlaying}
          info={{ "Step": simState.step, "Active Seed": simState.seed ?? "—", }}
          playInterval={playInterval}
          onPlayIntervalChange={setPlayInterval}
          seed={seed}
          onSeedChange={setSeed}
        />
      <main className="app-main">
        <SimGrid
          agents={simState.agents}
          gridLength={simState.grid_length}
          size={500}   // fixed canvas pixel size — no DPI issues
        />
        <p>Step: {simState.step}</p>
      </main>

      </div>
    </div>
  )
}

export default App
