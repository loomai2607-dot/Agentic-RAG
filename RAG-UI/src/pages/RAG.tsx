// RAG.tsx - Main Page
import { useState } from 'react';
import { Box, Typography } from '@mui/material';
import { RAGChat } from '@/components/RAGChat';
import { RAGUpload } from '@/components/RAGUpload';
import { RAGTraceCanvas } from '@/components/RAGTraceCanvas';

export default function RAGPage() {
  const [traceGraph, setTraceGraph] = useState<any>(null);
  const [traceLog, setTraceLog] = useState<any[]>([]);
  const [response, setResponse] = useState<string>('');

  return (
    <Box p={4} display="flex" flexDirection="column" gap={4}>
      <Typography variant="h4" fontWeight="bold">
        RAG Chat Interface
      </Typography>

      <RAGUpload />

      <RAGChat
        onResult={setResponse}
        onTrace={(graph: any, log: any[]) => {
          setTraceGraph(graph);
          setTraceLog(log);
        }}
      />

      {response && (
        <Box p={2} bgcolor="#f9f9f9" borderRadius={2}>
          <Typography variant="h6">Answer</Typography>
          <Typography>{response}</Typography>
        </Box>
      )}

      {traceGraph && (
        <Box>
          <Typography variant="h6">LangGraph Trace</Typography>
          <RAGTraceCanvas graph={traceGraph} log={traceLog} />
        </Box>
      )}
    </Box>
  );
}
