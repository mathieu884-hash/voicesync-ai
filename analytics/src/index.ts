import express, { Request, Response } from 'express'
import { register, Counter, Histogram, Gauge } from 'prom-client'
import pino from 'pino'
import pinoHttp from 'pino-http'
import cors from 'cors'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
const logger = pino()
const httpLogger = pinoHttp({ logger })

app.use(httpLogger)
app.use(cors())
app.use(express.json())

// Metrics
const jobsProcessed = new Counter({
  name: 'voicesync_jobs_processed_total',
  help: 'Total number of dubbing jobs processed',
  labelNames: ['status', 'language_pair'],
})

const jobDuration = new Histogram({
  name: 'voicesync_job_duration_seconds',
  help: 'Duration of dubbing jobs in seconds',
  labelNames: ['language_pair'],
  buckets: [10, 30, 60, 120, 300, 600],
})

const activeJobs = new Gauge({
  name: 'voicesync_active_jobs',
  help: 'Number of active dubbing jobs',
  labelNames: ['status'],
})

const apiLatency = new Histogram({
  name: 'voicesync_api_latency_ms',
  help: 'API request latency in milliseconds',
  labelNames: ['method', 'endpoint', 'status'],
  buckets: [10, 50, 100, 500, 1000, 5000],
})

const usersActive = new Gauge({
  name: 'voicesync_users_active',
  help: 'Number of active users',
})

const errorRate = new Counter({
  name: 'voicesync_errors_total',
  help: 'Total number of errors',
  labelNames: ['endpoint', 'error_type'],
})

// Routes
app.post('/api/analytics/job', (req: Request, res: Response) => {
  try {
    const { status, language_pair, duration } = req.body

    jobsProcessed.inc({ status, language_pair })
    jobDuration.observe({ language_pair }, duration)
    activeJobs.inc({ status })

    logger.info({
      event: 'job_processed',
      status,
      language_pair,
      duration,
    })

    res.json({ success: true })
  } catch (error) {
    logger.error(error)
    errorRate.inc({ endpoint: '/api/analytics/job', error_type: 'unknown' })
    res.status(500).json({ error: 'Failed to log job' })
  }
})

app.post('/api/analytics/event', (req: Request, res: Response) => {
  try {
    const { event_type, user_id, metadata } = req.body

    logger.info({
      event: event_type,
      user_id,
      metadata,
      timestamp: new Date().toISOString(),
    })

    res.json({ success: true })
  } catch (error) {
    logger.error(error)
    errorRate.inc({ endpoint: '/api/analytics/event', error_type: 'unknown' })
    res.status(500).json({ error: 'Failed to log event' })
  }
})

app.post('/api/analytics/error', (req: Request, res: Response) => {
  try {
    const { endpoint, error_type, message, stack_trace } = req.body

    errorRate.inc({ endpoint, error_type })

    logger.error({
      event: 'error_reported',
      endpoint,
      error_type,
      message,
      stack_trace,
      timestamp: new Date().toISOString(),
    })

    res.json({ success: true })
  } catch (error) {
    logger.error(error)
    res.status(500).json({ error: 'Failed to log error' })
  }
})

app.get('/api/analytics/stats', (req: Request, res: Response) => {
  try {
    res.json({
      metrics: {
        jobs_processed: jobsProcessed.get().values.length,
        active_jobs: activeJobs.get().values.length,
        total_errors: errorRate.get().values.length,
      },
      timestamp: new Date().toISOString(),
    })
  } catch (error) {
    logger.error(error)
    res.status(500).json({ error: 'Failed to get stats' })
  }
})

app.get('/metrics', async (req: Request, res: Response) => {
  try {
    res.set('Content-Type', register.contentType)
    res.end(await register.metrics())
  } catch (error) {
    logger.error(error)
    res.status(500).end(error)
  }
})

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() })
})

const PORT = process.env.PORT || 9090
app.listen(PORT, () => {
  logger.info(`Analytics service running on port ${PORT}`)
  logger.info(`Metrics available at http://localhost:${PORT}/metrics`)
})

export default app
