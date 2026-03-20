import React, { useEffect } from 'react';

const customStyles = {
  root: {
    '--bg': '#f6f6f4',
    '--text-main': '#1a1a1a',
    '--text-muted': '#666666',
    '--rule': '#d5d5d0',
    '--chart-bg': '#eaf0f4',
    '--chart-grid': '#dce3e8',
    '--color-red': '#c95b4f',
    '--color-blue': '#2b579a',
    '--color-green': '#6ba37b',
    '--color-purple': '#a288b5',
    '--color-slate': '#8a949c',
    '--color-light-purple': '#dcd3e6',
    '--color-light-blue': '#cce0f5',
  },
  body: {
    backgroundColor: '#f6f6f4',
    color: '#1a1a1a',
    fontFamily: "'Lora', Georgia, serif",
    lineHeight: '1.6',
    WebkitFontSmoothing: 'antialiased',
    MozOsxFontSmoothing: 'grayscale',
    padding: '2vw',
  },
  pageContainer: {
    maxWidth: '1600px',
    margin: '0 auto',
    backgroundColor: '#fff',
    boxShadow: '0 0 40px rgba(0,0,0,0.03)',
  },
  spread: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    minHeight: '90vh',
  },
  page: {
    padding: '6vw 5vw',
    position: 'relative',
  },
  pageLeft: {
    borderRight: '1px solid #ebebeb',
  },
  headerMarginalia: {
    position: 'absolute',
    top: '2vw',
    left: '5vw',
    right: '5vw',
    display: 'flex',
    justifyContent: 'space-between',
  },
  sansLabel: {
    fontFamily: "'Inter', Helvetica, sans-serif",
    fontSize: '0.65rem',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '0.08em',
    color: '#1a1a1a',
  },
  sansMeta: {
    fontFamily: "'Inter', Helvetica, sans-serif",
    fontSize: '0.75rem',
    color: '#666666',
    lineHeight: '1.4',
  },
  serifTitle: {
    fontSize: '1.5rem',
    lineHeight: '1.3',
    marginBottom: '1rem',
    letterSpacing: '-0.01em',
    fontWeight: '500',
  },
  serifBody: {
    fontSize: '0.95rem',
    lineHeight: '1.7',
    color: '#1a1a1a',
    maxWidth: '65ch',
  },
  dividerTop: {
    borderTop: '1px solid #d5d5d0',
    paddingTop: '0.5rem',
    marginTop: '4rem',
  },
  diagramContainer: {
    margin: '2.5rem 0',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-start',
    gap: '2rem',
  },
  diagramSvg: {
    width: '100%',
    maxWidth: '350px',
    height: 'auto',
  },
  chartBlock: {
    marginBottom: '4rem',
  },
  chartBox: {
    backgroundColor: '#eaf0f4',
    width: '100%',
    height: '280px',
    position: 'relative',
    marginTop: '1rem',
    marginBottom: '1rem',
    overflow: 'hidden',
  },
  chartSvg: {
    width: '100%',
    height: '100%',
    display: 'block',
  },
  legend: {
    display: 'flex',
    gap: '1.5rem',
    alignItems: 'center',
    marginTop: '1rem',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem',
  },
  legendDot: {
    width: '6px',
    height: '6px',
    borderRadius: '50%',
  },
  figureCaption: {
    display: 'flex',
    gap: '1rem',
    alignItems: 'baseline',
  },
  agentQueryBlock: {
    backgroundColor: '#fcfcfc',
    border: '1px solid #d5d5d0',
    padding: '2rem',
    margin: '2rem 0',
    position: 'relative',
    paddingLeft: 'calc(2rem + 3px)',
  },
  agentQueryBlockBar: {
    position: 'absolute',
    left: '0',
    top: '0',
    bottom: '0',
    width: '3px',
    backgroundColor: '#2b579a',
  },
  queryInput: {
    fontFamily: "'Lora', Georgia, serif",
    fontSize: '1.1rem',
    fontStyle: 'italic',
    color: '#1a1a1a',
    marginBottom: '1.5rem',
    paddingBottom: '1rem',
    borderBottom: '1px dashed #d5d5d0',
  },
  agentResponse: {
    fontSize: '0.9rem',
  },
};

const SansLabel = ({ children, style }) => (
  <span style={{ ...customStyles.sansLabel, ...style }}>{children}</span>
);

const SansMeta = ({ children, style }) => (
  <span style={{ ...customStyles.sansMeta, ...style }}>{children}</span>
);

