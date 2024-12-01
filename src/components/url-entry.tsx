import { useState } from 'react'
import { RotateCw, Search } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { useAppSelector, useAppDispatch } from '../state/hooks'
import { load, hide, update, QuestionState, QuestionStatus } from '../state/questionSlice'
import { ApiError, get } from 'aws-amplify/api'

const API_ROUTE = '/scrape'

export default function UrlEntry() {
  const [inputUrl, setInputUrl] = useState('')
  const [prevUrl, setPrevUrl] = useState('')
  const status = useAppSelector(state => state.question.status)
  const dispatch = useAppDispatch()

  const hideFeedback = () => dispatch(hide())

  const sendRequest = async (url: string, force_prompt: boolean) => {
    if (import.meta.env.PROD) { // hit production endpoint
      interface QueryParams {
        url: string,
        [key: string]: string
      }

      const queryParams: QueryParams = { url: url }
      if (force_prompt)
        queryParams['force-prompt'] = ''

      const getOperation = get({
        apiName: 'flask',
        path: API_ROUTE,
        options: {
          queryParams
        }
      })

      try {
        const { body } = await getOperation.response;
        const json = await body.json()

        dispatch(update(json as unknown as QuestionState))
      } catch (err: unknown) {
        dispatch(hide())
        if (err instanceof ApiError && err.response) {
          const {
            statusCode,
            body
          } = err.response;

          console.error(`Response status: ${statusCode} - ${body}`);
        }

        console.error((err as Error).message)
      }
    } else { // hit local server
      const baseUrl = import.meta.env.VITE_API_ROOT
      const endpoint = new URL(API_ROUTE, baseUrl)
      endpoint.searchParams.append('url', url)

      if (force_prompt)
        endpoint.searchParams.append('force-prompt', '')

      try {
        const res = await fetch(endpoint)
        const json = await res.json()
        if (!res.ok) {
          dispatch(hide())
          throw new Error(`Response status: ${res.status} - ${json}`)

        }

        dispatch(update(json))
      } catch (err: unknown) {
        dispatch(hide())
        console.error((err as Error).message)
      }
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    dispatch(load())

    setPrevUrl(inputUrl)
    await sendRequest(inputUrl, false)
    setInputUrl('')
  }

  const handleRetrySubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    dispatch(load())

    await sendRequest(prevUrl, true)
    setInputUrl('')
  }

  return (
    <div
      onFocus={() => hideFeedback()}
      className={`w-full max-w-md mx-auto p-4 ${status === QuestionStatus.Hidden ||  status === QuestionStatus.Complete ? '' : 'hidden'}`}
    >
      <div className="flex space-x-2">
        <form onSubmit={handleSubmit} className="relative flex-grow">
          <input
            type="url"
            value={inputUrl}
            onChange={(e) => setInputUrl(e.target.value)}
            placeholder="Enter URL"
            className="w-full px-4 py-2 pr-10 rounded-lg bg-primary/20 backdrop-blur-sm border border-primary text-white placeholder-white placeholder-opacity-70 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 transition-all duration-300 ease-in-out"
            required
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 transform -translate-y-1/2 text-white/80 hover:opacity-100 transition-opacity duration-300 ease-in-out"
            aria-label="Submit URL"
          >
            <Search className="w-5 h-5" />
          </button>
        </form>
        <TooltipProvider delayDuration={400}>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                type="submit"
                variant="outline"
                size="icon"
                className={`relative rounded-full w-10 h-10 bg-primary/20 hover:bg-primary/20 duration-200 border-primary text-priamry/80 hover:opacity-100 ${prevUrl !== '' ? '' : 'hidden'}`}
                onClick={handleRetrySubmit}
                aria-label="Retry with previous entry"
              >
                <RotateCw className="h-4 w-4" />
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Retry with previous URL</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </div>
    </div>
  )
}
