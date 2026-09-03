import React from 'react'
import { useStore } from './store'
import { translations } from './i18n'
import { DatasetImporter } from './components/DatasetImporter'
import { DatasetList } from './components/DatasetList'
import { ChatClaims } from './components/ChatClaims'
import { PhysicsLab } from './components/PhysicsLab'
import { DigitalTwin } from './components/DigitalTwin'

const App: React.FC = () => {
  const { activeTab, setActiveTab, datasets, addDataset, language, setLanguage } = useStore()
  const t = translations[language]

  const tabs = [
    { id: 'dashboard', label: t.dashboard },
    { id: 'chat', label: t.chat },
    { id: 'evidence', label: t.evidence },
    { id: 'intake', label: t.intake },
    { id: 'qc', label: t.qc },
    { id: 'physics', label: t.physics },
    { id: 'twin', label: t.twin },
    { id: 'replay', label: t.replay },
    { id: 'report', label: t.report },
    { id: 'audit', label: t.audit },
  ]

  return (
    <div className="app">
      <header className="header">
        <h1>🔬 QVE Verification Lab — Prototype 1</h1>
        <div className="language-toggle">
          <button onClick={() => setLanguage('en')} className={language === 'en' ? 'active' : ''}>EN</button>
          <button onClick={() => setLanguage('my')} className={language === 'my' ? 'active' : ''}>MY</button>
        </div>
      </header>

      <div className="main-container">
        <aside className="sidebar">
          <nav>
            <ul>
              {tabs.map((tab) => (
                <li key={tab.id}>
                  <button
                    onClick={() => setActiveTab(tab.id)}
                    className={activeTab === tab.id ? 'active' : ''}
                  >
                    {tab.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        <main className="content">
          <div className="strict-note">
            {t.strictNote}
          </div>

          {activeTab === 'dashboard' && (
            <div className="tab-content active">
              <h2>Dashboard</h2>
              <p>Welcome to QVE Verification Lab — Prototype 1</p>
              <p>Scientific evidence ledger + deterministic analysis + 3D digital twin</p>
              <p>✓ CSV and JSON import with SHA-256 hashing</p>
              <p>✓ Quality control checks and analysis</p>
              <p>✓ Evidence gates A-F for claim verification</p>
              <p>✓ Physics calculations (Casimir, radiation momentum)</p>
              <p>✓ 3D digital twin visualization (CONCEPTUAL / SIMULATION)</p>
              <p>✓ Immutable audit logging</p>
              <p>✓ Myanmar/English bilingual UI</p>
            </div>
          )}

          {activeTab === 'intake' && (
            <div className="tab-content active">
              <DatasetImporter onSuccess={(data) => addDataset(data)} />
              <DatasetList datasets={datasets} />
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="tab-content active">
              <ChatClaims />
            </div>
          )}

          {activeTab === 'physics' && (
            <div className="tab-content active">
              <PhysicsLab />
            </div>
          )}

          {activeTab === 'twin' && (
            <div className="tab-content active">
              <DigitalTwin />
            </div>
          )}

          {(activeTab === 'evidence' || activeTab === 'qc' || activeTab === 'replay' || activeTab === 'report' || activeTab === 'audit') && (
            <div className="tab-content active">
              <h2>{t[activeTab as keyof typeof t] || activeTab}</h2>
              <p>Feature under development</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