const DiagramExtraction = () => (
  <svg viewBox="0 0 400 120" style={customStyles.diagramSvg}>
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#d5d5d0" />
      </marker>
    </defs>
    <g transform="translate(60, 60)">
      <circle cx="0" cy="0" r="45" fill="#dcd3e6" />
      <circle cx="-15" cy="-15" r="8" fill="#a288b5" />
      <circle cx="15" cy="-10" r="8" fill="#a288b5" />
      <circle cx="-5" cy="15" r="8" fill="#a288b5" />
      <circle cx="20" cy="15" r="8" fill="#a288b5" />
      <circle cx="-25" cy="5" r="8" fill="#a288b5" />
      <text x="0" y="65" textAnchor="middle" style={{ ...customStyles.sansLabel, fontSize: '8px' }}>Unstructured Inputs</text>
    </g>
    <line x1="120" y1="60" x2="160" y2="60" stroke="#d5d5d0" strokeWidth="1" markerEnd="url(#arrow)" />
    <text x="140" y="50" textAnchor="middle" style={{ ...customStyles.sansLabel, fontSize: '7px', fill: '#666666' }}>Agent Synthesis</text>
    <g transform="translate(260, 60)">
      <line x1="-20" y1="0" x2="20" y2="-20" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="-20" y1="0" x2="20" y2="20" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="20" y1="-20" x2="40" y2="0" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="20" y1="20" x2="40" y2="0" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="-20" y1="0" x2="-40" y2="-15" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="-20" y1="0" x2="-40" y2="15" stroke="#d5d5d0" strokeWidth="1" />
      <circle cx="-20" cy="0" r="6" fill="#8a949c" />
      <circle cx="20" cy="-20" r="6" fill="#c95b4f" />
      <circle cx="20" cy="20" r="6" fill="#c95b4f" />
      <circle cx="40" cy="0" r="6" fill="#c95b4f" />
      <circle cx="-40" cy="-15" r="6" fill="#8a949c" />
      <circle cx="-40" cy="15" r="6" fill="#8a949c" />
      <text x="0" y="65" textAnchor="middle" style={{ ...customStyles.sansLabel, fontSize: '8px' }}>Structured Outputs</text>
    </g>
  </svg>
);

const DiagramValidation = () => (
  <svg viewBox="0 0 400 120" style={customStyles.diagramSvg}>
    <g transform="translate(50, 60)">
      <circle cx="0" cy="0" r="40" fill="#cce0f5" />
      <line x1="-15" y1="0" x2="15" y2="0" stroke="#2b579a" strokeWidth="2" />
      <line x1="0" y1="-15" x2="0" y2="15" stroke="#2b579a" strokeWidth="2" />
      <circle cx="-15" cy="0" r="5" fill="#2b579a" />
      <circle cx="15" cy="0" r="5" fill="#2b579a" />
      <circle cx="0" cy="-15" r="5" fill="#2b579a" />
      <circle cx="0" cy="15" r="5" fill="#2b579a" />
      <text x="0" y="60" textAnchor="middle" style={{ ...customStyles.sansLabel, fontSize: '8px' }}>Query Node</text>
    </g>
    <text x="110" y="63" textAnchor="middle" style={customStyles.sansMeta}>+</text>
    <g transform="translate(160, 60)">
      <circle cx="0" cy="0" r="40" fill="#cce0f5" />
      <path d="M 0 0 L -12 -12 M 0 0 L 12 -12 M 0 0 L 0 15" stroke="#2b579a" strokeWidth="2" fill="none" />
      <circle cx="-12" cy="-12" r="5" fill="#2b579a" />
      <circle cx="12" cy="-12" r="5" fill="#2b579a" />
      <circle cx="0" cy="15" r="5" fill="#2b579a" />
      <text x="0" y="60" textAnchor="middle" style={{ ...customStyles.sansLabel, fontSize: '8px' }}>Dataset Index</text>
    </g>
    <line x1="215" y1="60" x2="250" y2="60" stroke="#d5d5d0" strokeWidth="1" />
    <polygon points="250,57 255,60 250,63" fill="#d5d5d0" />
    <g transform="translate(320, 60)">
      <line x1="-20" y1="0" x2="10" y2="-20" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="-20" y1="0" x2="10" y2="0" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="-20" y1="0" x2="10" y2="20" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="10" y1="-20" x2="30" y2="-10" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="10" y1="20" x2="30" y2="10" stroke="#d5d5d0" strokeWidth="1" />
      <line x1="10" y1="0" x2="30" y2="-10" stroke="#d5d5d0" strokeWidth="1" />
      <circle cx="-20" cy="0" r="6" fill="#2b579a" />
      <circle cx="10" cy="-20" r="6" fill="#c95b4f" />
      <circle cx="10" cy="0" r="6" fill="#c95b4f" />
      <circle cx="10" cy="20" r="6" fill="#c95b4f" />
      <circle cx="30" cy="-10" r="6" fill="#c95b4f" />
      <circle cx="30" cy="10" r="6" fill="#c95b4f" />
      <text x="0" y="60" textAnchor="middle" style={{ ...customStyles.sansLabel, fontSize: '8px' }}>Correlated Insight</text>
    </g>
  </svg>
);

