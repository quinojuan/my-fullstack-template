import { BrowserRouter } from 'react-router-dom'
import AppRouter from './routers/AppRouter'
import '../shared/styles/App.css'

function App() {
  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  )
}

export default App