import { useState, ChangeEventHandler } from 'react'
import { Search } from 'lucide-react'
import { useAppSelector, useAppDispatch } from '../state/hooks'
import { load, hide, update, QuestionStatus } from '../state/questionSlice'

const API_ROUTE = '/scrape'

export default function UrlEntry() {
  const [inputUrl, setUrl] = useState('')
  const status = useAppSelector(state => state.question.status)
  const dispatch = useAppDispatch()

  const hideFeedback = () => dispatch(hide())

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setUrl('')
    dispatch(load())

    const baseUrl = import.meta.env.VITE_API_ROOT
    const endpoint = new URL(API_ROUTE, baseUrl)
    endpoint.searchParams.append('url', inputUrl)

    try {
      const res = await fetch(endpoint)
      if (!res.ok) throw new Error(`Response status: ${res.status}`)

      const json = await res.json()
      console.log(json)
      dispatch(update(json))
    } catch (err: unknown) {
      console.error((err as Error).message)
    }
  }

  return (
    <div
      onFocus={() => hideFeedback()}
      className={`w-full max-w-md mx-auto p-4 ${status === QuestionStatus.Hidden ||  status === QuestionStatus.Complete ? '' : 'hidden'}`}
    >
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="url"
          value={inputUrl}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
          className="w-full px-4 py-2 pr-10 rounded-lg bg-white bg-opacity-20 backdrop-blur-sm border border-white border-opacity-30 text-white placeholder-white placeholder-opacity-70 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 transition-all duration-300 ease-in-out"
          required
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-white opacity-70 hover:opacity-100 transition-opacity duration-300 ease-in-out"
          aria-label="Submit URL"
        >
          <Search className="w-5 h-5" />
        </button>
      </form>
    </div>
  )
}
