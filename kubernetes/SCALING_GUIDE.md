# VoiceSync AI - Scaling & Load Balancing Guide

## Architecture Overview

```
┌─────────────────────────────────────┐
│   Client Applications                │
│   (Web, Mobile, Desktop)            │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Load Balancer │
        │  (Nginx/Traefik│
        └────────┬───────┘
                 │
      ┌──────────┼──────────┐
      │          │          │
      ▼          ▼          ▼
   ┌────┐    ┌────┐    ┌────┐
   │API1│    │API2│    │API3│
   └─┬──┘    └─┬──┘    └─┬──┘
     │         │         │
     └─────────┬─────────┘
               ▼
      ┌──────────────────┐
      │   Database       │
      │  (PostgreSQL)    │
      │  with Replication│
      └──────────────────┘
```

## 1. Kubernetes Deployment

### Setup

```bash
cd kubernetes
bash setup.sh
```

### Key Components

**StatefulSet: PostgreSQL**
- Single master with persistent storage
- 10Gi storage
- Liveness and readiness probes

**Deployment: API (3 replicas)**
- Anti-affinity rules (spread across nodes)
- Rolling update strategy
- Resource requests/limits
- Health checks

**Deployment: Analytics (2 replicas)**
- Horizontal scaling
- Resource limits

**Deployment: Nginx Load Balancer**
- 2 replicas
- Least connections algorithm
- Connection pooling

### Horizontal Pod Autoscaler (HPA)

```yaml
metrics:
- CPU: 70% threshold
- Memory: 80% threshold

Scaling:
- Min: 3 replicas
- Max: 10 replicas
- Scale-up: 100% increase per 30s
- Scale-down: 50% decrease per 60s
```

## 2. Load Balancing Strategies

### Nginx Configuration

**Algorithms:**
- `least_conn` - Least connections
- `round_robin` - Default
- `ip_hash` - Session persistence

**Connection Pooling:**
```nginx
upstream voicesync_api {
    keepalive 32;
    server api1:8000;
    server api2:8000;
    server api3:8000;
}
```

**Health Checks:**
```nginx
server api1:8000 max_fails=3 fail_timeout=30s;
```

## 3. Caching Strategy

### Nginx Cache

```nginx
proxy_cache_path /var/cache/nginx \
  levels=1:2 \
  keys_zone=voicesync_cache:10m \
  max_size=1g \
  inactive=60m;
```

**Cache Rules:**
- GET `/api/voices` - 10m
- GET `/api/jobs/id` - 10m
- POST endpoints - No cache

### Redis Cache (Backend)

- Session data: 1 hour TTL
- User preferences: 24 hour TTL
- Job status: 5 minute TTL

## 4. Database Scaling

### PostgreSQL Configuration

**Connection Pooling (PgBouncer):**
```
max_db_connections = 100
default_pool_size = 25
min_pool_size = 10
reserve_pool_size = 5
```

**Replication:**
- Primary: Single write
- Replicas: Read-only (future)

**Optimization:**
- Indexes on frequently queried columns
- Partitioning for large tables
- Vacuum and analyze scheduled

## 5. Rate Limiting

```nginx
# General: 10 requests/second
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;

# API: 100 requests/second
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;

# Login: 5 requests/minute
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
```

## 6. Monitoring & Metrics

**Key Metrics:**
- Pod CPU/Memory usage
- Request latency
- Upstream response times
- Cache hit ratio
- Active connections

**Kubectl Commands:**

```bash
# View HPA status
kubectl get hpa -n voicesync

# View metrics
kubectl top pods -n voicesync

# Watch scaling
kubectl get pods -n voicesync -w

# View logs
kubectl logs -f deployment/api -n voicesync
```

## 7. Performance Optimization

### Nginx Tuning

```nginx
# Worker processes
worker_processes auto;

# Max connections per worker
worker_connections 4096;

# HTTP keepalive
keepalive_timeout 65;

# Gzip compression
gzip on;
gzip_comp_level 6;
```

### Application Tuning

- Connection pooling
- Async processing
- Database query optimization
- Caching strategies

## 8. Deployment Checklist

- [ ] Kubernetes cluster created
- [ ] Storage classes configured
- [ ] ConfigMaps and Secrets created
- [ ] Docker images built and pushed
- [ ] Deployments applied
- [ ] HPA configured
- [ ] Ingress rules set
- [ ] Monitoring enabled
- [ ] Load testing performed
- [ ] Alerts configured

## 9. Scaling to Production

### Phase 1: Initial (10-50 users)
- 3 API replicas
- 1 database instance
- 1 cache instance
- Estimated cost: ~$500/month

### Phase 2: Growth (50-500 users)
- 5-10 API replicas (with HPA)
- 1 primary + 1 replica database
- Redis Cluster (3 nodes)
- Estimated cost: ~$2000/month

### Phase 3: Scale (500+ users)
- Auto-scaling (10-50 replicas)
- Database sharding
- CDN for static content
- Multi-region deployment
- Estimated cost: ~$5000+/month

## 10. Troubleshooting

```bash
# Check pod status
kubectl describe pod <pod-name> -n voicesync

# Check HPA decisions
kubectl describe hpa api-hpa -n voicesync

# Check events
kubectl get events -n voicesync --sort-by='.lastTimestamp'

# Debug pod
kubectl exec -it <pod-name> -n voicesync -- /bin/bash
```
