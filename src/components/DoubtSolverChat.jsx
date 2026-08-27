import React, { useState, useRef, useEffect } from 'react';
import { 
  Bot, Send, User, Sparkles, Mic, MicOff, BookOpen, 
  Trash2 
} from 'lucide-react';

const PRESET_PROMPTS = [
  "Can you explain Virtual DOM reconciliation from my React notes?",
  "What is the difference between TCP and UDP for my networking exam?",
  "How do vector embeddings work in ChromaDB?",
  "Explain Big-O notation for binary search with an example."
];

const DoubtSolverChat = ({ onAddXP }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I am **IBM Bob**, your 24/7 AI Learning Companion. I am trained on your uploaded course documents and IBM SkillsBuild modules. What doubts can I resolve for you today?",
      citations: ["ChromaDB Index: Course_Syllabus_Overview.pdf"],
      timestamp: 'Just now'
    }
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [isVoiceActive, setIsVoiceActive] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isThinking]);

  const handleSend = (textOverride) => {
    const query = textOverride || input;
    if (!query.trim() || isThinking) return;

    const userMessage = {
      role: 'user',
      content: query.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsThinking(true);

    setTimeout(() => {
      setIsThinking(false);
      let reply = `According to your uploaded course syllabus and IBM SkillsBuild notes:`;
      let citations = ["ChromaDB Chunk #7: Module_3_Core_Concepts.pdf (Confidence: 97%)"];

      const qLower = query.toLowerCase();
      if (qLower.includes('dom') || qLower.includes('react')) {
        reply = `**Virtual DOM & Reconciliation Explained:**\n\n1. **Virtual DOM Tree:** React maintains an in-memory lightweight representation of the UI.\n2. **Diffing Algorithm:** When state updates occur, React generates a new Virtual DOM tree and diffs it with the previous one (O(n) heuristic).\n3. **Batch Patching:** Only the changed nodes are updated in the actual browser DOM, saving massive layout recalculation costs.\n\n*Bob's Tip: Use \`React.memo\` and \`useCallback\` to avoid re-rendering heavy child components unnecessarily!*`;
        citations = ["ChromaDB Chunk #12: React_Advanced_Patterns.pdf", "IBM SkillsBuild: Frontend Performance"];
      } else if (qLower.includes('tcp') || qLower.includes('udp')) {
        reply = `**TCP vs UDP Comparison:**\n\n- **TCP (Transmission Control Protocol):** Connection-oriented, guarantees packet delivery via 3-way handshake and retransmission. Best for web browsing (HTTP/HTTPS) and file transfers.\n- **UDP (User Datagram Protocol):** Connectionless, lightweight, no delivery guarantee, minimal latency. Best for live gaming, video streaming, and VoIP.`;
        citations = ["ChromaDB Chunk #4: Networking_Protocols.pdf"];
      } else if (qLower.includes('vector') || qLower.includes('chroma')) {
        reply = `**Vector Embeddings & ChromaDB:**\n\nText chunks are transformed into multi-dimensional floating-point vectors by embedding models. When you ask a doubt, your query is embedded and matched against stored document vectors using Cosine Similarity to extract the most relevant syllabus context!`;
        citations = ["ChromaDB Chunk #2: RAG_Vector_Search.pdf", "IBM Granite AI Spec"];
      } else {
        reply = `Based on your course materials for **${query}**:\n\nThe fundamental principle is to break the problem into modular, testable components. Always verify edge cases and establish clear input/output contracts before writing code.`;
      }

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: reply,
          citations,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);

      if (onAddXP) onAddXP(20);
    }, 1100);
  };

  const handleVoiceToggle = () => {
    setIsVoiceActive(!isVoiceActive);
    if (!isVoiceActive) {
      setTimeout(() => {
        setInput("Can you explain Virtual DOM reconciliation from my React notes?");
        setIsVoiceActive(false);
      }, 2000);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: "Chat cleared. Ask me any new doubts from your course documents!",
        citations: ["ChromaDB Vector Store"],
        timestamp: 'Just now'
      }
    ]);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      
      {/* Top Banner */}
      <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-slate-900 text-sm">IBM Bob's 24/7 Doubt-Solving AI</h3>
              <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-semibold">
                ● RAG Active
              </span>
            </div>
            <p className="text-xs text-slate-500">Trained on your uploaded syllabus & notes</p>
          </div>
        </div>

        <button
          onClick={handleClearChat}
          className="text-xs text-slate-500 hover:text-rose-600 flex items-center gap-1 transition-colors p-2 cursor-pointer"
          title="Clear Chat History"
        >
          <Trash2 className="w-4 h-4" />
          <span className="hidden sm:inline">Clear Chat</span>
        </button>
      </div>

      {/* Suggested Doubt Prompts */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs text-slate-500 font-semibold flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-blue-600" /> Quick Questions:
        </span>
        {PRESET_PROMPTS.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSend(prompt)}
            className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 hover:border-blue-400 text-slate-700 text-xs font-medium transition-all cursor-pointer shadow-xs"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Messages Box */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs h-[520px] flex flex-col justify-between overflow-hidden">
        
        <div className="overflow-y-auto space-y-4 pr-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 max-w-[88%] ${
                msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto flex-row'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'bg-blue-50 text-blue-600 border border-blue-200'
                }`}
              >
                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div className="space-y-1.5">
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-tr-none'
                      : 'bg-slate-50 text-slate-800 border border-slate-200 rounded-tl-none'
                  }`}
                >
                  <p className="whitespace-pre-line">{msg.content}</p>
                </div>

                {msg.citations && msg.citations.length > 0 && (
                  <div className="flex flex-wrap gap-1 px-1">
                    {msg.citations.map((c, i) => (
                      <span
                        key={i}
                        className="text-[10px] font-mono text-cyan-800 bg-cyan-50 border border-cyan-200 px-2 py-0.5 rounded-md flex items-center gap-1"
                      >
                        <BookOpen className="w-3 h-3 text-cyan-600" />
                        <span>{c}</span>
                      </span>
                    ))}
                  </div>
                )}

                <span className={`text-[10px] text-slate-400 block px-1 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                  {msg.timestamp}
                </span>
              </div>
            </div>
          ))}

          {isThinking && (
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4" />
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 rounded-tl-none flex items-center gap-1.5 text-slate-500 text-xs">
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce [animation-delay:0.4s]"></span>
                <span className="ml-2 font-medium">IBM Bob searching vector index...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="pt-4 border-t border-slate-100 flex flex-col gap-2">
          {isVoiceActive && (
            <div className="flex items-center gap-2 text-xs text-red-600 px-3 py-1.5 bg-red-50 border border-red-200 rounded-xl animate-pulse">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              <span>Listening to speech input simulation...</span>
            </div>
          )}

          <div className="flex items-center gap-2">
            <button
              onClick={handleVoiceToggle}
              className={`p-3 rounded-xl border transition-all cursor-pointer ${
                isVoiceActive
                  ? 'bg-red-50 border-red-300 text-red-600 animate-pulse'
                  : 'bg-slate-50 text-slate-600 border-slate-200 hover:text-slate-900 hover:bg-slate-100'
              }`}
              title="Voice Doubt Simulation"
            >
              {isVoiceActive ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            <input
              type="text"
              className="flex-1 px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 text-xs sm:text-sm focus:bg-white focus:outline-none focus:border-blue-600"
              placeholder="Ask Bob any doubt from your syllabus..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />

            <button
              onClick={() => handleSend()}
              disabled={!input.trim() || isThinking}
              className="px-5 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-xl text-xs sm:text-sm font-semibold flex items-center gap-1.5 shadow-xs transition-all cursor-pointer"
            >
              <span>Ask Bob</span>
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>

    </div>
  );
};

export default DoubtSolverChat;
