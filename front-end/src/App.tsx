import GradientBackground from './components/gradient-bg'
import UrlEntry from './components/url-entry'
import SurveyForm from './components/survey-form'
import Spinner from './components/spinner'

function App() {
  return (
    <div className="h-full">
      <GradientBackground />
      <div className="h-full flex flex-col justify-center items-center">
        <UrlEntry />
        <SurveyForm />
        <Spinner />
      </div>
    </div>
  )
}

export default App
