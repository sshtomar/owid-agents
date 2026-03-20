import React, { useState } from 'react';

const customStyles = {
  root: {
    '--bg-pure': '#ffffff',
    '--bg-subtle': '#f8fafc',
    '--bg-workspace': '#f1f5f9',
    '--bg-hover': '#f1f5f9',
    '--text-main': '#0f172a',
    '--text-muted': '#64748b',
    '--text-number': '#94a3b8',
    '--border-color': '#e2e8f0',
    '--border-strong': '#0f172a',
    '--accent': '#2563eb',
    '--accent-secondary': '#10b981',
  },
  body: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    backgroundColor: '#f1f5f9',
    color: '#0f172a',
    fontSize: '13px',
    lineHeight: '1.5',
    height: '100vh',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
    WebkitFontSmoothing: 'antialiased',
  },
  appHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px 32px',
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e2e8f0',
    height: '56px',
    flexShrink: 0,
    zIndex: 10,
  },
  logo: {
    fontSize: '16px',
    fontWeight: 600,
    letterSpacing: '-0.02em',
    color: '#0f172a',
  },
  headerNav: {
    display: 'flex',
    gap: '24px',
    color: '#64748b',
  },
  navLink: {
    textDecoration: 'none',
    color: '#64748b',
    fontWeight: 500,
    cursor: 'pointer',
  },
  navLinkActive: {
    textDecoration: 'none',
    color: '#2563eb',
    fontWeight: 500,
    cursor: 'pointer',
  },
  workspace: {
    display: 'flex',
    flex: 1,
    overflow: 'hidden',
    backgroundColor: '#f1f5f9',
  },
  dataCanvas: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    margin: '16px',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    overflowY: 'auto',
  },
  canvasHeader: {
    padding: '32px 32px 16px',
    borderBottom: '1px solid #e2e8f0',
  },
  breadcrumb: {
    color: '#2563eb',
    marginBottom: '16px',
    fontSize: '12px',
    fontWeight: 600,
    letterSpacing: '0.02em',
  },
  h1: {
    fontSize: '24px',
    fontWeight: 700,
    letterSpacing: '-0.03em',
    lineHeight: 1.1,
    marginBottom: '8px',
    color: '#0f172a',
  },
  comparisonMeta: {
    display: 'flex',
    gap: '32px',
    marginTop: '16px',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '12px',
    fontWeight: 500,
    color: '#64748b',
  },
  legendDot: {
    width: '10px',
    height: '10px',
    borderRadius: '2px',
  },
  chartGrid: {
    padding: '32px',
    display: 'flex',
    flexDirection: 'column',
    gap: '48px',
    flex: 1,
  },
  chartSection: {
    position: 'relative',
  },
  sectionLabel: {
    fontSize: '11px',
    textTransform: 'uppercase',
    fontWeight: 700,
    color: '#64748b',
    letterSpacing: '0.05em',
    marginBottom: '24px',
  },
  chartWrapper: {
    paddingLeft: '45px',
    position: 'relative',
  },
  yAxis: {
    position: 'absolute',
    left: 0,
    top: 0,
    bottom: '16px',
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    pointerEvents: 'none',
  },
  yLine: {
    width: '100%',
    borderTop: '1px solid #e2e8f0',
    position: 'relative',
  },
  yLabel: {
    position: 'absolute',
    left: '-40px',
    top: '-8px',
    fontSize: '10px',
    color: '#64748b',
    fontWeight: 500,
  },
  chartStage: {
    height: '180px',
    display: 'flex',
    alignItems: 'flex-end',
    gap: '6px',
    paddingBottom: '16px',
    borderBottom: '2px solid #0f172a',
    position: 'relative',
  },
  xAxis: {
    display: 'flex',
    justifyContent: 'space-between',
    paddingTop: '8px',
    color: '#64748b',
    fontSize: '11px',
    fontWeight: 500,
  },
  agentPanel: {
    width: '420px',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    margin: '16px 16px 16px 0',
    border: '1px solid #e2e8f0',
    borderRadius: '8px',
    flexShrink: 0,
    overflow: 'hidden',
  },
  agentHeader: {
    padding: '16px 32px',
    borderBottom: '1px solid #e2e8f0',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontWeight: 600,
    backgroundColor: '#f8fafc',
  },
  statusIndicator: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    fontSize: '11px',
    color: '#2563eb',
    fontWeight: 700,
    textTransform: 'uppercase',
  },
  dot: {
    width: '8px',
    height: '8px',
    backgroundColor: '#2563eb',
    borderRadius: '50%',
    boxShadow: '0 0 0 2px rgba(37, 99, 235, 0.2)',
  },
  agentTimeline: {
    flex: 1,
    overflowY: 'auto',
  },
  timelineItemUser: {
    padding: '24px 32px',
    borderBottom: '1px solid #e2e8f0',
    backgroundColor: '#ffffff',
  },
  timelineItemAgent: {
    padding: '24px 32px',
    borderBottom: '1px solid #e2e8f0',
    backgroundColor: '#f8fafc',
  },
  timelineItemAgentAlt: {
    padding: '24px 32px',
    borderBottom: '1px solid #e2e8f0',
    backgroundColor: '#ffffff',
  },
  messageMeta: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '8px',
    fontSize: '11px',
    color: '#64748b',
    textTransform: 'uppercase',
    fontWeight: 600,
  },
  messageContent: {
    fontSize: '13px',
    lineHeight: '1.6',
    color: '#0f172a',
  },
  correlationStat: {
    background: '#ffffff',
    border: '1px solid #e2e8f0',
    borderRadius: '6px',
    padding: '16px',
    marginTop: '16px',
  },
  statGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '16px',
    marginTop: '8px',
  },
  miniStatLabel: {
    fontSize: '10px',
    color: '#64748b',
    textTransform: 'uppercase',
    fontWeight: 700,
  },
  miniStatValue: {
    fontSize: '16px',
    fontWeight: 700,
  },
  agentInputContainer: {
    padding: '16px 32px',
    borderTop: '1px solid #e2e8f0',
    backgroundColor: '#f8fafc',
  },
  inputWrapper: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  agentInput: {
    width: '100%',
    border: '1px solid #e2e8f0',
    padding: '12px 16px',
    paddingRight: '48px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    fontSize: '13px',
    borderRadius: '6px',
    outline: 'none',
    background: '#ffffff',
  },
  submitBtn: {
    position: 'absolute',
    right: '8px',
    background: '#2563eb',
    color: '#ffffff',
    border: 'none',
    width: '32px',
    height: '32px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    borderRadius: '4px',
  },
  icon: {
    width: '16px',
    height: '16px',
    stroke: 'currentColor',
    strokeWidth: 2,
    fill: 'none',
  },
};

