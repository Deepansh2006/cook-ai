import { useEffect, useState } from 'react';
import { Box, Button, List, ListItem, ListItemText, Paper, Typography } from '@mui/material';
import { getHistory } from '../services/api';

export default function HistoryList({ token, onError, onLogout, refreshKey }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const data = await getHistory(token);
        setHistory(data.history || []);
      } catch (error) {
        onError(error.message || 'Could not load history');
      } finally {
        setLoading(false);
      }
    };
    if (token) {
      load();
    }
  }, [token, refreshKey, onError]);

  return (
    <Box sx={{ display: 'grid', gap: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6">Your search history</Typography>
        <Button variant="outlined" color="secondary" onClick={onLogout}>
          Logout
        </Button>
      </Box>
      <Paper variant="outlined" sx={{ p: 2 }}>
        {loading ? (
          <Typography>Loading history…</Typography>
        ) : history.length === 0 ? (
          <Typography>No saved searches yet.</Typography>
        ) : (
          <List>
            {history.map((item, index) => (
              <ListItem key={index} divider>
                <ListItemText
                  primary={item.query}
                  secondary={`Results: ${item.result_count} · ${new Date(item.created_at).toLocaleString()}`}
                />
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
    </Box>
  );
}
