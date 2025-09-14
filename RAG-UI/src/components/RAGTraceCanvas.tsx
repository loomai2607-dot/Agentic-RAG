// components/RAGTraceCanvas.tsx
import React, { useEffect, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  ReactFlowProvider,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import { Dialog, DialogTitle, DialogContent, Typography } from '@mui/material';
import 'reactflow/dist/style.css';

export function RAGTraceCanvas({ graph, log }: { graph: any; log: any[] }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const generatedNodes = graph.nodes.map((n: any, idx: number) => ({
      id: n.id,
      position: { x: 150 * idx, y: 100 },
      data: { label: n.label },
      style: { border: '1px solid #999', borderRadius: 8, padding: 8 },
    }));

    const generatedEdges = graph.edges.map((e: any) => ({
      id: `${e.source}-${e.target}`,
      source: e.source,
      target: e.target,
    }));

    setNodes(generatedNodes);
    setEdges(generatedEdges);
  }, [graph]);

  const onNodeClick = (_event: any, node: any) => {
    const match = log.find((l) => l.node === node.id);
    if (match) {
      setSelectedNode(match);
      setDialogOpen(true);
    }
  };

  return (
    <div style={{ height: 400, width: '100%' }}>
      <ReactFlowProvider>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
        >
          <Controls />
          <Background />
        </ReactFlow>
      </ReactFlowProvider>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Node Details: {selectedNode?.node}</DialogTitle>
        <DialogContent>
          <Typography variant="subtitle2">Input:</Typography>
          <Typography>{selectedNode?.input || '—'}</Typography>
          <Typography variant="subtitle2" mt={2}>Output:</Typography>
          <Typography>{Array.isArray(selectedNode?.output) ? JSON.stringify(selectedNode.output) : selectedNode?.output || '—'}</Typography>
        </DialogContent>
      </Dialog>
    </div>
  );
}
