import { useState } from 'react';
import { Box, Button, TextField, Typography } from '@mui/material';
import { loginUser } from '../services/api';

export default function LoginForm({ onLogin, onError, loggedIn }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const result = await loginUser(username, password);
      onLogin(result.token);
    } catch (error) {
      onError(error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'grid', gap: 2 }}>
      <Typography variant="h6">Login to Cook AI</Typography>
      <TextField
        label="Username"
        value={username}
        onChange={(event) => setUsername(event.target.value)}
        fullWidth
        required
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        fullWidth
        required
      />
      <Button type="submit" variant="contained" disabled={loading || loggedIn}>
        {loggedIn ? 'Already logged in' : loading ? 'Logging in…' : 'Login'}
      </Button>
    </Box>
  );
}
