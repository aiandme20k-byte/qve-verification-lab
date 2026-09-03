import React, { useState, useEffect } from 'react'
import { claimService } from '../api'

export const ChatClaims: React.FC = () => {
  const [claimTitle, setClaimTitle] = useState('')
  const [claimDesc, setClaimDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [claims, setClaims] = useState<any[]>([])

  const handleCreateClaim = async () => {
    if (!claimTitle || !claimDesc) return
    setLoading(true)
    try {
      const result = await claimService.createClaim(claimTitle, claimDesc)
      setClaims([...claims, result])
      setClaimTitle('')
      setClaimDesc('')
    } catch (err) {
      console.error('Claim creation failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-claims">
      <h3>Chat → Claims</h3>
      <div className="claim-form">
        <input
          type="text"
          placeholder="Claim title"
          value={claimTitle}
          onChange={(e) => setClaimTitle(e.target.value)}
        />
        <textarea
          placeholder="Description"
          value={claimDesc}
          onChange={(e) => setClaimDesc(e.target.value)}
        ></textarea>
        <button onClick={handleCreateClaim} disabled={loading}>
          {loading ? 'Creating...' : 'Create Claim'}
        </button>
      </div>
      <div className="claims-list">
        <h4>Claims</h4>
        {claims.map((claim) => (
          <div key={claim.id} className="claim-item">
            <h5>{claim.title}</h5>
            <p>{claim.description}</p>
            <p>State: <code>{claim.state}</code></p>
            <p>ID: <code>{claim.id.substring(0, 8)}...</code></p>
          </div>
        ))}
      </div>
    </div>
  )
}
