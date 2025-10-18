import { useState } from 'react';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import SendRoundedIcon from '@mui/icons-material/SendRounded';

interface ChatContentProps {
  userName?: string;
  onSubmit?: (message: string) => void;
}

export default function ChatContent({ userName = '영훈 이', onSubmit }: ChatContentProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (!message.trim()) return;
    onSubmit?.(message.trim());
    setMessage('');
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <Box
      sx={(theme) => ({
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        px: 3,
        py: { xs: 4, md: 8 },
        bgcolor: theme.palette.mode === 'dark' ? '#101010' : 'background.default',
      })}
    >
      <Stack spacing={2} alignItems="center" width="100%" maxWidth={720}>
        <Typography
          variant="h4"
          component="h1"
          sx={{
            fontWeight: 600,
            textAlign: 'center',
            color: (theme) => (theme.palette.mode === 'dark' ? theme.palette.grey[100] : theme.palette.text.primary),
          }}
        >
          {userName}님 안녕하세요!
        </Typography>

        <Paper
          elevation={6}
          sx={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            borderRadius: 3,
            px: { xs: 1.5, md: 2.5 },
            py: { xs: 1, md: 1.5 },
            bgcolor: (theme) => (theme.palette.mode === 'dark' ? '#161616' : '#ffffff'),
          }}
        >
          <TextField
            fullWidth
            placeholder="무엇이 궁금하신가요?"
            variant="standard"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={handleKeyDown}
            InputProps={{
              disableUnderline: true,
              sx: {
                fontSize: '1rem',
                color: (theme) =>
                  theme.palette.mode === 'dark' ? theme.palette.grey[100] : theme.palette.text.primary,
              },
            }}
          />
          <IconButton
            color="primary"
            onClick={handleSend}
            sx={{
              bgcolor: 'common.black',
              color: 'primary.contrastText',
              '&:hover': { bgcolor: 'primary.dark' },
            }}
          >
            <SendRoundedIcon />
          </IconButton>
        </Paper>
      </Stack>
    </Box>
  );
}
