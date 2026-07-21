import { create } from 'zustand'
import api from '../services/api'

interface Job {
  id: number
  title: string
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled'
  progress: number
  source_language: string
  target_language: string
  created_at: string
  estimated_duration: number
  segments?: Record<string, unknown>[]
}

interface JobsState {
  jobs: Job[]
  isLoading: boolean
  error: string | null
  currentJob: Job | null
  fetchJobs: (skip?: number, limit?: number, status?: string) => Promise<void>
  fetchJobDetail: (jobId: number) => Promise<void>
  createJob: (formData: FormData) => Promise<Job>
  cancelJob: (jobId: number) => Promise<void>
  downloadJob: (jobId: number) => Promise<void>
}

export const useJobsStore = create<JobsState>((set) => ({
  jobs: [],
  isLoading: false,
  error: null,
  currentJob: null,

  fetchJobs: async (skip = 0, limit = 10, status?: string) => {
    set({ isLoading: true, error: null })
    try {
      const { data } = await api.getJobs(skip, limit, status)
      set({ jobs: Array.isArray(data) ? data : data.items || [] })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to fetch jobs' })
    } finally {
      set({ isLoading: false })
    }
  },

  fetchJobDetail: async (jobId: number) => {
    set({ isLoading: true, error: null })
    try {
      const { data } = await api.getJobDetail(jobId)
      set({ currentJob: data })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to fetch job' })
    } finally {
      set({ isLoading: false })
    }
  },

  createJob: async (formData: FormData) => {
    set({ isLoading: true, error: null })
    try {
      const { data } = await api.createDubbingJob(formData)
      return data
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to create job' })
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  cancelJob: async (jobId: number) => {
    try {
      await api.cancelJob(jobId)
      set((state) => ({
        jobs: state.jobs.map((job) =>
          job.id === jobId ? { ...job, status: 'cancelled' as const } : job
        ),
      }))
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to cancel job' })
      throw error
    }
  },

  downloadJob: async (jobId: number) => {
    try {
      const response = await api.downloadJob(jobId)
      const blob = response.data as Blob
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `dubbed_video_${jobId}.mp4`
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to download job' })
      throw error
    }
  },
}))
