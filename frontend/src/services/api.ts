import axios from 'axios'

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  process.env.REACT_APP_API_URL ||
  'http://localhost:8000/api/v1'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

const api = {
  register: (data: { email: string; username: string; full_name: string; password: string }) =>
    client.post('/auth/register', data),
  login: (data: { email: string; password: string }) => client.post('/auth/login', data),
  getProfile: () => client.get('/auth/me'),
  changePassword: (data: { old_password: string; new_password: string }) =>
    client.post('/auth/change-password', data),
  createDubbingJob: (formData: FormData) =>
    client.post('/dubbing/create', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getJobs: (skip = 0, limit = 10, status?: string) => {
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
    if (status) params.append('status', status)
    return client.get(`/jobs?${params}`)
  },
  getJobDetail: (jobId: number) => client.get(`/jobs/${jobId}`),
  cancelJob: (jobId: number) => client.post(`/dubbing/cancel/${jobId}`),
  downloadJob: (jobId: number) =>
    client.get(`/jobs/${jobId}/download`, { responseType: 'blob' }),
  getVoices: (language?: string, gender?: string, skip = 0, limit = 50) => {
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
    if (language) params.append('language', language)
    if (gender) params.append('gender', gender)
    return client.get(`/voices?${params}`)
  },
  cloneVoice: (formData: FormData) =>
    client.post('/voices/clone', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getUserVoices: (skip = 0, limit = 10) => {
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
    return client.get(`/voices/user?${params}`)
  },
}

export default api
