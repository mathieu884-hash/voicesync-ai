import pino from 'pino'

const logger = pino()

export interface PerformanceMetrics {
  endpoint: string
  method: string
  statusCode: number
  duration: number
  timestamp: Date
}

export const trackPerformance = async (metrics: PerformanceMetrics) => {
  logger.info({
    event: 'performance_metrics',
    ...metrics,
  })
}

export interface ErrorMetrics {
  endpoint: string
  error: string
  statusCode: number
  userId?: number
  timestamp: Date
}

export const trackError = async (metrics: ErrorMetrics) => {
  logger.error({
    event: 'error_metrics',
    ...metrics,
  })
}

export interface UserMetrics {
  userId: number
  action: string
  metadata?: Record<string, unknown>
  timestamp: Date
}

export const trackUser = async (metrics: UserMetrics) => {
  logger.info({
    event: 'user_metrics',
    ...metrics,
  })
}
