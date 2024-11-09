import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface QuestionState {
  prompt: string
  options: []
}

const initialState = {
  prompt: '',
  options: []
} as QuestionState

export const questionSlice = createSlice({
  name: 'question',
  initialState,
  reducers: {
    update: (state, action: PayloadAction<QuestionState>) => {
      state.prompt = action.payload.prompt
      state.options = action.payload.options
    }
  }
})

export const { update } = questionSlice.actions; 

export default questionSlice.reducer;
