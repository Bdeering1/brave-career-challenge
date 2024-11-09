import { useState } from "react"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useAppSelector } from '../state/hooks'

export default function SurveyForm() {
  const [selectedAnswer, setSelectedAnswer] = useState("")
  const prompt = useAppSelector(state => state.question.prompt)
  const options = useAppSelector(state => state.question.options)

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    console.log("Submitted answer:", selectedAnswer)
  }

  return (
    <Card className="w-full max-w-lg mx-auto bg-white bg-opacity-20 backdrop-blur-sm border-white border-opacity-30">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center relative">{prompt}</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <div className="space-y-6">
            <RadioGroup value={selectedAnswer} onValueChange={setSelectedAnswer} className="space-y-3">
              {options.map((opt) => (
                <div key={opt} className="flex items-center space-x-2 rounded-lg border border-white border-opacity-30 transition-colors hover:bg-foreground/20">
                  <RadioGroupItem value={opt} id={opt} className="border-primary text-primary m-4" />
                  <Label htmlFor={opt} className="flex-grow cursor-pointer font-medium">
                    {opt}
                  </Label>
                </div>
              ))}
            </RadioGroup>
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full text-primary border border-white border-opacity-30 bg-white bg-opacity-10 hover:bg-primary/30" disabled={!selectedAnswer}>
            Submit Answer
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}
