import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import MuiCard from '@mui/material/Card';
import { styled } from '@mui/material/styles';
import AppTheme from '@theme/AppTheme';
import { mapTokenResponse, signIn } from '../../api/auth/api';
import { tokenStore } from '../../api/tokenStore';

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  margin: 'auto',
  [theme.breakpoints.up('sm')]: {
    maxWidth: '450px',
  },
  boxShadow:
    'hsla(220, 30%, 5%, 0.05) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.05) 0px 15px 35px -5px',
  ...theme.applyStyles('dark', {
    boxShadow:
      'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
  }),
}));

const SignInContainer = styled(Stack)(({ theme }) => ({
  height: 'calc((1 - var(--template-frame-height, 0)) * 100dvh)',
  minHeight: '100%',
  padding: theme.spacing(2),
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(4),
  },
  '&::before': {
    content: '""',
    display: 'block',
    position: 'absolute',
    zIndex: -1,
    inset: 0,
    backgroundImage:
      'radial-gradient(ellipse at 50% 50%, hsl(210, 100%, 97%), hsl(0, 0%, 100%))',
    backgroundRepeat: 'no-repeat',
    ...theme.applyStyles('dark', {
      backgroundImage:
        'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
    }),
  },
}));

interface SignInProps {
  disableCustomTheme?: boolean;
}

const SignIn = (props: SignInProps) => {
  const navigate = useNavigate();
  const [formError, setFormError] = React.useState('');
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [idError, setIdError] = React.useState(false);
  const [passwordError, setPasswordError] = React.useState(false);
  const idInputRef = React.useRef<HTMLInputElement>(null);
  const passwordInputRef = React.useRef<HTMLInputElement>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const data = new FormData(event.currentTarget);
    const id = (data.get('id') || '').toString().trim();
    const password = (data.get('password') || '').toString().trim();

    const isIdValid = id.length > 0;
    const isPasswordValid = password.length > 0;
    const hasError = !isIdValid || !isPasswordValid;

    setIdError(!isIdValid);
    setPasswordError(!isPasswordValid);
    setFormError(hasError ? 'ID 또는 비밀번호를 입력해주세요.' : '');

    if (!isIdValid) {
      idInputRef.current?.focus();
      return;
    }

    if (!isPasswordValid) {
      passwordInputRef.current?.focus();
      return;
    }

    try {
      setIsSubmitting(true);
      setFormError('');

      const response = await signIn({ username: id, password });
      const tokens = mapTokenResponse(response);
      tokenStore.setTokens(tokens);

      navigate('/', { replace: true });
    } catch (error) {
      setFormError('로그인에 실패했습니다. 다시 시도해주세요.');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppTheme {...props}>
      <CssBaseline enableColorScheme />
      <SignInContainer direction="column" justifyContent="space-between">
        <Card variant="outlined">
          <Typography
            component="h1"
            variant="h4"
            sx={{ width: '100%', fontSize: 'clamp(2rem, 10vw, 2.15rem)' }}
          >
            Sign in
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              width: '100%',
              gap: 2,
            }}
          >
            <FormControl>
              <FormLabel htmlFor="id">ID</FormLabel>
              <TextField
                id="id"
                type="text"
                name="id"
                placeholder="your-id"
                autoComplete="username"
                autoFocus
                required
                fullWidth
                variant="outlined"
                inputRef={idInputRef}
                error={idError}
              />
            </FormControl>
            <FormControl>
              <FormLabel htmlFor="password">Password</FormLabel>
              <TextField
                id="password"
                type="password"
                name="password"
                placeholder="******"
                autoComplete="current-password"
                required
                fullWidth
                variant="outlined"
                inputRef={passwordInputRef}
                error={passwordError}
              />
            </FormControl>
            {formError && <Alert severity="error">{formError}</Alert>}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Signing in...' : 'Sign in'}
            </Button>
          </Box>
        </Card>
      </SignInContainer>
    </AppTheme>
  );
};

export default SignIn;
