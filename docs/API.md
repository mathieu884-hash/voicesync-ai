# VoiceSync AI - API Documentation

## Overview

The VoiceSync AI API is a RESTful API that provides endpoints for video dubbing, voice synthesis, and job management.

**Base URL:** `http://localhost:8000/api/v1`

**Interactive Docs:** http://localhost:8000/docs (Swagger UI)

## Authentication

All API endpoints (except `/auth/login` and `/auth/register`) require Bearer token authentication.

### Headers

```bash
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Get Access Token

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

## Endpoints

### Authentication

#### Register

```bash
POST /api/v1/auth/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

#### Login

```bash
POST /api/v1/auth/login
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Dubbing

#### Create Dubbing Job

```bash
POST /api/v1/dubbing/create
Content-Type: multipart/form-data
```

**Parameters:**

- `video` (file, required) - Video file to dub
- `source_language` (string, required) - Source language code (e.g., "en")
- `target_language` (string, required) - Target language code (e.g., "fr")
- `preserve_voice` (boolean, optional) - Keep original voice timbre (default: true)
- `sync_lips` (boolean, optional) - Enable lip sync (default: true)
- `quality` (string, optional) - Output quality: "720p", "1080p", "4K" (default: "1080p")

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/dubbing/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "video=@movie.mp4" \
  -F "source_language=en" \
  -F "target_language=fr" \
  -F "quality=1080p"
```

**Response:**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2024-01-15T10:30:00Z",
  "estimated_duration": 300
}
```

### Jobs

#### Get Job Status

```bash
GET /api/v1/jobs/{job_id}
```

**Response:**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "estimated_completion": "2024-01-15T11:30:00Z",
  "error_message": null
}
```

**Status Values:**
- `queued` - Job is waiting to be processed
- `processing` - Job is currently being processed
- `completed` - Job completed successfully
- `failed` - Job failed
- `cancelled` - Job was cancelled

#### List Jobs

```bash
GET /api/v1/jobs?status=processing&limit=10&offset=0
```

**Query Parameters:**
- `status` (string, optional) - Filter by status
- `limit` (integer, optional) - Number of results (1-100, default: 10)
- `offset` (integer, optional) - Pagination offset (default: 0)

**Response:**

```json
[
  {
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "progress": 100,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z",
    "estimated_completion": "2024-01-15T11:00:00Z"
  }
]
```

#### Download Result

```bash
GET /api/v1/jobs/{job_id}/download
```

Returns the processed video file.

#### Cancel Job

```bash
POST /api/v1/dubbing/cancel/{job_id}
```

**Response:**

```json
{
  "message": "Job 550e8400-e29b-41d4-a716-446655440000 cancelled",
  "status": "cancelled"
}
```

### Voices

#### List Available Voices

```bash
GET /api/v1/voices?language=en&gender=female
```

**Query Parameters:**
- `language` (string, optional) - Filter by language
- `gender` (string, optional) - Filter by gender ("male", "female", "neutral")

**Response:**

```json
[
  {
    "id": "voice_001",
    "name": "Sarah",
    "language": "en",
    "gender": "female",
    "accent": "American",
    "sample_url": "https://...",
    "preview_audio_url": "https://...",
    "quality": "high"
  }
]
```

#### Get Voice Details

```bash
GET /api/v1/voices/{voice_id}
```

#### Clone Voice

```bash
POST /api/v1/voices/clone
Content-Type: multipart/form-data
```

**Parameters:**
- `audio_file` (file, required) - Sample audio (15-30 seconds)
- `voice_name` (string, required) - Name for cloned voice

**Response:**

```json
{
  "voice_id": "voice_cloned_001",
  "name": "My Custom Voice",
  "status": "processing",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Error Responses

### Error Format

```json
{
  "detail": "Error description",
  "status": "error"
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |

### Example Errors

#### Invalid Token

```json
{
  "detail": "Invalid or expired token",
  "status": "error"
}
```

#### File Too Large

```json
{
  "detail": "File size exceeds maximum of 2GB",
  "status": "error"
}
```

#### Unsupported Format

```json
{
  "detail": "Video format not supported. Supported: mp4, mkv, avi, mov",
  "status": "error"
}
```

## Rate Limiting

API requests are rate limited to 100 requests per hour per user.

**Headers:**
- `X-RateLimit-Limit`: 100
- `X-RateLimit-Remaining`: 45
- `X-RateLimit-Reset`: 1705315200

## WebSocket (Real-time Updates)

Connect to receive real-time job progress updates:

```bash
ws://localhost:8000/ws?job_id=550e8400-e29b-41d4-a716-446655440000&token=YOUR_TOKEN
```

**Message Format:**

```json
{
  "type": "progress",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "progress": 75,
  "status": "processing",
  "message": "Synthesizing voice..."
}
```

## Code Examples

### Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your_access_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Create dubbing job
with open("movie.mp4", "rb") as f:
    files = {"video": f}
    data = {
        "source_language": "en",
        "target_language": "fr",
        "quality": "1080p"
    }
    response = requests.post(
        f"{BASE_URL}/dubbing/create",
        headers=headers,
        files=files,
        data=data
    )
    job_id = response.json()["job_id"]

# Get job status
response = requests.get(
    f"{BASE_URL}/jobs/{job_id}",
    headers=headers
)
print(response.json())
```

### JavaScript

```javascript
const BASE_URL = "http://localhost:8000/api/v1";
const token = "your_access_token";

const headers = {
  "Authorization": `Bearer ${token}`
};

// Create dubbing job
const formData = new FormData();
formData.append("video", videoFile);
formData.append("source_language", "en");
formData.append("target_language", "fr");

const response = await fetch(`${BASE_URL}/dubbing/create`, {
  method: "POST",
  headers,
  body: formData
});

const { job_id } = await response.json();
```

## Support

- 📖 [Full Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/mathieu884-hash/voicesync-ai/issues)
- 💬 [Discord Community](https://discord.gg/voicesync)
