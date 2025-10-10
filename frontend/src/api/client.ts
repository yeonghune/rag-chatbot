import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig } from 'axios';

export interface CreateClientOptions extends AxiosRequestConfig {}

let client: AxiosInstance | null = null;

const defaultConfig: AxiosRequestConfig = {
  baseURL: '/api',
  timeout: 10_000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const createClient = (
  config: CreateClientOptions = {},
): AxiosInstance => {
  if (!client) {
    client = axios.create({
      ...defaultConfig,
      ...config,
      headers: {
        ...defaultConfig.headers,
        ...config.headers,
      },
    });
  }

  return client;
};

export const getClient = (): AxiosInstance => {
  if (!client) {
    client = createClient();
  }

  return client;
};
