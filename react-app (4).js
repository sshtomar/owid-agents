import React, { useState, useEffect, useRef } from 'react';

const customStyles = {
  topoBg: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    zIndex: 0,
    opacity: 0.4,
    pointerEvents: 'none',
    background: `
      radial-gradient(circle at 20% 30%, transparent 0, transparent 40px, #E2E0D5 41px, transparent 42px),
      radial-gradient(circle at 20% 30%, transparent 0, transparent 80px, #E2E0D5 81px, transparent 82px),
      radial-gradient(circle at 70% 60%, transparent 0, transparent 100px, #E2E0D5 101px, transparent 102px),
      radial-gradient(circle at 70% 60%, transparent 0, transparent 150px, #E2E0D5 151px, transparent 152px),
      radial-gradient(circle at 80% 20%, transparent 0, transparent 60px, #E2E0D5 61px, transparent 62px)
    `,
    backgroundSize: '800px 800px',
    backgroundRepeat: 'repeat',
  },
  agentBlockBefore: {
    content: "''",
    position: 'absolute',
    left: '-20px',
    top: '6px',
    width: '4px',
    height: '4px',
    backgroundColor: '#D94833',
    borderRadius: '50%',
  },
};

const AgentBlock = ({ id, query, response, detail }) => (
  <div className="agent-block" id={id} style={{ position: 'relative' }}>
    <div style={{ position: 'absolute', left: '-20px', top: '6px', width: '4px', height: '4px', backgroundColor: '#D94833', borderRadius: '50%' }}></div>
    <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '10px', color: '#7A786F', marginBottom: '8px', display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
      <span style={{ color: '#EA5E33' }}>{'>'}</span>
      <span>{query}</span>
    </div>
    <div style={{ fontWeight: 500, color: '#2B2A27', marginBottom: '6px', textAlign: 'justify', hyphens: 'auto' }}>{response}</div>
    <div style={{ color: '#7A786F', marginBottom: '12px', textAlign: 'justify', hyphens: 'auto' }}>{detail}</div>
  </div>
);

const ThumbnailItem = ({ index, src, active, onClick }) => (
  <div
    onClick={onClick}
    style={{ display: 'flex', flexDirection: 'column', gap: '4px', flex: 1, cursor: 'pointer', opacity: active ? 1 : 0.7, transition: 'opacity 0.2s ease' }}
    onMouseEnter={e => e.currentTarget.style.opacity = '1'}
    onMouseLeave={e => { if (!active) e.currentTarget.style.opacity = '0.7'; }}
  >
    <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '9px', color: '#7A786F' }}>{String(index).padStart(2, '0')}</span>
    <img
      src={src}
      alt="Terrain"
      style={{
        width: '100%',
        height: '48px',
        objectFit: 'cover',
        filter: active ? 'grayscale(0%) contrast(1)' : 'grayscale(80%) contrast(1.2)',
        transition: 'filter 0.3s ease',
      }}
    />
  </div>
);