const ChartAtmospheric = () => (
  <div style={customStyles.chartBox}>
    <svg viewBox="0 0 800 280" style={customStyles.chartSvg} preserveAspectRatio="none">
      <line x1="0" y1="40" x2="800" y2="40" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="80" x2="800" y2="80" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="120" x2="800" y2="120" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="160" x2="800" y2="160" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="200" x2="800" y2="200" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="240" x2="800" y2="240" stroke="#dce3e8" strokeWidth="1" />
      <text x="10" y="35" style={{ fontSize: '10px', fill: '#8a949c', fontFamily: "'Inter', Helvetica, sans-serif", transform: 'rotate(-90deg)', transformOrigin: '10px 35px' }}>PM2.5 Density (μg/m³)</text>
      <path d="M 40 20 C 200 20, 300 240, 760 250" fill="none" stroke="#6ba37b" strokeWidth="1.5" />
      <path d="M 40 20 C 250 20, 350 220, 760 230" fill="none" stroke="#6ba37b" strokeWidth="1.5" strokeOpacity="0.6" />
      <path d="M 40 20 C 300 20, 400 200, 760 210" fill="none" stroke="#6ba37b" strokeWidth="1.5" strokeOpacity="0.3" />
      <text x="400" y="270" textAnchor="middle" style={{ fontSize: '10px', fontFamily: "'Inter', Helvetica, sans-serif", fill: '#666666' }}>Time (2005 - 2023)</text>
    </svg>
  </div>
);

