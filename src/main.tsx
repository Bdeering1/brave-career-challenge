import { Amplify } from 'aws-amplify';
import amplifyconfig from './amplifyconfiguration.json';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { store } from './state/store'
import App from './App.tsx'
import './index.css'

Amplify.configure(amplifyconfig);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>,
)
