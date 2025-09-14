// redux/ragSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface TraceNode {
  name: string;
  input: any;
  output: any;
  status: string;
}

interface RAGState {
  response: string;
  trace: TraceNode[];
}

const initialState: RAGState = {
  response: '',
  trace: [],
};

const ragSlice = createSlice({
  name: 'rag',
  initialState,
  reducers: {
    setResponse: (state, action: PayloadAction<string>) => {
      state.response = action.payload;
    },
    setTrace: (state, action: PayloadAction<TraceNode[]>) => {
      state.trace = action.payload;
    },
    clearAll: (state) => {
      state.response = '';
      state.trace = [];
    },
  },
});

export const { setResponse, setTrace, clearAll } = ragSlice.actions;
export default ragSlice.reducer;