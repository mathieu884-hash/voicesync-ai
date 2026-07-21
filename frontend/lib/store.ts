import { create } from 'zustand';

interface AuthState {
  token: string | null;
  user: any | null;
  isAuthenticated: boolean;
  setToken: (token: string) => void;
  setUser: (user: any) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  isAuthenticated: false,
  setToken: (token) => set({ token, isAuthenticated: !!token }),
  setUser: (user) => set({ user }),
  logout: () => set({ token: null, user: null, isAuthenticated: false }),
}));

interface DubbingState {
  currentJob: any | null;
  jobs: any[];
  setCurrentJob: (job: any) => void;
  addJob: (job: any) => void;
  updateJob: (jobId: string, updates: any) => void;
}

export const useDubbingStore = create<DubbingState>((set) => ({
  currentJob: null,
  jobs: [],
  setCurrentJob: (job) => set({ currentJob: job }),
  addJob: (job) => set((state) => ({ jobs: [...state.jobs, job] })),
  updateJob: (jobId, updates) =>
    set((state) => ({
      jobs: state.jobs.map((job) => (job.id === jobId ? { ...job, ...updates } : job)),
    })),
}));
