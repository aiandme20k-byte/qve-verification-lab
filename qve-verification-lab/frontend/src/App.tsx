import React from 'react'
import { useStore } from './store'
import { translations } from './i18n'
import { DatasetImporter } from './components/DatasetImporter'
import { DatasetList } from './components/DatasetList'
import { ChatClaims } from './components/ChatClaims'
import { PhysicsLab } from './components/PhysicsLab'
import { DigitalTwin } from './components/DigitalTwin'
import './app_v23_theme.css'

const nav = ['dashboard','mission','vehicle','telemetry','evidence','intake','qc','physics','twin','replay','report','audit'] as const
const metrics = [['VEHICLE MASS','11,450','kg'],['LENGTH','28.6','m'],['WIDTH','14.2','m'],['HEIGHT','7.8','m'],['ALTITUDE','390.0','km'],['VELOCITY','7.68','km/s'],['CABIN PRESSURE','14.00','psia'],['CABIN TEMP','2.41','°C']]

const App: React.FC = () => {
  const { activeTab, setActiveTab, datasets, addDataset, language, setLanguage } = useStore()
  const t = translations[language]
  const label = (id:string) => id==='mission'?'Mission Control':id==='vehicle'?'Vehicle':id==='telemetry'?'Telemetry':(t as any)[id] || id[0].toUpperCase()+id.slice(1)
  const Dashboard = () => <>
    <div className="metric-grid">{metrics.map(([a,b,c])=><div className="metric" key={a}><label>{a}</label><strong>{b}</strong><em>{c}</em></div>)}</div>
    <div className="qve-grid" style={{marginTop:14}}>
      <section className="qve-card"><h2>QVE PROJECT v2.3 — D1 LAB DIGITAL TWIN</h2><p className="qve-muted">Design-1 laboratory verification article • spacecraft reference geometry shown as MODEL / SIMULATION only</p><div className="ship-stage"><span className="ship-watermark">VISUALIZATION • NOT FLIGHT PROOF</span><div className="ship"><div className="engine"/><i className="sensor s1"/><i className="sensor s2"/><i className="sensor s3"/><i className="sensor s4"/></div><div className="legend"><span>STRUCTURE</span><span>POWER</span><span>SENSORS</span><span>DAQ</span><span>THERMAL</span></div></div></section>
      <section className="qve-card"><h3>REAL-WORLD LAB STATUS</h3><div className="alert-list"><div className="alert"><span>DAQ chain</span><b className="ok">READY / CONFIGURED</b></div><div className="alert"><span>Calibration</span><b className="warn">REQUIRED BEFORE RUN</b></div><div className="alert"><span>Mechanical force path</span><b className="ok">CONTROLLED</b></div><div className="alert"><span>Independent power</span><b className="ok">REQUIRED</b></div><div className="alert"><span>Flight claim gate</span><b className="bad">LOCKED</b></div></div><h3 style={{marginTop:18}}>EVIDENCE GATES</h3><div className="gates">{['Raw hash','Calibration','QC','Analysis','Replication','Review'].map((x,i)=><div className="gate" key={x}><b>G{i+1} {x}</b><small>{i<3?'CONFIGURED':'WORKFLOW'}</small></div>)}</div></section>
    </div>
    <section className="qve-card" style={{marginTop:14}}><h3>TELEMETRY REPLAY — SIMULATION SAMPLE</h3><div className="timeline">{Array.from({length:64},(_,i)=><div className="bar" style={{height:`${20+Math.abs(Math.sin(i*.42))*55+((i*17)%18)}%`}} key={i}/>)}</div><div className="timeline-line"><span>T−60 s</span><span>CONTROLLED EVENT</span><span>T+60 s</span></div></section>
  </>
  const Main = () => {
    if(activeTab==='dashboard'||activeTab==='mission'||activeTab==='vehicle'||activeTab==='telemetry') return <Dashboard />
    if(activeTab==='intake') return <><DatasetImporter onSuccess={(data)=>addDataset(data)}/><DatasetList datasets={datasets}/></>
    if(activeTab==='chat') return <ChatClaims />
    if(activeTab==='physics') return <PhysicsLab />
    if(activeTab==='twin') return <DigitalTwin />
    return <section className="qve-card"><h2>{label(activeTab)}</h2><p className="qve-muted">This module remains evidence-gated. Imported or simulated data are not automatically promoted to independently verified measurements.</p><div className="gates">{['MODEL','SIMULATED','ACTUAL_DATA','CALCULATED','INCONCLUSIVE','VERIFIED'].map(x=><div className="gate" key={x}><b>{x}</b><small>Evidence state</small></div>)}</div></section>
  }
  return <div className="app"><div className="qve-shell"><header className="qve-top"><div className="qve-brand">QVE PROJECT v2.3 <small>QUANTUM VACUUM ENERGY SPACECRAFT • VERIFICATION LAB</small></div><div><button onClick={()=>setLanguage('en')}>EN</button> <button onClick={()=>setLanguage('my')}>မြန်မာ</button></div></header><div className="qve-nav">{nav.map(id=><button key={id} onClick={()=>setActiveTab(id)} className={activeTab===id?'active':''}>{label(id)}</button>)}</div><div style={{marginBottom:12}}><span className="qve-badge sim">● SIMULATION / DIGITAL TWIN</span> <span className="qve-badge actual">● EVIDENCE GATE ACTIVE</span></div><Main /></div></div>
}
export default App
