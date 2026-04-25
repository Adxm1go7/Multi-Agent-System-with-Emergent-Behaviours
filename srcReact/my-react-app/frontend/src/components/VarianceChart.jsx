import { useEffect, useRef } from "react";

export default function VarianceChart({ history = [] }) {
  const canvasRef = useRef(null);
  const W = 600, H = 300;
  const PAD = { top: 20, right: 20, bottom: 35, left: 50 };

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

    // Grid lines + Y axis labels
    ctx.strokeStyle = "#e0e0e0";
    ctx.fillStyle   = "#888";
    ctx.font        = "10px monospace";
    ctx.textAlign   = "right";
    ctx.lineWidth   = 1;
    const maxY = 0.25;
    for (let i = 0; i <= 4; i++) {
      const y   = PAD.top + (iH / 4) * i;
      const val = (maxY * (4 - i) / 4).toFixed(3);
      ctx.beginPath();
      ctx.moveTo(PAD.left, y);
      ctx.lineTo(PAD.left + iW, y);
      ctx.stroke();
      ctx.fillText(val, PAD.left - 6, y + 3);
    }

    // Axis labels
    ctx.fillStyle = "#555";
    ctx.font      = "11px monospace";
    ctx.textAlign = "center";
    ctx.fillText("Steps", PAD.left + iW / 2, H - 4);

    // Save + rotate for Y label
    ctx.save();
    ctx.translate(12, PAD.top + iH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText("Variance", 0, 0);
    ctx.restore();

    if (history.length < 2) return;

    const xScale = iW / Math.max(history.length - 1, 1);
    const yScale = iH / maxY;

    // Fill area under line
    ctx.beginPath();
    ctx.moveTo(PAD.left, PAD.top + iH);
    history.forEach((v, i) => {
      ctx.lineTo(PAD.left + i * xScale, PAD.top + iH - Math.min(v, maxY) * yScale);
    });
    ctx.lineTo(PAD.left + (history.length - 1) * xScale, PAD.top + iH);
    ctx.closePath();
    ctx.fillStyle = "rgba(21, 101, 192, 0.1)";
    ctx.fill();

    // Line
    ctx.beginPath();
    history.forEach((v, i) => {
      const x = PAD.left + i * xScale;
      const y = PAD.top + iH - Math.min(v, maxY) * yScale;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.strokeStyle = "#1565c0";
    ctx.lineWidth   = 2;
    ctx.lineJoin    = "round";
    ctx.stroke();

    // Current value label
    const last = history.at(-1);
    ctx.fillStyle = "#1565c0";
    ctx.font      = "bold 11px monospace";
    ctx.textAlign = "left";
    ctx.fillText(`σ² = ${last.toFixed(4)}`, PAD.left + 4, PAD.top + 14);

  }, [history]);

  return (
    <div>
      <p style={{ margin: "0 0 4px 0", fontSize: "15px", fontWeight: 600, color: "#333" }}>
        Opinion Variance
      </p>
      <canvas ref={canvasRef} width={W} height={H}
        style={{ border: "1px solid #ddd", borderRadius: "4px", display: "block" }} />
    </div>
  );
}