const DataCanvas = ({ containerRef, canvasRef, leaderSvgRef, agentRefs }) => {
  useEffect(() => {
    const colors = {
      bg: '#F6F5EE',
      high: '#EA5E33',
      med: '#F29A44',
      low: '#F5D38A',
      cool: '#A6C4A2',
      empty: 'rgba(200, 200, 190, 0.2)',
    };

    const gridSize = 12;
    const padding = 20;

    const hotspots = [
      { x: 0.3, y: 0.4, radius: 0.4, intensity: 1.0 },
      { x: 0.4, y: 0.7, radius: 0.3, intensity: 0.8 },
      { x: 0.6, y: 0.3, radius: 0.25, intensity: 0.6 },
      { x: 0.7, y: 0.6, radius: 0.35, intensity: 0.7 },
    ];

    const targetNodes = [
      { rx: 0.25, ry: 0.35, id: 1 },
      { rx: 0.5, ry: 0.55, id: 2 },
      { rx: 0.65, ry: 0.75, id: 3 },
    ];

    function drawMatrix(canvas, ctx, width, height) {
      ctx.fillStyle = colors.bg;
      ctx.fillRect(0, 0, width, height);

      ctx.globalCompositeOperation = 'multiply';

      const cols = Math.floor((width - padding * 2) / gridSize);
      const rows = Math.floor((height - padding * 2) / gridSize);

      const startX = (width - cols * gridSize) / 2;
      const startY = (height - rows * gridSize) / 2;

      for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
          const cx = startX + i * gridSize + gridSize / 2;
          const cy = startY + j * gridSize + gridSize / 2;

          const nx = i / cols;
          const ny = j / rows;

          let maxInfluence = 0;
          const noise = Math.sin(nx * 20) * Math.cos(ny * 20) * 0.15;

          hotspots.forEach(spot => {
            const dx = nx - spot.x;
            const dy = ny - spot.y;
            const dist = Math.sqrt(dx * dx + dy * dy * (height / width));
            if (dist < spot.radius) {
              let influence = Math.pow(1 - dist / spot.radius, 1.5) * spot.intensity;
              maxInfluence = Math.max(maxInfluence, influence);
            }
          });

          maxInfluence += noise;
          maxInfluence = Math.max(0, Math.min(1, maxInfluence));

          if (Math.random() > maxInfluence + 0.1 && maxInfluence < 0.2) continue;

          let radius = (gridSize / 2) * 0.8;
          let fill = colors.empty;

          if (maxInfluence > 0.7) {
            fill = colors.high;
            radius *= 0.9;
          } else if (maxInfluence > 0.4) {
            fill = colors.med;
            radius *= 0.7;
          } else if (maxInfluence > 0.2) {
            fill = colors.low;
            radius *= 0.5;
          } else if (maxInfluence > 0.05) {
            fill = colors.cool;
            radius *= 0.3;
          } else {
            radius *= 0.15;
          }

          const ox = (Math.random() - 0.5) * 1.5;
          const oy = (Math.random() - 0.5) * 1.5;

          ctx.beginPath();
          ctx.arc(cx + ox, cy + oy, radius, 0, Math.PI * 2);
          ctx.fillStyle = fill;
          ctx.fill();

          if (maxInfluence > 0.85 && Math.random() > 0.5) {
            ctx.beginPath();
            ctx.arc(cx + ox, cy + oy, radius * 0.3, 0, Math.PI * 2);
            ctx.fillStyle = colors.bg;
            ctx.fill();
          }

          if (maxInfluence > 0.5 && maxInfluence < 0.6 && Math.random() > 0.8) {
            ctx.beginPath();
            ctx.arc(cx + ox, cy + oy, radius * 1.5, 0, Math.PI * 2);
            ctx.strokeStyle = colors.high;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      ctx.globalCompositeOperation = 'source-over';
    }

    function updateLeaderLines(canvas, width, height) {
      const svg = leaderSvgRef.current;
      if (!svg) return;

      svg.setAttribute('width', window.innerWidth);
      svg.setAttribute('height', window.innerHeight);
      svg.style.width = window.innerWidth + 'px';
      svg.style.height = window.innerHeight + 'px';

      const canvasRect = canvas.getBoundingClientRect();

      targetNodes.forEach((node, index) => {
        const i = index + 1;
        const anchorEl = agentRefs[index]?.current;
        if (!anchorEl) return;

        const anchorRect = anchorEl.getBoundingClientRect();
        const startX = anchorRect.right + 10;
        const startY = anchorRect.top + 10;

        const endX = canvasRect.left + canvasRect.width * node.rx;
        const endY = canvasRect.top + canvasRect.height * node.ry;

        const pathEl = svg.querySelector(`#path-${i}`);
        const nodeEl = svg.querySelector(`#node-${i}`);

        if (pathEl && nodeEl) {
          const midX = startX + (endX - startX) * 0.3;
          const d = `M ${startX} ${startY} L ${midX} ${startY} L ${endX} ${endY}`;
          pathEl.setAttribute('d', d);
          nodeEl.setAttribute('cx', endX);
          nodeEl.setAttribute('cy', endY);
        }
      });
    }

    function resizeAndDraw() {
      const canvas = canvasRef.current;
      const container = containerRef.current;
      if (!canvas || !container) return;

      const ctx = canvas.getContext('2d', { alpha: false });
      const dpr = window.devicePixelRatio || 1;
      const rect = container.getBoundingClientRect();

      const width = rect.width;
      const height = rect.height;

      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;

      ctx.scale(dpr, dpr);

      drawMatrix(canvas, ctx, width, height);
      updateLeaderLines(canvas, width, height);
    }

    const timer = setTimeout(resizeAndDraw, 100);
    window.addEventListener('resize', resizeAndDraw);

    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', resizeAndDraw);
    };
  }, [canvasRef, containerRef, leaderSvgRef, agentRefs]);

  return null;
};

