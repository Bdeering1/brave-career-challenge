import GradientBackground from './components/gradient-bg'
import UrlEntry from './components/url-entry'

function App() {
  return (
    <div className="h-full">
      <GradientBackground />
      <div className="h-full flex justify-center items-center">
        <UrlEntry />
      </div>
    </div>
  )
}

export default App
