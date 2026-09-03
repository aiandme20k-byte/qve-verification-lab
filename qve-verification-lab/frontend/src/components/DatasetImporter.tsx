import React, { useState } from 'react'
import { datasetService } from '../api'

interface ImporterProps {
  onSuccess: (data: any) => void
}

export const DatasetImporter: React.FC<ImporterProps> = ({ onSuccess }) => {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f && (f.name.endsWith('.csv') || f.name.endsWith('.json'))) {
      setFile(f)
      setError(null)
    } else {
      setError('Please select a CSV or JSON file')
      setFile(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    try {
      const result = await datasetService.importDataset(file)
      onSuccess(result)
      setFile(null)
    } catch (err) {
      setError((err as Error).message || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="importer-box">
      <h3>Import Dataset</h3>
      <input type="file" onChange={handleFileChange} accept=".csv,.json" />
      {file && <p>Selected: {file.name}</p>}
      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  )
}
