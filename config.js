/**
 * EduTrack Global Client Configuration
 * Configure your live backend API URL below:
 */
(function() {
  const isLocal = window.location.hostname === 'localhost' || 
                  window.location.hostname === '127.0.0.1' || 
                  window.location.protocol === 'file:';

  // Support dynamic runtime API parameter: ?api=https://your-service.onrender.com
  let runtimeApi = null;
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const paramApi = urlParams.get('api');
    if (paramApi) {
      localStorage.setItem('edutrack_api_url', paramApi);
      runtimeApi = paramApi;
    } else {
      runtimeApi = localStorage.getItem('edutrack_api_url');
    }
  } catch (_) {}

  // Set default production backend URL here (e.g. Render/Railway):
  const PRODUCTION_BACKEND_URL = runtimeApi || '';

  window.EDUTRACK_API_URL = isLocal 
    ? (runtimeApi || 'http://localhost:5000') 
    : (PRODUCTION_BACKEND_URL || '');

  // DeepL Translation API Integration (Free Tier)
  window.DEEPL_API_KEY = '84c3da37-9f70-4cc9-9187-8149259640d2:fx';
  window.DEEPL_API_URL = 'https://api-free.deepl.com/v2/translate';
})();
