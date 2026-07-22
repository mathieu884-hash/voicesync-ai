# VoiceSync AI - Analytics & Monitoring

## Real-time Analytics Service

### Features

✅ Prometheus Metrics  
✅ Structured Logging with Pino  
✅ Performance Tracking  
✅ Error Tracking  
✅ User Event Logging  
✅ Health Checks  
✅ REST API  

### Quick Start

```bash
cd analytics
npm install
npm run dev
```

**Access:**
- Metrics: http://localhost:9090/metrics
- Health: http://localhost:9090/health
- Stats: http://localhost:9090/api/analytics/stats

### API Endpoints

#### Log Job Completion
```bash
POST /api/analytics/job
{
  "status": "completed",
  "language_pair": "en_fr",
  "duration": 45
}
```

#### Log User Event
```bash
POST /api/analytics/event
{
  "event_type": "login",
  "user_id": 123,
  "metadata": { "source": "mobile" }
}
```

#### Log Error
```bash
POST /api/analytics/error
{
  "endpoint": "/api/jobs",
  "error_type": "validation_error",
  "message": "Invalid job parameters"
}
```

#### Get Statistics
```bash
GET /api/analytics/stats
```

### Metrics Collected

**Job Metrics:**
- `voicesync_jobs_processed_total` - Total jobs processed
- `voicesync_job_duration_seconds` - Job processing duration
- `voicesync_active_jobs` - Currently active jobs

**API Metrics:**
- `voicesync_api_latency_ms` - Request latency
- `voicesync_users_active` - Active users count

**Error Metrics:**
- `voicesync_errors_total` - Total errors

### Integration

In your FastAPI backend:

```python
from analytics.client import analyticsClient

await analyticsClient.logJobCompletion(
    job_id=123,
    status='completed',
    duration=45,
    language_pair='en_fr'
)
```

### Docker

```bash
docker build -t voicesync-analytics .
docker run -p 9090:9090 voicesync-analytics
```

### Environment Variables

```env
PORT=9090
LOG_LEVEL=info
ANALYTICS_URL=http://localhost:9090
```
