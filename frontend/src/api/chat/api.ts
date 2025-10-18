import { client } from '@src/main';
import type { ChatResponse } from './types';

export const getChatList = async (): Promise<ChatResponse[]> => {
  const response = await client.get<ChatResponse[]>('/chats/');
  return response.data;
};
