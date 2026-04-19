import { useState } from 'react';
import { Box, Button, TextField, Typography } from '@mui/material';
import { registerUser } from '../services/api';

export default function RegisterForm({ onRegister, onError }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (password !== confirm) {
      onError('Password and confirm password must match');
      return;
    }
    setLoading(true);
    try {
      const result = await registerUser(username, password);
      onRegister(result.token);
    } catch (error) {
      onError(error.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'grid', gap: 2 }}>
      <Typography variant="h6">Create a new account</Typography>
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
      <TextField
        label="Confirm Password"
        type="password"
        value={confirm}
        onChange={(event) => setConfirm(event.target.value)}
        fullWidth
        required
      />
      <Button type="submit" variant="contained" disabled={loading}>
        {loading ? 'Registering…' : 'Register'}
      </Button>
    </Box>
  );
}
