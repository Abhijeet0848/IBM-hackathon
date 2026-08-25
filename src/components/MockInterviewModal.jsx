import React, { useState, useEffect, useRef } from 'react';
import { X, Mic, Send, Bot, User } from 'lucide-react';

const MockInterviewModal = ({ onClose }) => {
  const [messages, setMessages] = useState([
    { role: 'system', content: "Hello. I'm the AI technical screener for this role. Let's discuss your background. Specifically, can you tell me how you would approach state management in a medium-sized React application?" }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      setIsTyping(false);
      let aiResponse = "That makes sense. Follow-up question: How would you decide between using Redux versus React's built-in Context API for that scenario?";
      
      if (newMessages.length > 3) {
        aiResponse = "Thank you. Those are all the questions I have for now. We will review your responses and get back to you.";
      }
      
      setMessages(prev => [...prev, { role: 'system', content: aiResponse }]);
    }, 1500);
  };

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 50, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}>
      {/* Simple Backdrop */}
      <div 
        style={{ position: 'absolute', inset: 0, background: 'rgba(15, 23, 42, 0.4)' }} 
        onClick={onClose}
      />
      
      {/* Modal Dialog */}
      <div className="card animate-fade-in" style={{ position: 'relative', width: '100%', maxWidth: '600px', height: '70vh', display: 'flex', flexDirection: 'column', zIndex: 51, padding: 0, overflow: 'hidden' }}>
        
        {/* Header */}
        <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#f8fafc' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
               <Bot size={18} className="text-primary" /> Technical Screening
            </h3>
          </div>
          <button onClick={onClose} className="btn-outline" style={{ padding: '0.25rem', border: 'none' }}>
            <X size={20} />
          </button>
        </div>

        {/* Chat Area */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', background: 'white' }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{ display: 'flex', gap: '0.75rem', flexDirection: msg.role === 'user' ? 'row-reverse' : 'row' }}>
              <div style={{ width: '28px', height: '28px', borderRadius: '4px', background: msg.role === 'system' ? 'var(--secondary)' : 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                {msg.role === 'system' ? <Bot size={14} color="var(--fg)" /> : <User size={14} color="white" />}
              </div>
              <div style={{ 
                background: msg.role === 'system' ? 'var(--bg)' : 'var(--primary)', 
                color: msg.role === 'system' ? 'var(--fg)' : 'white',
                padding: '0.75rem 1rem', 
                borderRadius: 'var(--radius)', 
                border: msg.role === 'system' ? '1px solid var(--border-color)' : '1px solid transparent',
                maxWidth: '85%',
                fontSize: '0.875rem'
              }}>
                {msg.content}
              </div>
            </div>
          ))}
          {isTyping && (
            <div style={{ display: 'flex', gap: '0.75rem' }}>
               <div style={{ width: '28px', height: '28px', borderRadius: '4px', background: 'var(--secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Bot size={14} color="var(--fg)" />
              </div>
              <div style={{ background: 'var(--bg)', padding: '0.75rem 1rem', borderRadius: 'var(--radius)', border: '1px solid var(--border-color)', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                Typing...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div style={{ padding: '1rem 1.5rem', borderTop: '1px solid var(--border-color)', display: 'flex', gap: '0.5rem', background: '#f8fafc' }}>
          <input 
            type="text" 
            className="input-field" 
            placeholder="Type your answer here..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            style={{ flex: 1, background: 'white' }}
          />
          <button className="btn btn-primary" onClick={handleSend} style={{ padding: '0.5rem 1rem' }}>
            Send
          </button>
        </div>

      </div>
    </div>
  );
};

export default MockInterviewModal;
