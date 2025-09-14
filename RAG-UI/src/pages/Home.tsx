// pages/Home.tsx
import { Box, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  return (
    <Box display="flex" flexDirection="column" gap={3} alignItems="center" justifyContent="center" mt={8}>
      <Typography variant="h4">Welcome to AI App</Typography>

      <Button variant="contained" onClick={() => navigate('/rag')}>
        Go to RAG UI
      </Button>

      <Button
        variant="outlined"
        onClick={() => window.open(import.meta.env.VITE_EXTERNAL_URL, '_blank', 'noopener,noreferrer')}
      >
        Go to Call Summarization UI
      </Button>
    </Box>
  );
}
