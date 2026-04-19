import { useState } from 'react';
import { Box, Button, TextField, Typography, List, ListItem, ListItemText, Paper } from '@mui/material';
import { getRecommendations } from '../services/api';

export default function RecommendForm({ token, onError, onSuccess }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) {
      onError('Please enter a search query first.');
      return;
    }
    setLoading(true);
    try {
      const data = await getRecommendations(token, query);
      setResults(data.recommendations || []);
      onSuccess('Recommendations loaded successfully.');
    } catch (error) {
      onError(error.message || 'Recommendation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: 'grid', gap: 2 }} component="form" onSubmit={handleSubmit}>
      <Typography variant="h6">Get recipe suggestions</Typography>
      <TextField
        label="Search ingredients or recipe"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        fullWidth
      />
      <Button type="submit" variant="contained" disabled={loading}>
        {loading ? 'Searching…' : 'Get Recommendations'}
      </Button>

      {results.length > 0 && (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography variant="subtitle1" sx={{ mb: 1 }}>
            Top recipe matches
          </Typography>
          <List>
            {results.map((item, index) => (
              <ListItem key={index} divider>
                <ListItemText
                  primary={item.recipe}
                  secondary={Array.isArray(item.ingredients) ? item.ingredients.join(', ') : item.ingredients}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
}
