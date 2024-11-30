import { cn } from "@/lib/utils"
import { useAppSelector } from '../state/hooks'
import { QuestionStatus } from "../state/questionSlice"

interface LoadingIndicatorProps {
  className?: string
}

export default function Spinner({ 
  className 
}: LoadingIndicatorProps = {}) {
  const status = useAppSelector(state => state.question.status)

  return (
    <div className={`flex items-center justify-center ${status === QuestionStatus.Loading ? '' : 'hidden'}`}>
      <div
        className={cn(
          "w-16 h-16 border-4 animate-spin rounded-full border-solid border-primary/80 border-t-transparent",
          className
        )}
        role="status"
        aria-label="Loading"
      >
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  )
}
