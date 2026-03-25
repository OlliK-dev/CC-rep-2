import { useState } from 'react'
import './App.css'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
).replace(/\/$/, '')

function App() {

  const [text, setText] = useState('')
  const [sentiment, setSentiment] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!text.trim()) return

    setLoading(true)
    setSentiment('')

    try {
      const response = await fetch(`${API_BASE_URL}/sentiment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({text}),
      })

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      const data = await response.json()
      setSentiment(data.sentiment)
    } catch (error) {
      setSentiment('Error contacting backend')
    }

    setLoading(false)
  }

  return (
    <div className='page'>


      <div className="header-one">
        <h1>
          Sentiment Analysis Project
        </h1>
      </div>


      <div className='border-box'>

        <div className='text'>
          <h2>Write a sentence that will be analyzed:</h2>
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder='type a sentence'
          />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>


          {sentiment && <h3>Sentiment: {sentiment}</h3>}
        </div>

      </div>

    </div>

  )
}

export default App
