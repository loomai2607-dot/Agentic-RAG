// components/RAGUpload.tsx
import { Box, Button, Typography } from '@mui/material';
import { useRef, useState } from 'react';

export function RAGUpload() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileUpload = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setStatus('Uploading...');

    try {
      const res = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      
      const data = await res.json();
      setStatus(data.message || 'Upload successful');
    } catch (err) {
      console.error('Upload failed:', err);
      setStatus('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box>
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.txt"
        style={{ display: 'none' }}
        onChange={handleFileUpload}
      />
      <Button
        variant="outlined"
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
      >
        {uploading ? 'Uploading...' : 'Upload Document'}
      </Button>
      {status && <Typography mt={1}>{status}</Typography>}
    </Box>
  );
}