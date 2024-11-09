import GradientBackground from './components/gradient-bg'
import UrlEntry from './components/url-entry'
import SurveyForm from './components/survey-form'

function App() {
  return (
    <div className="h-full">
      <GradientBackground />
      <div className="h-full flex flex-col justify-center items-center">
        <UrlEntry />
        <SurveyForm />
      </div>
    </div>
  )
}

export default App