const App = () => {
  const [activeThumb, setActiveThumb] = useState(0);

  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const leaderSvgRef = useRef(null);
  const agentRef1 = useRef(null);
  const agentRef2 = useRef(null);
  const agentRef3 = useRef(null);
  const agentRefs = [agentRef1, agentRef2, agentRef3];

  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        background-color: #F6F5EE;
        color: #2B2A27;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 11px;
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
        overflow-x: hidden;
      }
    `;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);

  const thumbnails = [
    'https://images.pexels.com/photos/2832039/pexels-photo-2832039.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/2432299/pexels-photo-2432299.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/3408744/pexels-photo-3408744.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/2101187/pexels-photo-2101187.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/417102/pexels-photo-417102.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/221502/pexels-photo-221502.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/2832042/pexels-photo-2832042.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/3315053/pexels-photo-3315053.jpeg?auto=compress&cs=tinysrgb&w=300',
    'https://images.pexels.com/photos/2387873/pexels-photo-2387873.jpeg?auto=compress&cs=tinysrgb&w=300',
  ];

  const gridStyle = {
    position: 'relative',
    zIndex: 1,
    display: 'grid',
    gridTemplateColumns: '280px 1fr 320px',
    gridTemplateRows: '1fr auto',
    flexGrow: 1,
    padding: '40px 40px 20px 40px',
    gap: '40px',
    maxWidth: '1800px',
    margin: '0 auto',
    width: '100%',
  };

  const sidebarLeftStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '40px',
    paddingTop: '60px',
  };

  const vizStageStyle = {
    position: 'relative',
    width: '100%',
    height: '100%',
    minHeight: '600px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  const crosshairBase = {
    position: 'absolute',
    width: '10px',
    height: '10px',
    pointerEvents: 'none',
  };

  const crosshairLineH = {
    position: 'absolute',
    top: '50%',
    left: 0,
    width: '100%',
    height: '1px',
    backgroundColor: '#C2C0B5',
    transform: 'translateY(-50%)',
  };

  const crosshairLineV = {
    position: 'absolute',
    left: '50%',
    top: 0,
    height: '100%',
    width: '1px',
    backgroundColor: '#C2C0B5',
    transform: 'translateX(-50%)',
  };

  const Crosshair = ({ style }) => (
    <div style={{ ...crosshairBase, ...style }}>
      <div style={crosshairLineH}></div>
      <div style={crosshairLineV}></div>
    </div>
  );

  const sidebarRightStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '32px',
  };

  const thumbnailStripStyle = {
    gridColumn: '1 / -1',
    display: 'flex',
    gap: '8px',
    marginTop: '20px',
    paddingTop: '20px',
    borderTop: '1px solid #C2C0B5',
  };

  const systemTitleStyle = {
    gridColumn: '1 / -1',
    marginTop: '40px',
    paddingBottom: '20px',
    borderTop: '1px solid #C2C0B5',
    paddingTop: '16px',
  };

  return (
    <div style={{ backgroundColor: '#F6F5EE', color: '#2B2A27', fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif", fontSize: '11px', lineHeight: 1.5, minHeight: '100vh', display: 'flex', flexDirection: 'column', overflowX: 'hidden' }}>
      <div style={customStyles.topoBg}></div>

      <DataCanvas
        canvasRef={canvasRef}
        containerRef={containerRef}
        leaderSvgRef={leaderSvgRef}
        agentRefs={agentRefs}
      />

      <main style={gridStyle}>
        <svg
          ref={leaderSvgRef}
          style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}
        >
          <path id="path-1" fill="none" stroke="#2B2A27" strokeWidth="0.75" strokeDasharray="2 3" opacity="0.6" d=""></path>
          <circle id="node-1" fill="transparent" stroke="#2B2A27" strokeWidth="1" cx="0" cy="0" r="3"></circle>
          <path id="path-2" fill="none" stroke="#2B2A27" strokeWidth="0.75" strokeDasharray="2 3" opacity="0.6" d=""></path>
          <circle id="node-2" fill="transparent" stroke="#2B2A27" strokeWidth="1" cx="0" cy="0" r="3"></circle>
          <path id="path-3" fill="none" stroke="#2B2A27" strokeWidth="0.75" strokeDasharray="2 3" opacity="0.6" d=""></path>
          <circle id="node-3" fill="transparent" stroke="#2B2A27" strokeWidth="1" cx="0" cy="0" r="3"></circle>
        </svg>

        {/* Left Sidebar */}
        <aside style={sidebarLeftStyle}>
          <div style={{ borderBottom: '1px solid #C2C0B5', paddingBottom: '16px', marginBottom: '0px' }}>
            <span style={{ fontSize: '9px', textTransform: 'uppercase', letterSpacing: '0.5px', color: '#7A786F', marginBottom: '4px', display: 'block' }}>System Status</span>
            <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '10px', display: 'flex', justifyContent: 'space-between' }}>
              <span>AGENT: ACTIVE</span>
              <span>v.3.14.0</span>
            </div>
          </div>

          <div ref={agentRef1}>
            <AgentBlock
              id="agent-anchor-1"
              query="Analyze structural vulnerability anomalies in NW sector considering baseline temperature shift."
              response="Significant deviation detected. Urban density decoupling from rapid cooling models."
              detail="Sector NW (grid ref: 4A-7B) exhibits a +2.1°C retention index overnight. Historical housing stock lacking thermal mass upgrades correlates directly with the visual clustering."
            />
          </div>

          <div ref={agentRef2}>
            <AgentBlock
              id="agent-anchor-2"
              query="Isolate primary risk vector for central corridor."
              response="The 'Almudena' sink effect is operating counter-intuitively."
              detail="Expected to act as a thermal buffer, the central impermeable zone is trapping adjacent heat exhaust. Surrounding neighborhoods show rapid compound vulnerability index spiking > 8.5."
            />
          </div>

          <div ref={agentRef3}>
            <AgentBlock
              id="agent-anchor-3"
              query="Compute infrastructure degradation zones."
              response="Rail corridor severance creating micro-climate pockets."
              detail="ADIF infrastructure forms a hard boundary preventing convective cooling flow towards the Eastern perimeter. Proposed intervention: structural permeation at grid points 22, 28, and 31."
            />
          </div>
        </aside>

        {/* Visualization Stage */}
        <div ref={containerRef} style={vizStageStyle} id="viz-container">
          <Crosshair style={{ top: 0, left: 0 }} />
          <Crosshair style={{ top: 0, right: 0 }} />
          <Crosshair style={{ bottom: 0, left: 0 }} />
          <Crosshair style={{ bottom: 0, right: 0 }} />
          <canvas ref={canvasRef} id="data-canvas" style={{ width: '100%', height: '100%' }}></canvas>
        </div>

        {/* Right Sidebar */}
        <aside style={sidebarRightStyle}>
          <div style={{ marginBottom: '40px' }}>
            <span style={{ fontSize: '9px', textTransform: 'uppercase', letterSpacing: '0.5px', color: '#7A786F', marginBottom: '4px', display: 'block' }}>Dataset Ref: CL-2024-X</span>
            <h1 style={{ fontSize: '14px', fontWeight: 600, letterSpacing: '-0.2px', lineHeight: 1.2, color: '#2B2A27', marginBottom: '8px' }}>Environmental Vulnerability &amp; Urban Heat Island (UHI) Exposure</h1>
            <p style={{ color: '#7A786F', marginTop: '8px' }}>Spatial analysis of structural decay correlated with localized climate shifts, Madrid metropolitan sample.</p>
          </div>

          <div style={{ borderBottom: '1px solid #C2C0B5', paddingBottom: '16px', marginBottom: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '9px', textTransform: 'uppercase', letterSpacing: '0.5px', color: '#7A786F', marginBottom: '4px', display: 'block' }}>Temperature Variance (ΔT)</span>

            {[
              { color: '#EA5E33', label: '> 5°C Anomaly' },
              { color: '#F29A44', label: '3°C - 5°C Anomaly' },
              { color: '#F5D38A', label: '1°C - 3°C Anomaly' },
              { color: '#A6C4A2', label: '< 1°C Baseline' },
            ].map((item, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '24px', height: '12px', borderRadius: '1px', backgroundColor: item.color }}></div>
                <span>{item.label}</span>
              </div>
            ))}

            <div style={{ marginTop: '16px', color: '#7A786F', textAlign: 'justify', hyphens: 'auto' }}>
              In the eastern intervention sector, UHI effects compound baseline climatic shifts, pushing localized temperatures up to 5°C above regional averages during peak stress events. This creates critical risk zones for vulnerable populations residing in low-efficiency structures.
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '9px', textTransform: 'uppercase', letterSpacing: '0.5px', color: '#7A786F', marginBottom: '4px', display: 'block' }}>Structural Quality &amp; Age Index</span>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <span style={{ width: '60px', fontSize: '10px' }}>High Age</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', height: '16px' }}>
                  <div style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#F5D38A', opacity: 0.8 }}></div>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#F29A44', opacity: 0.8 }}></div>
                  <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#EA5E33', opacity: 0.8 }}></div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginTop: '12px' }}>
                <span style={{ width: '60px', fontSize: '10px' }}>Low Quality</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', height: '16px' }}>
                  <div style={{ width: '4px', height: '4px', borderRadius: '50%', backgroundColor: '#D94833', opacity: 0.3 }}></div>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#D94833', opacity: 0.6 }}></div>
                  <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#D94833', opacity: 0.9 }}></div>
                </div>
              </div>
            </div>

            <div style={{ marginTop: '24px', color: '#7A786F', textAlign: 'justify', hyphens: 'auto' }}>
              Paradoxically, proximity to open, un-urbanized spaces does not mitigate risk if structural quality is poor. The boundary zones exhibit high intensity risk due to a lack of mitigating public space capable of offsetting the thermal mass of surrounding decaying infrastructure.
            </div>
          </div>
        </aside>

        {/* System Title */}
        <div style={systemTitleStyle}>
          <h2 style={{ fontSize: '14px', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '4px', fontWeight: 500 }}>DataWorld / Agent Analysis Platform</h2>
          <p style={{ color: '#7A786F', maxWidth: '600px' }}>Generative natural language modeling applied to high-density geospatial datasets. Scale 1:50,000.</p>
        </div>

        {/* Thumbnail Strip */}
        <footer style={{ ...thumbnailStripStyle, gridColumn: '1 / -1' }}>
          {thumbnails.map((src, i) => (
            <ThumbnailItem
              key={i}
              index={i + 1}
              src={src}
              active={activeThumb === i}
              onClick={() => setActiveThumb(i)}
            />
          ))}
        </footer>
      </main>
    </div>
  );
};

export default App;