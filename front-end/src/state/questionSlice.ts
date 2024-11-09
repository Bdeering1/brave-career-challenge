import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export enum QuestionStatus {
  Hidden = 'hidden',
  Loading = 'loading',
  Ready = 'ready',
  Complete = 'complete'
}

export interface QuestionState {
  prompt: string
  options: []
  status: QuestionStatus
}

const initialState = {
  prompt: '',
  options: [],
  status: QuestionStatus.Hidden
} as QuestionState

export const questionSlice = createSlice({
  name: 'question',
  initialState,
  reducers: {
    load: (state) => {
      state.status = QuestionStatus.Loading
    },
    complete: (state) => {
      state.status = QuestionStatus.Complete
    },
    hide: (state) => {
      state.status = QuestionStatus.Hidden
    },
    update: (state, action: PayloadAction<QuestionState>) => {
      state.prompt = action.payload.prompt
      state.options = action.payload.options
      state.status = QuestionStatus.Ready
    }
  }
})

export const { load, complete, hide, update } = questionSlice.actions; 

export default questionSlice.reducer;
