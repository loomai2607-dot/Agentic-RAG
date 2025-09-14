// components/RAGChat.tsx
import { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';

export function RAGChat({ onResult, onTrace }: any) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_RAG_API_QUERY}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      onResult(data.answer);
      onTrace(data.trace_graph, data.trace_log);
    } catch (err) {
      console.error('RAG Query failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box display="flex" gap={2}>
      <TextField
        fullWidth
        label="Ask your question"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
      />
      <Button variant="contained" onClick={handleSubmit} disabled={loading}>
        {loading ? 'Loading...' : 'Submit'}
      </Button>
    </Box>
  );
}
