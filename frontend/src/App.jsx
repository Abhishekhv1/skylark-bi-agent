import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import './App.css';
import remarkGfm from 'remark-gfm';

function App() {
  const [messages, setMessages] = useState([
    {
      sender: 'agent',
      text: 'Hello! I am your Monday.com Business Intelligence Agent. How can I assist you with deal pipelines or work order metrics today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const res = await fetch('https://skylark-bi-agent-61rc.onrender.com/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { sender: 'agent', text: data.response }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'agent', text: '⚠️ Error connecting to backend server. Make sure FastAPI is running.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>Monday.com Business Intelligence Agent</h1>
        <p>Executive Analytics & Real-Time Insights</p>
      </header>

      <div className="messages-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message-row ${msg.sender}`}>
            <div className="avatar">
              {msg.sender === 'agent' ? <Bot size={20} /> : <User size={20} />}
            </div>
            <div className="message-bubble">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {msg.text}
            </ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div className="message-row agent">
            <div className="avatar"><Bot size={20} /></div>
            <div className="message-bubble loading-bubble">
              <Loader2 className="spinner" size={18} /> Analyzing Monday.com datasets...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} className="input-form">
        <input
          type="text"
          placeholder="Ask a question (e.g., How is our energy pipeline looking?)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}

export default App;