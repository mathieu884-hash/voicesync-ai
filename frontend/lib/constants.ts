export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
export const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';

export const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'French' },
  { code: 'es', name: 'Spanish' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'ru', name: 'Russian' },
  { code: 'ja', name: 'Japanese' },
  { code: 'zh', name: 'Chinese' },
  { code: 'ko', name: 'Korean' },
  { code: 'ar', name: 'Arabic' },
  { code: 'hi', name: 'Hindi' },
];

export const VOICE_TYPES = ['original', 'male', 'female', 'custom'];

export const QUALITY_OPTIONS = ['720p', '1080p', '4K'];

export const PRICING_PLANS = [
  {
    id: 'basic',
    name: 'Basic',
    price: 9.99,
    minutes: 30,
    languages: 10,
    quality: '720p',
    features: ['doublage_standard', 'sous_titres'],
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 29.99,
    minutes: 150,
    languages: 30,
    quality: '1080p',
    features: ['doublage_premium', 'sync_labiale', 'api_access'],
  },
  {
    id: 'studio',
    name: 'Studio',
    price: 99.99,
    minutes: 600,
    languages: 50,
    quality: '4K',
    features: ['voix_personnalisees', 'batch_processing', 'priority_support'],
  },
];