const ChartEnergy = () => (
  <div style={customStyles.chartBox}>
    <svg viewBox="0 0 800 280" style={customStyles.chartSvg} preserveAspectRatio="none">
      <line x1="0" y1="40" x2="800" y2="40" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="80" x2="800" y2="80" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="120" x2="800" y2="120" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="160" x2="800" y2="160" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="200" x2="800" y2="200" stroke="#dce3e8" strokeWidth="1" />
      <line x1="0" y1="240" x2="800" y2="240" stroke="#dce3e8" strokeWidth="1" />
      <text x="10" y="35" style={{ fontSize: '10px', fill: '#8a949c', fontFamily: "'Inter', Helvetica, sans-serif", transform: 'rotate(-90deg)', transformOrigin: '10px 35px' }}>Generation Capacity (GW)</text>
      <path d="M 40 30 C 250 30, 400 160, 760 170" fill="none" stroke="#2b579a" strokeWidth="2" />
      <text x="765" y="170" style={{ fontSize: '8px', fill: '#2b579a', fontFamily: "'Inter', Helvetica, sans-serif", fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.08em', dominantBaseline: 'middle' }}>Coal Decline</text>
      <path d="M 40 30 C 200 30, 350 200, 760 210" fill="none" stroke="#c95b4f" strokeWidth="2" />
      <text x="765" y="210" style={{ fontSize: '8px', fill: '#c95b4f', fontFamily: "'Inter', Helvetica, sans-serif", fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.08em', dominantBaseline: 'middle' }}>Nat Gas</text>
      <path d="M 40 30 C 150 30, 250 250, 760 260" fill="none" stroke="#6ba37b" strokeWidth="2" />
      <text x="765" y="260" style={{ fontSize: '8px', fill: '#6ba37b', fontFamily: "'Inter', Helvetica, sans-serif", fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.08em', dominantBaseline: 'middle' }}>Renewables</text>
      <text x="400" y="270" textAnchor="middle" style={{ fontSize: '10px', fontFamily: "'Inter', Helvetica, sans-serif", fill: '#666666' }}>Time (2005 - 2023)</text>
    </svg>
  </div>
);

const LeftPage = () => (
  <article style={{ ...customStyles.page, ...customStyles.pageLeft }}>
    <header style={customStyles.headerMarginalia}>
      <SansLabel>DataWorld Platform</SansLabel>
      <SansLabel>Vol. 4 / Research Agents</SansLabel>
    </header>

    <div style={{ marginTop: '4vw' }}>
      <h1 style={customStyles.serifTitle}>The Analytical Paradigm</h1>
      <div style={customStyles.serifBody}>
        <p style={{ marginBottom: '1.5rem' }}>We deploy autonomous research agents to interpret raw, unstructured data from global institutions, transforming disparate metrics into synthesized models. Traditional analysis queries static databases; our agents parse dynamic inputs across energy, environment, and health sectors, identifying correlations that manual extraction would overlook.</p>
        <p style={{ marginBottom: '1.5rem' }}>The system is designed not as a conversational interface, but as a rigorous analytical instrument. Queries are processed, validated against primary sources, and output as statistically sound visualizations and typeset reports.</p>
      </div>
    </div>

    <div style={customStyles.dividerTop}>
      <div style={{ ...customStyles.sansLabel, marginBottom: '1rem' }}>Data Extraction Architecture</div>
      <div style={customStyles.diagramContainer}>
        <DiagramExtraction />
      </div>
    </div>

    <div style={customStyles.dividerTop}>
      <div style={{ ...customStyles.sansLabel, marginBottom: '1rem' }}>System Validation Model</div>
      <div style={customStyles.diagramContainer}>
        <DiagramValidation />
      </div>
    </div>
  </article>
);

const RightPage = () => (
  <article style={customStyles.page}>
    <header style={customStyles.headerMarginalia}>
      <SansLabel>Generated Analysis</SansLabel>
      <SansLabel>Pg. 12</SansLabel>
    </header>

    <div style={{ marginTop: '4vw' }}>
      <div style={customStyles.agentQueryBlock}>
        <div style={customStyles.agentQueryBlockBar}></div>
        <div style={{ ...customStyles.sansLabel, color: '#2b579a', marginBottom: '0.5rem' }}>Agent Protocol Initiated</div>
        <div style={customStyles.queryInput}>
          "Analyze the correlation between renewable energy capacity expansion and atmospheric particulate matter (PM2.5) reduction in Western Europe, from 2005 to 2023."
        </div>
        <div style={{ ...customStyles.serifBody, ...customStyles.agentResponse }}>
          <p>Analysis complete. Querying World Bank Environmental Data and Global Energy Monitor arrays. A demonstrable inverse correlation exists. As renewable capacity (specifically wind and solar photovoltaic) scaled logarithmically post-2010, the derivative of PM2.5 concentrations steepened downwards. The inflection point observed in 2014 corresponds with the retirement of 42 GW of coal-fired generation capacity across the specified region.</p>
        </div>
      </div>

      <div style={{ ...customStyles.chartBlock, ...customStyles.dividerTop }}>
        <div style={customStyles.sansLabel}>Atmospheric Impact Modeling</div>
        <ChartAtmospheric />
        <div style={customStyles.figureCaption}>
          <span style={{ ...customStyles.sansLabel, color: '#6ba37b' }}>Fig 1.0</span>
          <SansMeta>Projected trajectory of particulate reduction across three tier-1 urban centers.</SansMeta>
        </div>
      </div>

      <div style={{ ...customStyles.chartBlock, ...customStyles.dividerTop }}>
        <div style={customStyles.sansLabel}>Energy Source Substitution Rates</div>
        <ChartEnergy />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div style={customStyles.legend}>
            <div style={customStyles.legendItem}>
              <div style={{ ...customStyles.legendDot, backgroundColor: '#6ba37b' }}></div>
              <SansMeta>Renewable Integration</SansMeta>
            </div>
            <div style={customStyles.legendItem}>
              <div style={{ ...customStyles.legendDot, backgroundColor: '#c95b4f' }}></div>
              <SansMeta>Transitional Fuels</SansMeta>
            </div>
            <div style={customStyles.legendItem}>
              <div style={{ ...customStyles.legendDot, backgroundColor: '#2b579a' }}></div>
              <SansMeta>Fossil Base-load</SansMeta>
            </div>
          </div>
          <div style={{ ...customStyles.sansMeta, textAlign: 'right', fontSize: '0.65rem', maxWidth: '200px' }}>
            Ref. A2: Global Energy Monitor dataset parsing complete. Margins of error &lt; 2.1%.
          </div>
        </div>
      </div>
    </div>
  </article>
);

const App = () => {
  useEffect(() => {
    const link1 = document.createElement('link');
    link1.rel = 'preconnect';
    link1.href = 'https://fonts.googleapis.com';
    document.head.appendChild(link1);

    const link2 = document.createElement('link');
    link2.rel = 'preconnect';
    link2.href = 'https://fonts.gstatic.com';
    link2.crossOrigin = 'anonymous';
    document.head.appendChild(link2);

    const link3 = document.createElement('link');
    link3.rel = 'stylesheet';
    link3.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap';
    document.head.appendChild(link3);

    const style = document.createElement('style');
    style.textContent = `
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body { background-color: #f6f6f4; }
      @media (max-width: 1024px) {
        .spread-responsive { grid-template-columns: 1fr !important; }
        .page-left-responsive { border-right: none !important; border-bottom: 1px solid #ebebeb; }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(link1);
      document.head.removeChild(link2);
      document.head.removeChild(link3);
      document.head.removeChild(style);
    };
  }, []);

  return (
    <div style={customStyles.body}>
      <div style={customStyles.pageContainer}>
        <div className="spread-responsive" style={customStyles.spread}>
          <div className="page-left-responsive">
            <LeftPage />
          </div>
          <RightPage />
        </div>
      </div>
    </div>
  );
};

export default App;