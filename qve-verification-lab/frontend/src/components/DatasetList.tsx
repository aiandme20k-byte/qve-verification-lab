import React, { useEffect, useState } from 'react'
import { datasetService } from '../api'

interface DatasetListProps {
  datasets: any[]
}

export const DatasetList: React.FC<DatasetListProps> = ({ datasets }) => {
  const [qcResults, setQcResults] = useState<Record<string, any>>({})

  const handleRunQC = async (datasetId: string) => {
    try {
      const result = await datasetService.runQC(datasetId)
      setQcResults({ ...qcResults, [datasetId]: result })
    } catch (err) {
      console.error('QC failed:', err)
    }
  }

  return (
    <div className="dataset-list">
      <h3>Imported Datasets</h3>
      {datasets.length === 0 ? (
        <p>No datasets imported yet</p>
      ) : (
        <ul>
          {datasets.map((ds) => (
            <li key={ds.id} className="dataset-item">
              <div>
                <strong>{ds.filename}</strong>
                <p>State: <code>{ds.state}</code></p>
                <p>Rows: {ds.row_count}</p>
                <p>SHA-256: <code>{ds.sha256.substring(0, 16)}...</code></p>
                <p>Created: {new Date(ds.created_at).toLocaleString()}</p>
              </div>
              <button onClick={() => handleRunQC(ds.id)}>Run QC</button>
              {qcResults[ds.id] && (
                <div className="qc-results">
                  <h4>QC Results:</h4>
                  <pre>{JSON.stringify(qcResults[ds.id], null, 2)}</pre>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
