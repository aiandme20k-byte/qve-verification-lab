import React, { useState } from 'react'
import { physicsService } from '../api'

export const PhysicsLab: React.FC = () => {
  const [casimirArea, setCasimirArea] = useState(1.0)
  const [casimirGap, setCasimirGap] = useState(10)
  const [casimirResult, setCasimirResult] = useState<any>(null)
  const [radiationEnergy, setRadiationEnergy] = useState(1.0)
  const [radiationResult, setRadiationResult] = useState<any>(null)

  const handleCasimirCalc = async () => {
    try {
      const result = await physicsService.calculateCasimir(casimirArea, casimirGap)
      setCasimirResult(result)
    } catch (err) {
      console.error('Casimir calc failed:', err)
    }
  }

  const handleRadiationCalc = async () => {
    try {
      const result = await physicsService.calculateRadiation(radiationEnergy)
      setRadiationResult(result)
    } catch (err) {
      console.error('Radiation calc failed:', err)
    }
  }

  return (
    <div className="physics-lab">
      <h3>Physics Lab</h3>
      
      <div className="calculation-box">
        <h4>Casimir Force Calculator</h4>
        <label>
          Area (m²):
          <input type="number" value={casimirArea} onChange={(e) => setCasimirArea(parseFloat(e.target.value))} />
        </label>
        <label>
          Gap (nm):
          <input type="number" value={casimirGap} onChange={(e) => setCasimirGap(parseFloat(e.target.value))} />
        </label>
        <button onClick={handleCasimirCalc}>Calculate</button>
        {casimirResult && (
          <div className="result">
            <p>Force: {casimirResult.force_newtons.toExponential(4)} N</p>
            <p>State: <code>{casimirResult.state}</code></p>
            <p className="note">⚠️ {casimirResult.note}</p>
          </div>
        )}
      </div>

      <div className="calculation-box">
        <h4>Radiation Momentum Calculator</h4>
        <label>
          Energy (J):
          <input type="number" value={radiationEnergy} onChange={(e) => setRadiationEnergy(parseFloat(e.target.value))} />
        </label>
        <button onClick={handleRadiationCalc}>Calculate</button>
        {radiationResult && (
          <div className="result">
            <p>Momentum: {radiationResult.momentum_kg_m_s.toExponential(4)} kg·m/s</p>
            <p>State: <code>{radiationResult.state}</code></p>
            <p className="note">⚠️ {radiationResult.note}</p>
          </div>
        )}
      </div>
    </div>
  )
}
