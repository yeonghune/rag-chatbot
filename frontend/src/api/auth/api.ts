import { getClient } from '../client';
import type { AuthTokens } from '../interceptors';
import type {
  SignInRequest,
  SignInResponse,
  TokenResponse,
  User,
} from './types';

export const signIn = async (payload: SignInRequest) => {
  const client = getClient();
  const form = new URLSearchParams();
  form.append('username', payload.username);
  form.append('password', payload.password);

  const { data } = await client.post<SignInResponse>('/auth/token', form, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Skip-Auth-Interceptor': 'true',
    },
  });
  return data;
};

export const refreshToken = async () => {
  const client = getClient();
  const { data } = await client.post<TokenResponse>('/auth/refresh',
    {
      headers: {
        'X-Skip-Auth-Interceptor': 'true'
      }
    }
  );
  return data;
};

export const signOut = async () => {
  const client = getClient();
  await client.post('/auth/logout');
};

export const getCurrentUser = async () => {
  const client = getClient();
  const { data } = await client.get<User>('/auth/me');
  return data;
};

export const mapTokenResponse = (token: TokenResponse): AuthTokens => ({
  accessToken: token.access_token,
  tokenType: token.token_type,
  user: token.user,
});
