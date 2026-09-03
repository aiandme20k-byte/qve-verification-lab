import { create } from 'zustand'

export interface Dataset {
  id: string
  filename: string
  import_type: string
  sha256: string
  state: string
  row_count: number
  created_at: string
  metadata?: Record<string, any>
}

export interface QCResult {
  check_type: string
  status: string
  count: number
  details?: Record<string, any>
}

export interface Claim {
  id: string
  title: string
  description: string
  state: string
  supporting_data?: Record<string, any>
  created_at: string
}

interface AppStore {
  activeTab: string
  setActiveTab: (tab: string) => void
  datasets: Dataset[]
  addDataset: (dataset: Dataset) => void
  claims: Claim[]
  addClaim: (claim: Claim) => void
  language: 'en' | 'my'
  setLanguage: (lang: 'en' | 'my') => void
}

export const useStore = create<AppStore>((set) => ({
  activeTab: 'dashboard',
  setActiveTab: (tab) => set({ activeTab: tab }),
  datasets: [],
  addDataset: (dataset) => set((state) => ({ datasets: [...state.datasets, dataset] })),
  claims: [],
  addClaim: (claim) => set((state) => ({ claims: [...state.claims, claim] })),
  language: 'en',
  setLanguage: (lang) => set({ language: lang }),
}))
