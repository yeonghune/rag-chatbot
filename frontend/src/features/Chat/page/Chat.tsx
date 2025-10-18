import { useEffect, useState } from 'react';
import AppTheme from '@theme/Apptheme';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import LeftSideBar from '../components/LeftSideBar';
import ChatContent from '../components/ChatContent';
import { useAppContext } from '@src/shared/contexts/AppContext';
import { getChatList } from '@src/api/chat/api';
import type { ChatResponse } from '@src/api/chat/types';

export default function Chat(props: { disableCustomTheme?: boolean }) {
  const { name } = useAppContext();
  const [activeChatId, setActiveChatId] = useState<string>('1');
  const [chats, setChats] = useState<ChatResponse[]>([]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const data = await getChatList();
        setChats(data);
        console.log(data);
      } catch (error) {
        console.error('Failed to load chats', error);
      }
    };

    fetchChats();
  }, []);

  const handleSubmitMessage = (message: string) => {
    // TODO: integrate with chat backend
    console.log(`Send message to chat ${activeChatId}: ${message}`);
  };

  return (
    <AppTheme {...props}>
      <CssBaseline enableColorScheme />
      <Box
        sx={(theme) => ({
          display: 'flex',
          height: '100vh',
          bgcolor:
            theme.palette.mode === 'dark'
              ? '#0d0d0d'
              : theme.palette.background.default,
        })}
      >
        <LeftSideBar
          activeChatId={activeChatId}
          setActiveChatId={setActiveChatId}
          userName={name}
          chats={chats}
        />

        <Box
          component="main"
          sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}
        >
          <ChatContent userName={name} onSubmit={handleSubmitMessage} />
        </Box>
      </Box>
    </AppTheme>
  );
}
