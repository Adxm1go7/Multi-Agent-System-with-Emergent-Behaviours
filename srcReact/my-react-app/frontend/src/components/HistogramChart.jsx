
import { useEffect, useRef } from "react";

export default function HistogramChart({ opinions = [] }) {
  const canvasRef = useRef(null);
  const W    = 600, H = 300;
  const PAD  = { top: 20, right: 20, bottom: 35, left: 50 };
  const BINS = 20;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, W, H);

    const iW = W - PAD.left - PAD.right;
    const iH = H - PAD.top  - PAD.bottom;

    // Background
    ctx.fillStyle = "#f9f9f9";
    ctx.fillRect(0, 0, W, H);

    const counts = new Array(BINS).fill(0);
    for (const v of opinions) {
      const b = Math.min(Math.floor(v * BINS), BINS - 1);
      counts[b]++;
    }
    const maxCount = Math.max(...counts, 1);
    const barW     = iW / BINS;

    // Grid lines + Y labels
    ctx.strokeStyle = "#e0e0e0";
    ctx.fillStyle   = "#888";
    ctx.font        = "10px monospace";
    ctx.textAlign   = "right";
    ctx.lineWidth   = 1;
    for (let i = 0; i <= 4; i++) {
      const y   = PAD.top + (iH / 4) * i;
      const val = Math.round(maxCount * (4 - i) / 4);
      ctx.beginPath();
      ctx.moveTo(PAD.left, y);
      ctx.lineTo(PAD.left + iW, y);
      ctx.stroke();
      ctx.fillText(val, PAD.left - 6, y + 3);
    }

    // X axis labels
    ctx.fillStyle = "#555";
    ctx.font      = "10px monospace";
    ctx.textAlign = "center";
    ctx.fillText("0.0", PAD.left, H - 18);
    ctx.fillText("0.5", PAD.left + iW / 2, H - 18);
    ctx.fillText("1.0", PAD.left + iW, H - 18);
    ctx.fillText("Opinion", PAD.left + iW / 2, H - 4);

    // Y axis label
    ctx.save();
    ctx.translate(12, PAD.top + iH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText("Agents", 0, 0);
    ctx.restore();

    // Bars: red to blue gradient matching grid colours
    counts.forEach((count, i) => {
      const centre = (i + 0.5) / BINS;
      const r = Math.round(214 * (1 - centre) + 31  * centre);
      const g = Math.round(39  * (1 - centre) + 119 * centre);
      const b = Math.round(40  * (1 - centre) + 180 * centre);

      const x    = PAD.left + i * barW;
      const barH = (count / maxCount) * iH;
      const y    = PAD.top + iH - barH;

      ctx.fillStyle = `rgb(${r},${g},${b})`;
      ctx.fillRect(x + 1, y, barW - 2, barH);
    });

  }, [opinions]);

  return (
    <div>
      <p style={{ margin: "0 0 4px 0", fontSize: "15px", fontWeight: 600, color: "#333" }}>
        Opinion Distribution
      </p>
      <canvas ref={canvasRef} width={W} height={H}
        style={{ border: "1px solid #ddd", borderRadius: "4px", display: "block" }} />
    </div>
  );
}