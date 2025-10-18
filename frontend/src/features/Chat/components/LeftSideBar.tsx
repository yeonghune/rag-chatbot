import { useState } from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Tooltip from '@mui/material/Tooltip';
import Avatar from '@mui/material/Avatar';
import MenuRoundedIcon from '@mui/icons-material/MenuRounded';
import ChevronLeftRoundedIcon from '@mui/icons-material/ChevronLeftRounded';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import type { ChatResponse } from '@src/api/chat/types';

const SIDEBAR_WIDTH = 288;
const SIDEBAR_COLLAPSED_WIDTH = 64;

interface LeftSideBarProps {
  activeChatId: string;
  setActiveChatId: (id: string) => void;
  userName: string;
  chats: ChatResponse[];
}

export default function LeftSideBar({
  activeChatId,
  setActiveChatId,
  userName,
  chats,
}: LeftSideBarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleToggleSidebar = () => setIsCollapsed((prev) => !prev);

  const renderChat = (chat: ChatResponse) => {
    const isActive = chat.chatId === activeChatId;

    return (
      <ListItemButton
        key={chat.chatId}
        selected={isActive}
        onClick={() => setActiveChatId(chat.chatId)}
        sx={{
          mx: 1,
          mb: 0.5,
          borderRadius: 1.5,
          px: 2,
          py: 1.1,
          justifyContent: 'flex-start',
          textAlign: 'left',
        }}
      >
        <ListItemText
          primary={chat.title}
          secondary={new Date(chat.updatedAt).toLocaleString()}
          sx={{ whiteSpace: 'nowrap' }}
        />
      </ListItemButton>
    );
  };

  return (
    <Box
      component="aside"
      sx={{
        bgcolor: 'grey.50',
        display: 'flex',
        flexDirection: 'column',
        width: isCollapsed ? SIDEBAR_COLLAPSED_WIDTH : SIDEBAR_WIDTH,
        transition: 'width 0.2s ease',
        borderRight: (theme) => `1px solid ${theme.palette.divider}`,
        py: 1.5,
      }}
    >
      <Stack
        direction="row"
        justifyContent="flex-start"
        alignItems="center"
        spacing={12}
        sx={{ px: isCollapsed ? 1 : 2.5, pb: 1.5 }}
      >
        {!isCollapsed && (
          <Typography variant="subtitle1" sx={{ whiteSpace: 'nowrap', fontWeight: 600 }}>
            Rag Chatbot
          </Typography>
        )}
        <IconButton onClick={handleToggleSidebar}>
          {isCollapsed ? <MenuRoundedIcon /> : <ChevronLeftRoundedIcon />}
        </IconButton>
      </Stack>

      <Divider />

      <Box sx={{ px: isCollapsed ? 1 : 2, py: 1.5 }}>
        {isCollapsed ? (
          <Tooltip title="New Chat" placement="right">
            <IconButton>
              <AddRoundedIcon />
            </IconButton>
          </Tooltip>
        ) : (
          <Button
            fullWidth
            startIcon={<AddRoundedIcon />}
            variant="contained"
            sx={{ overflow: 'hidden', borderRadius: 2, fontWeight: 600, textTransform: 'none' }}
          >
            New Chat
          </Button>
        )}
      </Box>

      <Divider />

      {!isCollapsed && (
        <List disablePadding sx={{ overflowY: 'auto', overflowX: 'hidden' }}>
          {chats.map((chat) => renderChat(chat))}
        </List>
      )}

      <Divider />

      <Stack
        direction="row"
        alignItems="center"
        spacing={1.5}
        sx={{ px: isCollapsed ? 1.5 : 2, pt: 2, pb: 0.5, mt: 'auto' }}
      >
        <Avatar sx={{ width: 36, height: 36 }} />
        {!isCollapsed && (
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="body2" sx={{ whiteSpace: 'nowrap', fontWeight: 600 }}>
              {userName}
            </Typography>
          </Box>
        )}
      </Stack>
    </Box>
  );
}
