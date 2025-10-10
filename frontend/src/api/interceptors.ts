import { AxiosHeaders } from 'axios';
import type { AxiosError, AxiosInstance } from 'axios';
import type { User } from './auth/types';

export interface AuthTokens {
  accessToken: string;
  tokenType?: string;
  user?: User;
}

export interface TokenStore {
  getAccessToken: () => string | null;
  setTokens?: (tokens: AuthTokens) => void;
  clearTokens?: () => void;
}

export interface AttachAuthInterceptorOptions {
  tokenStore: TokenStore;
  refreshTokens?: () => Promise<AuthTokens>;
  onUnauthorized?: () => void;
}

type RetryableRequestConfig = {
  _retry?: boolean;
};

export const attachAuthInterceptors = (
  client: AxiosInstance,
  { tokenStore, refreshTokens, onUnauthorized }: AttachAuthInterceptorOptions,
) => {
  client.interceptors.request.use((config) => {
    const token = tokenStore.getAccessToken();

    if (token) {
      const headers = AxiosHeaders.from(config.headers ?? {});
      headers.set('Authorization', `Bearer ${token}`);
      config.headers = headers;
    }

    return config;
  });

  client.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const status = error.response?.status;
      const originalRequest = error.config as (AxiosError['config'] &
        RetryableRequestConfig) | undefined;

      if (status !== 401 || !originalRequest || originalRequest._retry) {
        return Promise.reject(error);
      }

      if (!refreshTokens) {
        tokenStore.clearTokens?.();
        onUnauthorized?.();
        return Promise.reject(error);
      }

      originalRequest._retry = true;

      try {
        const tokens = await refreshTokens();

        tokenStore.setTokens?.(tokens);

        if (tokens.accessToken) {
          const headers = AxiosHeaders.from(originalRequest.headers ?? {});
          headers.set('Authorization', `Bearer ${tokens.accessToken}`);
          originalRequest.headers = headers;
        }

        return client(originalRequest);
      } catch (refreshError) {
        tokenStore.clearTokens?.();
        onUnauthorized?.();
        return Promise.reject(refreshError);
      }
    },
  );
};
