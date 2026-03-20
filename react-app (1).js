import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

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
  },
};

const UserIcon = () => (
  <svg style={{ width: 16, height: 16, stroke: 'currentColor', strokeWidth: 2, fill: 'none' }} viewBox="0 0 24 24">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
);

const ServerIcon = () => (
  <svg style={{ width: 16, height: 16, stroke: 'currentColor', strokeWidth: 2, fill: 'none' }} viewBox="0 0 24 24">
    <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
    <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
    <line x1="6" y1="6" x2="6.01" y2="6" />
    <line x1="6" y1="18" x2="6.01" y2="18" />
  </svg>
);

const ChatIcon = ({ color }) => (
  <svg style={{ width: 16, height: 16, stroke: color || 'currentColor', strokeWidth: 2, fill: 'none' }} viewBox="0 0 24 24">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);

const ArrowIcon = () => (
  <svg viewBox="0 0 24 24" style={{ width: 16, height: 16, fill: 'none', stroke: 'currentColor', strokeWidth: 2.5 }}>
    <line x1="5" y1="12" x2="19" y2="12" />
    <polyline points="12 5 19 12 12 19" />
  </svg>
);

const barData = [
  { value: 'low', height: '15%' },
  { value: 'low', height: '18%' },
  { value: 'low', height: '20%' },
  { value: 'med', height: '25%' },
  { value: 'med', height: '32%' },
  { value: 'med', height: '45%' },
  { value: 'high', height: '55%' },
  { value: 'high', height: '68%' },
  { value: 'high', height: '75%' },
  { value: 'high', height: '82%' },
  { value: 'high', height: '88%' },
  { value: 'agent-focus', height: '92%' },
];

const getBarColor = (value, isHovered) => {
  if (value === 'agent-focus') return '#2563eb';
  if (isHovered) return '#cbd5e1';
  if (value === 'high') return '#cbd5e1';
  if (value === 'med') return '#e2e8f0';
  return '#f1f5f9';
};

const BarChart = () => {
  const [hoveredBar, setHoveredBar] = useState(null);

  return (
    <div style={{ paddingLeft: 45, position: 'relative' }}>
      <div style={{
        position: 'absolute',
        left: 0,
        top: 0,
        bottom: 16,
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        pointerEvents: 'none',
      }}>
        {['40B', '30B', '20B', '10B', '0'].map((label) => (
          <div key={label} style={{ width: '100%', borderTop: '1px solid #e2e8f0', position: 'relative' }}>
            <span style={{ position: 'absolute', left: -35, top: -8, fontSize: 10, color: '#64748b', fontWeight: 500 }}>
              {label}
            </span>
          </div>
        ))}
      </div>

      <div style={{
        height: 300,
        display: 'flex',
        alignItems: 'flex-end',
        gap: 4,
        paddingBottom: 16,
        borderBottom: '2px solid #0f172a',
        position: 'relative',
      }}>
        {barData.map((bar, i) => (
          <div
            key={i}
            style={{
              flex: 1,
              height: bar.height,
              backgroundColor: getBarColor(bar.value, hoveredBar === i),
              transition: 'background-color 0.2s, height 0.5s',
              position: 'relative',
              zIndex: 1,
              cursor: 'pointer',
            }}
            onMouseEnter={() => setHoveredBar(i)}
            onMouseLeave={() => setHoveredBar(null)}
          />
        ))}
      </div>

      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        paddingTop: 8,
        color: '#64748b',
        fontSize: 11,
        fontWeight: 500,
      }}>
        <span>1950</span>
        <span>1970</span>
        <span>1990</span>
        <span>2010</span>
        <span style={{ color: '#2563eb', fontWeight: 700 }}>2022</span>
      </div>
    </div>
  );
};

const ChartControls = () => {
  const [active, setActive] = useState('Global');
  const pills = ['Global', 'By Region', 'Per Capita'];

  return (
    <div style={{ display: 'flex', gap: 16, marginBottom: 24 }}>
      {pills.map((pill) => (
        <button
          key={pill}
          onClick={() => setActive(pill)}
          style={{
            padding: '6px 16px',
            border: active === pill ? '1px solid #2563eb' : '1px solid #e2e8f0',
            borderRadius: 9999,
            fontSize: 12,
            background: active === pill ? '#2563eb' : '#ffffff',
            color: active === pill ? '#ffffff' : '#64748b',
            cursor: 'pointer',
            transition: 'all 0.2s',
            fontWeight: 500,
            fontFamily: 'inherit',
          }}
        >
          {pill}
        </button>
      ))}
    </div>
  );
};

