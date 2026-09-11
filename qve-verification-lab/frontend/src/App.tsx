import React from 'react'
import { useStore } from './store'
import { translations } from './i18n'
import { DatasetImporter } from './components/DatasetImporter'
import { DatasetList } from './components/DatasetList'
import { ChatClaims } from './components/ChatClaims'
import { PhysicsLab } from './components/PhysicsLab'
import { DigitalTwin } from './components/DigitalTwin'
import './app_v23_theme.css'
import './v23FlightLab.css'

const nav = ['dashboard','mission','vehicle','telemetry','evidence','intake','qc','physics','twin','replay','report','audit'] as const
const metrics = [['VEHICLE MASS','11,450','kg'],['LENGTH','28.6','m'],['WIDTH','14.2','m'],['HEIGHT','7.8','m'],['ALTITUDE','390.0','km'],['VELOCITY','7.68','km/s'],['CABIN PRESSURE','14.00','psia'],['CABIN TEMP','2.41','°C']]
const sensors = [['Force','AFM / MEMS Sensor','SIMULATED'],['Power','Power Analyzer','SIMULATED'],['RF Spectrum','Rohde & Schwarz','SIMULATED'],['Magnetic','SQUID / Hall','SIMULATED'],['Temperature','PT100 / DS18B20','SIMULATED'],['Vibration','Inertial Sensor','SIMULATED']]

