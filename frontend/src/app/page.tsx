'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ChatDemo() {
  const [prompt, setPrompt] = useState('shop from walmart.ca a healthy recipe organic')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<any>(null)
  const router = useRouter()

  const handleSend = async () => {
    setLoading(true)
    setResponse(null)
    try {
      const res = await fetch('/api/agent/shop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      })
      const data = await res.json()
      setResponse(data)
      
      // If it requires human approval, redirect to the new order
      if (data.requires_approval && data.order_id) {
        setTimeout(() => {
          router.push(`/admin/approvals/${data.order_id}`)
        }, 2000)
      }
    } catch (e: any) {
      setResponse({ error: e.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-20 p-6 border rounded-lg shadow-sm">
      <h1 className="text-2xl font-bold mb-4">Autonomous AI Shopper</h1>
      <p className="text-gray-600 mb-6">
        Ask the agent to shop for you. The agent is secured by the Autonomous Commerce Harness.
      </p>

      <div className="flex flex-col gap-4">
        <textarea 
          className="border p-4 rounded-md w-full"
          rows={3}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button 
          className="bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
          onClick={handleSend}
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Send to Agent'}
        </button>
      </div>

      {response && (
        <div className="mt-8 p-4 bg-gray-50 rounded-md whitespace-pre-wrap font-mono text-sm">
          {JSON.stringify(response, null, 2)}
        </div>
      )}
    </div>
  )
}
