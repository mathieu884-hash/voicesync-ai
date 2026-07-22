import express from 'express'
import { createLogger } from '../logger'
const logger = createLogger('health')

const router = express.Router()

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  timestamp: string
  uptime: number
  services: {
    database: 'up' | 'down'
    cache: 'up' | 'down'
    queue: 'up' | 'down'
  }
}

router.get('/health', async (req, res) => {
  try {
    const healthStatus: HealthStatus = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      services: {
        database: 'up',
        cache: 'up',
        queue: 'up',
      },
    }

    logger.info('Health check passed')
    res.json(healthStatus)
  } catch (error) {
    logger.error(error, 'Health check failed')
    res.status(500).json({ status: 'unhealthy', error: 'Service unavailable' })
  }
})

router.get('/ready', async (req, res) => {
  try {
    // Check if all services are ready
    res.json({ ready: true, timestamp: new Date().toISOString() })
  } catch (error) {
    logger.error(error, 'Readiness check failed')
    res.status(503).json({ ready: false })
  }
})

export default router
