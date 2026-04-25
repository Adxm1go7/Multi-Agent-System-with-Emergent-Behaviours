import { useEffect, useRef } from "react";

// Opinion [0,1] -> red to blue
function opinionToColor(v) {
  const r = Math.round(255 * (1 - v));
  const g = Math.round(0);
  const b = Math.round(255  * v);
  return `rgb(${r},${g},${b})`;
}

export default function SimGrid({ agents = [], gridLength = 10, size = 500 }) {
  const canvasRef = useRef(null);
  const cellSize  = size / gridLength;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    // Clear
    ctx.fillStyle = "#e0e0e0";  // empty cell colour
    ctx.fillRect(0, 0, size, size);

    // Build lookup so we don't loop agents inside a nested loop
    const lookup = {};
    for (const a of agents) {
      lookup[`${a.row},${a.col}`] = a;
    }

    // Draw every cell
    const gap = cellSize > 4 ? 1 : 0;  // gap between cells only if big enough
    for (let row = 0; row < gridLength; row++) {
      for (let col = 0; col < gridLength; col++) {
        const agent = lookup[`${row},${col}`];

        ctx.fillStyle = agent ? opinionToColor(agent.opinion) : "#e0e0e0";
        ctx.fillRect(
          col * cellSize + gap,
          row * cellSize + gap,
          cellSize - gap * 2,
          cellSize - gap * 2,
        );

        // Draw broadcaster agents with a Diamond in centre
        if (agent?.is_broadcaster) {
          const cx = col * cellSize + cellSize / 2;
          const cy = row * cellSize + cellSize / 2;
          const half = (cellSize / 2) - gap;

          ctx.fillStyle = opinionToColor(agent.opinion);
          ctx.beginPath();
          ctx.moveTo(cx,        cy - half);  // top
          ctx.lineTo(cx + half, cy);         // right
          ctx.lineTo(cx,        cy + half);  // bottom
          ctx.lineTo(cx - half, cy);         // left
          ctx.closePath();
          ctx.fill();

          // White outline so it stands out
          ctx.strokeStyle = "white";
          ctx.lineWidth   = 1;
          ctx.stroke();
        } else if (agent?.is_stubborn) {
          const cx = col * cellSize + cellSize / 2;
          const cy = row * cellSize + cellSize / 2;
          const radius = Math.max(1, cellSize * 0.10);
          ctx.fillStyle = "white";
          ctx.beginPath();
          ctx.arc(cx, cy, radius, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }
  }, [agents, gridLength, size, cellSize]);


  return <canvas ref={canvasRef} width={size} height={size} />;
}