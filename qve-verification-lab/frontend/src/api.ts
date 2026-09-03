import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export const datasetService = {
  importDataset: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/datasets/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getDataset: async (datasetId: string) => {
    const response = await api.get(`/api/datasets/${datasetId}`)
    return response.data
  },

  runQC: async (datasetId: string) => {
    const response = await api.post(`/api/qc/${datasetId}`)
    return response.data
  },
}

export const claimService = {
  createClaim: async (title: string, description: string) => {
    const response = await api.post('/api/claims', {
      title,
      description,
      supporting_data: {},
    })
    return response.data
  },

  getClaim: async (claimId: string) => {
    const response = await api.get(`/api/claims/${claimId}`)
    return response.data
  },
}

export const physicsService = {
  calculateCasimir: async (area: number, gap: number) => {
    const response = await api.post('/api/physics/casimir', null, {
      params: { area_m2: area, gap_nm: gap },
    })
    return response.data
  },

  calculateRadiation: async (energy: number) => {
    const response = await api.post('/api/physics/radiation', null, {
      params: { energy_joules: energy },
    })
    return response.data
  },
}

export const evidenceService = {
  evaluateGate: async (gate: string, evidenceData: Record<string, any>) => {
    const response = await api.post(`/api/evidence/gate/${gate}`, evidenceData)
    return response.data
  },
}

export default api