const AgentPanel = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([
    {
      type: 'user',
      content: 'Analyze the spike in 2022. What factors drove the increase despite renewable energy growth?',
    },
    {
      type: 'agent-process',
      tasks: [
        { num: '01', title: 'Querying sectoral breakdown for 2021-2022', desc: 'Source: Global Carbon Budget 2023' },
        { num: '02', title: 'Cross-referencing with global events', desc: 'Identifying post-pandemic rebound effects.' },
      ],
    },
    {
      type: 'agent-response',
      content: null,
    },
  ]);

  const handleSend = () => {
    if (!inputValue.trim()) return;
    setMessages((prev) => [
      ...prev,
      { type: 'user', content: inputValue.trim() },
    ]);
    setInputValue('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <aside style={{
      width: 400,
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#ffffff',
      margin: '16px 16px 16px 0',
      border: '1px solid #e2e8f0',
      borderRadius: 8,
      flexShrink: 0,
      overflow: 'hidden',
    }}>
      <div style={{
        padding: '16px 32px',
        borderBottom: '1px solid #e2e8f0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontWeight: 600,
        backgroundColor: '#f8fafc',
        fontSize: 13,
      }}>
        <span>Research Agent</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: '#2563eb', fontWeight: 700, textTransform: 'uppercase' }}>
          <div style={{
            width: 8,
            height: 8,
            backgroundColor: '#2563eb',
            borderRadius: '50%',
            boxShadow: '0 0 0 2px rgba(37, 99, 235, 0.2)',
          }} />
          Active
        </div>
      </div>

      <div style={{ flex: 1, overflowY: 'auto' }}>
        {messages.map((msg, i) => {
          if (msg.type === 'user') {
            return (
              <div key={i} style={{ padding: '24px 32px', borderBottom: '1px solid #e2e8f0', backgroundColor: '#ffffff' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, fontSize: 11, color: '#64748b', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.05em' }}>
                  <UserIcon /> User
                </div>
                <div style={{ fontSize: 13, lineHeight: 1.6, color: '#0f172a' }}>{msg.content}</div>
              </div>
            );
          }
          if (msg.type === 'agent-process') {
            return (
              <div key={i} style={{ padding: '24px 32px', borderBottom: '1px solid #e2e8f0', backgroundColor: '#f8fafc' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, fontSize: 11, color: '#64748b', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.05em' }}>
                  <ServerIcon /> Agent Process
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 16 }}>
                  {msg.tasks.map((task, j) => (
                    <div key={j} style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
                      <span style={{ color: '#2563eb', fontSize: 11, fontWeight: 700, width: 16, paddingTop: 2 }}>{task.num}</span>
                      <div style={{ flex: 1, borderBottom: j < msg.tasks.length - 1 ? '1px solid #e2e8f0' : 'none', paddingBottom: j < msg.tasks.length - 1 ? 8 : 0 }}>
                        <div style={{ fontWeight: 600, marginBottom: 2, color: '#0f172a', fontSize: 13 }}>{task.title}</div>
                        <div style={{ color: '#64748b', fontSize: 12 }}>{task.desc}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          }
          if (msg.type === 'agent-response') {
            return (
              <div key={i} style={{ padding: '24px 32px', borderBottom: '1px solid #e2e8f0', backgroundColor: '#ffffff' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, fontSize: 11, color: '#64748b', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.05em' }}>
                  <ChatIcon color="#2563eb" /> Agent Response
                </div>
                <div style={{ fontSize: 13, lineHeight: 1.6, color: '#0f172a' }}>
                  The <span style={{ color: '#2563eb', fontWeight: 600 }}>0.9% increase</span> in 2022 was primarily driven by:
                  <br /><br />
                  1. A strong rebound in international aviation.<br />
                  2. An increase in coal usage due to high natural gas prices.
                </div>
              </div>
            );
          }
          return null;
        })}
      </div>

      <div style={{ padding: '16px 32px', borderTop: '1px solid #e2e8f0', backgroundColor: '#f8fafc' }}>
        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about this dataset..."
            style={{
              width: '100%',
              border: '1px solid #e2e8f0',
              padding: '12px 16px',
              paddingRight: 48,
              fontFamily: 'inherit',
              fontSize: 13,
              borderRadius: 6,
              outline: 'none',
              backgroundColor: '#ffffff',
              color: '#0f172a',
              transition: 'border-color 0.2s, box-shadow 0.2s',
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#2563eb';
              e.target.style.boxShadow = '0 0 0 3px rgba(37, 99, 235, 0.1)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = '#e2e8f0';
              e.target.style.boxShadow = 'none';
            }}
          />
          <button
            onClick={handleSend}
            aria-label="Send message"
            style={{
              position: 'absolute',
              right: 8,
              background: '#2563eb',
              color: '#ffffff',
              border: 'none',
              width: 32,
              height: 32,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              borderRadius: 4,
              transition: 'opacity 0.2s',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.opacity = '0.9')}
            onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
          >
            <ArrowIcon />
          </button>
        </div>
      </div>
    </aside>
  );
};

const Header = () => {
  const navItems = [
    { label: 'Energy', active: false },
    { label: 'Environment', active: false },
    { label: 'Health', active: false },
    { label: 'Models', active: true },
  ];

  return (
    <header style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '16px 32px',
      backgroundColor: '#ffffff',
      borderBottom: '1px solid #e2e8f0',
      height: 56,
      flexShrink: 0,
      zIndex: 10,
    }}>
      <div style={{ fontSize: 16, fontWeight: 600, letterSpacing: '-0.02em', color: '#0f172a' }}>
        DataWorld / Agents
      </div>
      <nav style={{ display: 'flex', gap: 24, color: '#64748b' }}>
        {navItems.map((item) => (
          <a
            key={item.label}
            href="#"
            onClick={(e) => e.preventDefault()}
            style={{
              textDecoration: 'none',
              color: item.active ? '#2563eb' : '#64748b',
              transition: 'color 0.2s',
              fontWeight: 500,
              fontSize: 13,
            }}
            onMouseEnter={(e) => { if (!item.active) e.currentTarget.style.color = '#2563eb'; }}
            onMouseLeave={(e) => { if (!item.active) e.currentTarget.style.color = '#64748b'; }}
          >
            {item.label}
          </a>
        ))}
      </nav>
    </header>
  );
};

const MainCanvas = () => (
  <main style={{
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#ffffff',
    margin: 16,
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    overflowY: 'auto',
  }}>
    <header style={{ padding: '32px 32px 16px' }}>
      <div style={{ color: '#2563eb', marginBottom: 16, fontSize: 12, fontWeight: 600, letterSpacing: '0.02em' }}>
        Environment / Climate Change / CO2 Emissions
      </div>
      <h1 style={{ fontSize: 28, fontWeight: 700, letterSpacing: '-0.03em', lineHeight: 1.1, marginBottom: 8, color: '#0f172a' }}>
        Annual global CO₂ emissions
      </h1>
      <p style={{ color: '#64748b', fontSize: 14, maxWidth: 600 }}>
        Measured in billion tonnes per year. Includes emissions from fossil fuels and industry. Land-use change is not included.
      </p>
    </header>

    <div style={{ padding: 32, borderBottom: '1px solid #e2e8f0' }}>
      <ChartControls />
      <BarChart />
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', borderBottom: '1px solid #e2e8f0' }}>
      {[
        { label: 'Latest Value (2022)', value: '37.15B t', color: '#0f172a' },
        { label: 'YOY Growth', value: '+0.9%', color: '#2563eb' },
        { label: 'Primary Source', value: 'Coal (41%)', color: '#0f172a' },
      ].map((stat, i, arr) => (
        <div key={stat.label} style={{
          padding: '24px 32px',
          borderRight: i < arr.length - 1 ? '1px solid #e2e8f0' : 'none',
        }}>
          <div style={{ color: '#64748b', fontSize: 12, marginBottom: 4, fontWeight: 500 }}>{stat.label}</div>
          <div style={{ fontSize: 24, fontWeight: 700, letterSpacing: '-0.02em', color: stat.color }}>{stat.value}</div>
        </div>
      ))}
    </div>

    <div style={{ padding: 32 }}>
      <h3 style={{ fontWeight: 600, marginBottom: 16, color: '#0f172a', fontSize: 13 }}>Dataset Methodology</h3>
      <p style={{ color: '#64748b', maxWidth: 800, lineHeight: 1.6, fontSize: 13 }}>
        Data is sourced from the Global Carbon Project. Emissions from fossil fuels and industry include emissions from coal, oil, gas, cement production, and flaring.
      </p>
    </div>
  </main>
);

const HomePage = () => (
  <div style={{
    display: 'flex',
    flex: 1,
    overflow: 'hidden',
    backgroundColor: '#f1f5f9',
  }}>
    <MainCanvas />
    <AgentPanel />
  </div>
);

const App = () => {
  useEffect(() => {
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
    document.body.style.backgroundColor = '#f1f5f9';
    document.body.style.color = '#0f172a';
    document.body.style.fontSize = '13px';
    document.body.style.lineHeight = '1.5';
    document.body.style.WebkitFontSmoothing = 'antialiased';
    document.documentElement.style.height = '100%';
    document.body.style.height = '100%';
  }, []);

  return (
    <Router basename="/">
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;