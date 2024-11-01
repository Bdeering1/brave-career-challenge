import { useState } from 'react'
import { Search } from 'lucide-react'

const API_ROUTE = '/scrape'

export default function UrlEntry() {
  const [inputUrl, setUrl] = useState('')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setUrl('');

    const baseUrl = import.meta.env.VITE_API_ROOT;
    const endpoint = new URL(API_ROUTE, baseUrl)
    endpoint.searchParams.append('url', inputUrl);

    try {
      const res = await fetch(endpoint)
      if (!res.ok) throw new Error(`Response status: ${res.status}`);

      const json = await res.json();
      console.log(json);
    } catch (err: unknown) {
      console.error((err as Error).message);
    }
  }

  return (
    <div className="w-full max-w-md mx-auto p-4">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="url"
          value={inputUrl}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
          className="w-full px-4 py-2 pr-10 rounded-full bg-white bg-opacity-20 backdrop-blur-sm border border-white border-opacity-30 text-white placeholder-white placeholder-opacity-70 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 transition-all duration-300 ease-in-out"
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
