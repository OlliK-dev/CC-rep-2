import { useState } from 'react'
import './App.css'

function App() {

  const [text, setText] = useState('')
  const [sentiment, setSentiment] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!text.trim()) return

    setLoading(true)
    setSentiment('')

    try {
      const response = await fetch('https://cc-rep-2-backend-git-cloud-computing-2026.2.rahtiapp.fi/sentiment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({text}),
      })

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
