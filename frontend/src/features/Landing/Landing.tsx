import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { getCurrentUser, signOut } from '../../api/auth/api';
import { tokenStore } from '../../api/tokenStore';

const Landing = () => {
  const navigate = useNavigate();
  const cachedUserName = React.useMemo(
    () => tokenStore.getTokens()?.user?.name ?? '',
    [],
  );
  const [status, setStatus] = React.useState<'loading' | 'ready' | 'error'>(
    cachedUserName ? 'ready' : 'loading',
  );
  const [userName, setUserName] = React.useState<string>(cachedUserName);
  const [message, setMessage] = React.useState<string>('');

  React.useEffect(() => {
    let mounted = true;

    const run = async () => {
      setStatus('loading');
      setMessage('');

      try {
        const user = await getCurrentUser();
        if (!mounted) {
          return;
        }
        setUserName(user.name);
        setStatus('ready');
      } catch (error) {
        if (!mounted) {
          return;
        }
        setStatus('error');
        setMessage('세션이 만료되었어요. 다시 로그인해주세요.');
        tokenStore.clearTokens();
        navigate('/auth', { replace: true });
      }
    };

    run();

    return () => {
      mounted = false;
    };
  }, [navigate]);

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch {
      // ignore logout failures
    } finally {
      tokenStore.clearTokens();
      navigate('/auth', { replace: true });
    }
  };

  if (status === 'loading') {
    return (
      <Box
        sx={{
          display: 'grid',
          placeItems: 'center',
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #f4f6fc, #dfe9f3)',
        }}
      >
        <Stack spacing={2} alignItems="center">
          <CircularProgress />
          <Typography variant="body2" color="text.secondary">
            인증 상태를 확인하고 있어요...
          </Typography>
        </Stack>
      </Box>
    );
  }

  if (status === 'error') {
    return (
      <Box
        sx={{
          display: 'grid',
          placeItems: 'center',
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #f4f6fc, #dfe9f3)',
        }}
      >
        <Alert severity="error">{message}</Alert>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #f4f6fc, #dfe9f3)',
        padding: 3,
      }}
    >
      <Paper
        elevation={0}
        sx={{
          maxWidth: 560,
          width: '100%',
          padding: 6,
          borderRadius: 4,
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
          textAlign: 'center',
          backgroundColor: 'rgba(255,255,255,0.85)',
          backdropFilter: 'blur(8px)',
        }}
      >
        <Stack spacing={1.5}>
          <Typography variant="overline" letterSpacing={6} color="text.secondary">
            RAG CHATBOT PLATFORM
          </Typography>
          <Typography variant="h3" fontWeight={800}>
            안녕하세요, {userName}님!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            지식 베이스를 연결하고, 프롬프트를 실험하고, 팀이 신뢰할 수 있는 답변을 전달해요. 안전하게, 재현 가능하게, 그리고 즐겁게.
          </Typography>
        </Stack>

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center">
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/playground')}
            sx={{ minWidth: 160, borderRadius: 999 }}
          >
            PlayGround 열기
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={handleSignOut}
            sx={{ minWidth: 160, borderRadius: 999 }}
          >
            로그아웃
          </Button>
        </Stack>

        <Typography variant="caption" color="text.secondary">
          Retrieval-Augmented Generation을 탐구하는 팀을 위해 준비했어요.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Landing;
