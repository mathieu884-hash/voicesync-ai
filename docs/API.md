# API Documentation

## Overview

La VoiceSync AI API est une API REST complète pour le dubbing vidéo automatisé avec IA.

## Base URL

```
https://api.voicesync-ai.com/api/v1
```

## Authentication

Tous les endpoints (sauf `/auth/register` et `/auth/login`) nécessitent un token JWT:

```http
Authorization: Bearer {access_token}
```

## Error Responses

Tous les erreurs sont retournées au format JSON:

```json
{
  "detail": "Error message",
  "status": "error",
  "error_code": "ERROR_CODE"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_CREDENTIALS | 401 | Email ou password invalide |
| TOKEN_EXPIRED | 401 | Token JWT expiré |
| UNAUTHORIZED | 403 | Accès non autorisé |
| NOT_FOUND | 404 | Ressource non trouvée |
| VALIDATION_ERROR | 422 | Erreur de validation |
| SERVER_ERROR | 500 | Erreur serveur |

## Rate Limiting

Les requêtes sont limitées à:
- 1000 requêtes par heure pour les utilisateurs gratuits
- Illimité pour les utilisateurs premium

## Webhooks

Les événements suivants peuvent être envoyés via webhooks:

- `job.created` - Job créé
- `job.processing` - Job en cours de traitement
- `job.completed` - Job complété
- `job.failed` - Job échoué

## Pagination

Les listes utilisent la pagination:

```http
GET /jobs?skip=0&limit=10&sort=-created_at
```

Returns:
```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```
