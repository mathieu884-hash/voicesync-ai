import axios from 'axios'
import pino from 'pino'

const logger = pino()

const ANALYTICS_URL = process.env.ANALYTICS_URL || 'http://localhost:9090'

export const analyticsClient = {
  // Log job completion
  logJobCompletion: async (jobId: number, status: string, duration: number, languagePair: string) => {
    try {
      await axios.post(`${ANALYTICS_URL}/api/analytics/job`, {
        job_id: jobId,
        status,
        duration,
        language_pair: languagePair,
        timestamp: new Date().toISOString(),
      })
    } catch (error) {
      logger.error({ error, jobId }, 'Failed to log job completion')
    }
  },

  // Log user events
  logUserEvent: async (userId: number, eventType: string, metadata?: Record<string, unknown>) => {
    try {
      await axios.post(`${ANALYTICS_URL}/api/analytics/event`, {
        user_id: userId,
        event_type: eventType,
        metadata,
        timestamp: new Date().toISOString(),
      })
    } catch (error) {
      logger.error({ error, userId }, 'Failed to log user event')
    }
  },

  // Log errors
  logError: async (endpoint: string, errorType: string, message: string, stackTrace?: string) => {
    try {
      await axios.post(`${ANALYTICS_URL}/api/analytics/error`, {
        endpoint,
        error_type: errorType,
        message,
        stack_trace: stackTrace,
        timestamp: new Date().toISOString(),
      })
    } catch (error) {
      logger.error({ error, endpoint }, 'Failed to log error')
    }
  },

  // Get analytics stats
  getStats: async () => {
    try {
      const response = await axios.get(`${ANALYTICS_URL}/api/analytics/stats`)
      return response.data
    } catch (error) {
      logger.error({ error }, 'Failed to get analytics stats')
      return null
    }
  },
}

export default analyticsClient
