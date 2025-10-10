import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { StyledEngineProvider } from '@mui/material/styles';
import App from './App.tsx';
import { createClient } from './api/client';
import { attachAuthInterceptors } from './api/interceptors';
import { tokenStore } from './api/tokenStore';
import { mapTokenResponse, refreshToken } from './api/auth/api';

const client = createClient();

attachAuthInterceptors(client, {
  tokenStore,
  refreshTokens: async () => {
    const refreshed = await refreshToken();
    return mapTokenResponse(refreshed);
  },
  onUnauthorized: () => {
    tokenStore.clearTokens();
    if (window.location.pathname !== '/auth') {
      window.location.replace('/auth');
    }
  },
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <StyledEngineProvider injectFirst>
      <App />
    </StyledEngineProvider>
  </StrictMode>,
);