const Bar = ({ heightPercent, type, active }) => {
  const baseStyle = {
    flex: 1,
    borderRadius: '2px 2px 0 0',
    transition: 'height 0.5s ease',
    height: `${heightPercent}%`,
  };

  let bgColor = '#e2e8f0';
  if (type === 'emissions') bgColor = active ? '#2563eb' : '#cbd5e1';
  if (type === 'renewables') bgColor = active ? '#10b981' : '#d1fae5';

  return <div style={{ ...baseStyle, backgroundColor: bgColor }} />;
};

const emissionsBars = [
  { height: 45 }, { height: 48 }, { height: 52 }, { height: 60 }, { height: 65 },
  { height: 72 }, { height: 80 }, { height: 85 }, { height: 88 }, { height: 90 },
  { height: 92, active: true },
];

const renewablesBars = [
  { height: 12 }, { height: 15 }, { height: 18 }, { height: 25 }, { height: 32 },
  { height: 42 }, { height: 55 }, { height: 68 }, { height: 78 }, { height: 88 },
  { height: 96, active: true },
];

const App = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'user',
      content: 'Compare the rate of change between CO2 emissions and renewable growth over the last decade. Is the green energy transition actually slowing down emission growth?',
    },
    {
      id: 2,
      type: 'agent-analysis',
      content: null,
    },
    {
      id: 3,
      type: 'agent-insight',
      content: 'Analysis suggests a "Decoupling Threshold" has not yet been reached globally. However, in EU-27 markets, I see a -0.62 inverse correlation, suggesting successful displacement.',
    },
  ]);

  const handleSubmit = () => {
    if (inputValue.trim()) {
      const newMessage = {
        id: messages.length + 1,
        type: 'user',
        content: inputValue.trim(),
      };
      setMessages([...messages, newMessage]);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSubmit();
  };

  return (
    <div style={customStyles.body}>
      <header style={customStyles.appHeader}>
        <div style={customStyles.logo}>DataWorld / Agents</div>
        <nav style={customStyles.headerNav}>
          <a style={customStyles.navLink} href="#">Energy</a>
          <a style={customStyles.navLink} href="#">Environment</a>
          <a style={customStyles.navLink} href="#">Health</a>
          <a style={customStyles.navLinkActive} href="#">Models</a>
        </nav>
      </header>

      <div style={customStyles.workspace}>
        <main style={customStyles.dataCanvas}>
          <header style={customStyles.canvasHeader}>
            <div style={customStyles.breadcrumb}>Comparison / Emissions vs. Renewables</div>
            <h1 style={customStyles.h1}>CO₂ Emissions &amp; Renewable Growth Correlation</h1>
            <div style={customStyles.comparisonMeta}>
              <div style={customStyles.legendItem}>
                <div style={{ ...customStyles.legendDot, background: '#2563eb' }}></div>
                Global CO₂ Emissions (Billion Tonnes)
              </div>
              <div style={customStyles.legendItem}>
                <div style={{ ...customStyles.legendDot, background: '#10b981' }}></div>
                Renewable Capacity (Terawatt-hours)
              </div>
            </div>
          </header>

          <div style={customStyles.chartGrid}>
            <div style={customStyles.chartSection}>
              <div style={customStyles.sectionLabel}>Dataset 01: Annual Global CO₂ Emissions</div>
              <div style={customStyles.chartWrapper}>
                <div style={customStyles.yAxis}>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>40B</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>30B</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>20B</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>10B</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>0</span></div>
                </div>
                <div style={customStyles.chartStage}>
                  {emissionsBars.map((bar, i) => (
                    <Bar key={i} heightPercent={bar.height} type="emissions" active={!!bar.active} />
                  ))}
                </div>
              </div>
            </div>

            <div style={customStyles.chartSection}>
              <div style={customStyles.sectionLabel}>Dataset 02: Global Renewable Energy Capacity</div>
              <div style={customStyles.chartWrapper}>
                <div style={customStyles.yAxis}>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>10k</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>7.5k</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>5k</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>2.5k</span></div>
                  <div style={customStyles.yLine}><span style={customStyles.yLabel}>0</span></div>
                </div>
                <div style={customStyles.chartStage}>
                  {renewablesBars.map((bar, i) => (
                    <Bar key={i} heightPercent={bar.height} type="renewables" active={!!bar.active} />
                  ))}
                </div>
                <div style={customStyles.xAxis}>
                  <span>2012</span>
                  <span>2014</span>
                  <span>2016</span>
                  <span>2018</span>
                  <span>2020</span>
                  <span style={{ color: '#2563eb', fontWeight: 700 }}>2022</span>
                </div>
              </div>
            </div>
          </div>

          <div style={{ padding: '32px', borderTop: '1px solid #e2e8f0', display: 'flex', gap: '48px' }}>
            <div>
              <h4 style={{ fontSize: '11px', textTransform: 'uppercase', color: '#64748b', marginBottom: '4px' }}>Sync Mode</h4>
              <p style={{ fontWeight: 600 }}>Multi-Axis Time Series (Active)</p>
            </div>
            <div>
              <h4 style={{ fontSize: '11px', textTransform: 'uppercase', color: '#64748b', marginBottom: '4px' }}>Data Granularity</h4>
              <p style={{ fontWeight: 600 }}>Annualized</p>
            </div>
          </div>
        </main>

        <aside style={customStyles.agentPanel}>
          <div style={customStyles.agentHeader}>
            <span>Research Agent</span>
            <div style={customStyles.statusIndicator}>
              <div style={customStyles.dot}></div> Active
            </div>
          </div>

          <div style={customStyles.agentTimeline}>
            {messages.map((msg) => {
              if (msg.type === 'user') {
                return (
                  <div key={msg.id} style={customStyles.timelineItemUser}>
                    <div style={customStyles.messageMeta}>
                      <svg style={customStyles.icon} viewBox="0 0 24 24">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                        <circle cx="12" cy="7" r="4" />
                      </svg>
                      User
                    </div>
                    <div style={customStyles.messageContent}>{msg.content}</div>
                  </div>
                );
              }

              if (msg.type === 'agent-analysis') {
                return (
                  <div key={msg.id} style={customStyles.timelineItemAgent}>
                    <div style={customStyles.messageMeta}>
                      <svg style={customStyles.icon} viewBox="0 0 24 24">
                        <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
                        <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
                        <line x1="6" y1="6" x2="6.01" y2="6" />
                        <line x1="6" y1="18" x2="6.01" y2="18" />
                      </svg>
                      Correlation Analysis
                    </div>
                    <div style={customStyles.messageContent}>
                      I've calculated the Pearson correlation coefficient and indexed growth rates for both datasets from 2012–2022.
                      <div style={customStyles.correlationStat}>
                        <div style={customStyles.miniStatLabel}>Correlation (R)</div>
                        <div style={customStyles.miniStatValue}>
                          0.84{' '}
                          <span style={{ fontSize: '12px', fontWeight: 400, color: '#64748b' }}>(Strong Positive)</span>
                        </div>
                        <div style={customStyles.statGrid}>
                          <div>
                            <div style={customStyles.miniStatLabel}>CO2 CAGR</div>
                            <div style={{ ...customStyles.miniStatValue, color: '#ef4444' }}>+0.7%</div>
                          </div>
                          <div>
                            <div style={customStyles.miniStatLabel}>Renewables CAGR</div>
                            <div style={{ ...customStyles.miniStatValue, color: '#10b981' }}>+8.2%</div>
                          </div>
                        </div>
                      </div>
                      <p style={{ marginTop: '16px' }}>
                        While renewable growth is outstripping emissions growth by a factor of 10x, the absolute volume of fossil fuel combustion in developing markets still offsets the green transition gains.
                      </p>
                    </div>
                  </div>
                );
              }

              if (msg.type === 'agent-insight') {
                return (
                  <div key={msg.id} style={customStyles.timelineItemAgentAlt}>
                    <div style={customStyles.messageMeta}>
                      <svg style={{ ...customStyles.icon, color: '#2563eb' }} viewBox="0 0 24 24">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                      </svg>
                      Agent Insight
                    </div>
                    <div style={customStyles.messageContent}>
                      Analysis suggests a <span style={{ fontWeight: 600 }}>"Decoupling Threshold"</span> has not yet been reached globally. However, in EU-27 markets, I see a -0.62 inverse correlation, suggesting successful displacement.
                    </div>
                  </div>
                );
              }

              return null;
            })}
          </div>

          <div style={customStyles.agentInputContainer}>
            <div style={customStyles.inputWrapper}>
              <input
                type="text"
                style={customStyles.agentInput}
                placeholder="Ask about this correlation..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
              />
              <button style={customStyles.submitBtn} onClick={handleSubmit}>
                <svg viewBox="0 0 24 24" style={{ width: '16px', height: '16px', stroke: '#ffffff', strokeWidth: 2, fill: 'none' }}>
                  <line x1="5" y1="12" x2="19" y2="12" />
                  <polyline points="12 5 19 12 12 19" />
                </svg>
              </button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default App;