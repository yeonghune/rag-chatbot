import type { AuthTokens } from './interceptors';

const STORAGE_KEY = 'rag-auth-tokens';

let cachedTokens: AuthTokens | null = null;

const readFromSession = (): AuthTokens | null => {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const raw = window.sessionStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }

    const parsed = JSON.parse(raw) as AuthTokens;

    if (parsed && typeof parsed.accessToken === 'string') {
      return parsed;
    }
  } catch {
    // ignore corrupted storage
  }

  return null;
};

const writeToSession = (tokens: AuthTokens | null) => {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    if (!tokens) {
      window.sessionStorage.removeItem(STORAGE_KEY);
      return;
    }

    window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(tokens));
  } catch {
    // ignore storage errors (e.g., quota exceeded, private mode)
  }
};

export const tokenStore = {
  getTokens(): AuthTokens | null {
    if (cachedTokens) {
      return cachedTokens;
    }

    cachedTokens = readFromSession();
    return cachedTokens;
  },
  getAccessToken(): string | null {
    return this.getTokens()?.accessToken ?? null;
  },
  setTokens(tokens: AuthTokens) {
    cachedTokens = tokens;
    writeToSession(tokens);
  },
  clearTokens() {
    cachedTokens = null;
    writeToSession(null);
  },
};

export type TokenStore = typeof tokenStore;