const App: React.FC = () => {
  const { activeTab, setActiveTab, datasets, addDataset, language, setLanguage } = useStore()
  const t = translations[language]
  const label = (id: string) => {
    if (id === 'mission') return language === 'my' ? 'မစ်ရှင်ထိန်းချုပ်ရေး' : 'Mission Control'
    if (id === 'vehicle') return language === 'my' ? 'ယာဉ်' : 'Vehicle'
    if (id === 'telemetry') return language === 'my' ? 'တယ်လီမက်ထရီ' : 'Telemetry'
    return (t as any)[id] || id[0].toUpperCase() + id.slice(1)
  }
  const Dashboard = () => <>
    <div className="metric-grid">{metrics.map(([a,b,c]) => <div className="metric" key={a}><label>{a}</label><strong>{b}</strong><em>{c}</em></div>)}</div>
    <div className="qve-hero">
      <section className="qve-card"><h2>QVE PROJECT v2.3 — D1 SPACE & FLIGHT LAB</h2><p className="qve-muted">Spacecraft reference geometry + laboratory digital twin • MODEL / SIMULATION unless supported by traceable instrument evidence.</p>
        <div className="ship-stage"><span className="ship-watermark">DIGITAL TWIN • NOT FLIGHT PROOF</span><span className="ship-label sl1">STRUCTURE</span><span className="ship-label sl2">POWER / THERMAL</span><span className="ship-label sl3">DAQ / FORCE PATH</span>
          <div className="ship"><div className="ship-cockpit"/><div className="ship-ridge"/><div className="engine"/><i className="sensor s1"/><i className="sensor s2"/><i className="sensor s3"/><i className="sensor s4"/></div>
        </div>
      </section>
      <section className="qve-card side-panel"><h3>{language === 'my' ? 'လက်တွေ့ Lab အခြေအနေ' : 'REAL-WORLD LAB STATUS'}</h3>
        <div className="status-line"><span>DAQ chain</span><b className="ok">READY</b></div><div className="status-line"><span>Calibration</span><b className="warn">REQUIRED</b></div><div className="status-line"><span>Independent power</span><b className="ok">REQUIRED</b></div><div className="status-line"><span>Force-path isolation</span><b className="ok">CONTROLLED</b></div><div className="status-line"><span>Flight/propulsion claim</span><b className="danger">LOCKED</b></div>
        <h3 style={{marginTop:6}}>EVIDENCE GATES</h3><div className="gate-grid">{['A Instrumentation','B Stability','C Repeatability','D Energy','E Momentum','F Replication'].map((x,i)=><div className="gate" key={x}><b>{x}</b><small>{i < 3 ? 'Configured' : 'Pending evidence'}</small></div>)}</div>
      </section>
    </div>
    <section className="qve-card telemetry"><h3>TELEMETRY REPLAY • SAMPLE / SIMULATION</h3><div className="timeline">{Array.from({length:72},(_,i)=><div className="bar" style={{height:`${16 + Math.abs(Math.sin(i*.34))*58 + ((i*13)%20)}%`}} key={i}/>)}</div><div className="timeline-meta"><span>T−120 s</span><span>CONTROLLED EVENT WINDOW</span><span>T+120 s</span></div></section>
    <div className="bottom-grid">
      <section className="qve-card"><h3>SENSOR / DAQ CHANNELS</h3><div className="sensor-grid">{sensors.map(([a,b,c])=><div className="sensor-box" key={a}><b>{a}</b><small>{b}</small><small>{c}</small></div>)}</div></section>
      <section className="qve-card"><h3>SPACE ENVIRONMENT</h3><div className="space-list"><div className="space-row"><span>Reference orbit</span><span>390 km / SIM</span></div><div className="space-row"><span>Velocity</span><span>7.68 km/s / SIM</span></div><div className="space-row"><span>Vacuum profile</span><span>MODEL</span></div><div className="space-row"><span>Thermal profile</span><span>MODEL</span></div><div className="space-row"><span>Radiation</span><span>MODEL</span></div></div></section>
      <section className="qve-card"><h3>DATA PROVENANCE</h3><p className="qve-muted">Imported datasets retain SHA-256 identity and evidence state. SIMULATED and SOURCE_REPORTED information cannot silently become VERIFIED.</p><div className="status-line"><span>Imported datasets</span><b>{datasets.length}</b></div><div className="status-line"><span>Raw overwrite</span><b className="ok">BLOCKED</b></div></section>
    </div>
  </>
  const Main = () => {
    if (['dashboard','mission','vehicle','telemetry'].includes(activeTab)) return <Dashboard />
    if (activeTab === 'intake') return <><DatasetImporter onSuccess={(data) => addDataset(data)}/><DatasetList datasets={datasets}/></>
    if (activeTab === 'chat') return <ChatClaims />
    if (activeTab === 'physics') return <PhysicsLab />
    if (activeTab === 'twin') return <DigitalTwin />
    return <section className="qve-card module-placeholder"><div><strong>{label(activeTab)}</strong><span>{language === 'my' ? 'Evidence-gated module — data provenance မပြည့်မီ အတည်ပြုမထားပါ။' : 'Evidence-gated module — imported/simulated data are not automatically verified.'}</span></div></section>
  }
  return <div className="app"><div className="qve-shell">
    <header className="qve-top"><div className="qve-brand">QVE PROJECT v2.3 <small>QUANTUM VACUUM ENERGY SPACECRAFT • SPACE & FLIGHT LAB CENTER</small></div><div className="qve-top-actions"><button className={language === 'en' ? 'active' : ''} onClick={() => setLanguage('en')}>EN</button><button className={language === 'my' ? 'active' : ''} onClick={() => setLanguage('my')}>မြန်မာ</button></div></header>
    <div className="qve-nav">{nav.map(id => <button key={id} onClick={() => setActiveTab(id)} className={activeTab === id ? 'active' : ''}>{label(id)}</button>)}</div>
    <div className="qve-badges"><span className="qve-badge sim">● SIMULATION / DIGITAL TWIN</span><span className="qve-badge evidence">● EVIDENCE GATE ACTIVE</span></div>
    <Main />
    <footer className="qve-foot"><span>QVE • D1 LAB • v2.3</span><span>MODEL ≠ MEASUREMENT ≠ VERIFIED</span></footer>
  </div></div>
}
export default App
