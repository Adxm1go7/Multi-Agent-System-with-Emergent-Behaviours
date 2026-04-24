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

  const doReset = useCallback(async () => {
    setIsPlaying(false);  // ← stop playing on reset
    const res = await fetch(`${API}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        gridSize, convinceRange, convergenceMult, opinionType, stubbornFrac
      }),
    });
    setSimState(await res.json());
  }, [gridSize, convinceRange, convergenceMult, opinionType, stubbornFrac]);

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
          info={{ "Step": simState.step }}
          playInterval={playInterval}
          onPlayIntervalChange={setPlayInterval}
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
