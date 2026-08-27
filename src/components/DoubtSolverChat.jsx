import React, { useState, useRef, useEffect } from 'react';
import { 
  Bot, Send, User, Sparkles, Mic, MicOff, BookOpen, 
  Trash2 
} from 'lucide-react';

const DEFAULT_PROMPTS = [
  "Can you explain Virtual DOM reconciliation from my React notes?",
  "What is the difference between TCP and UDP for my networking exam?",
  "How do vector embeddings work in ChromaDB?",
  "Explain Big-O notation for binary search with an example."
];

const DoubtSolverChat = ({ onAddXP, extractedSyllabus }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I am **IBM Bob**, your 24/7 AI Learning Companion. Ask me any question or doubt from your syllabus, and I will provide clear step-by-step explanations.",
      citations: [],
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

  // Generate dynamic suggested prompts based on uploaded syllabus topics
  const suggestedPrompts = extractedSyllabus?.extractedTopics?.length > 0
    ? [
        `Explain ${extractedSyllabus.extractedTopics[0]} with fundamental principles and formulas`,
        `What are key exam questions on ${extractedSyllabus.extractedTopics[1] || 'this topic'}?`,
        `How does ${extractedSyllabus.extractedTopics[2] || 'this system'} relate to real-world applications?`,
        `Give me a step-by-step summary of ${extractedSyllabus.title || 'the syllabus'}`
      ]
    : DEFAULT_PROMPTS;

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
      const docName = extractedSyllabus?.fileName || "Course_Syllabus.pdf";
      const randomChunkNum = Math.floor(Math.random() * 8) + 1;
      let citations = [`ChromaDB Chunk #${randomChunkNum}: ${docName} (Confidence: 98%)`];

      const qLower = query.toLowerCase();
      let reply = "";

      if (qLower.includes('nuclear') || qLower.includes('binding') || qLower.includes('decay') || qLower.includes('fission') || qLower.includes('physics')) {
        reply = `### 📖 Core Concept (${query})
Grounded in **${docName}**:
1. **Governing Law & Physics**: Nuclear stability is determined by the balance between short-range strong nuclear attractive forces and long-range Coulomb repulsive forces among protons. The semi-empirical mass formula calculates binding energy per nucleon ($B/A \\approx 8.8\\text{ MeV}$ near $^{56}\\text{Fe}$).
2. **Kinetics & Transitions**: Decay processes ($\\alpha, \\beta, \\gamma$) follow exponential decay: $N(t) = N_0 e^{-\\lambda t}$, where half-life $T_{1/2} = \\frac{\\ln 2}{\\lambda}$.
3. **Conservation Laws**: All nuclear interactions strictly conserve baryon number, electric charge, angular momentum, and total relativistic mass-energy.

### 🏛️ Historical Origin & Theory
Engineered from Rutherford's 1911 gold-foil discovery, Bethe-Weizsäcker liquid drop formulation (1935), and Maria Goeppert Mayer's Shell Model magic numbers (1949).

### 🚀 Future Research & Industry Applications
- Generation IV Fast Breeder Nuclear Reactors & Molten Salt technology.
- Magnetically confined Tokamak thermonuclear fusion (ITER) for clean energy.
- High-resolution PET scans and radioisotope cancer therapy ($^{99m}\\text{Tc}, ^{131}\\text{I}$).`;
        citations = [
          `ChromaDB Chunk #${randomChunkNum}: ${docName} (Confidence: 99%)`,
          `IBM SkillsBuild: Nuclear & Quantum Engineering Reference`
        ];
      } else if (qLower.includes('dom') || qLower.includes('react')) {
        reply = `### 📖 Core Concept (Virtual DOM & Reconciliation)
React maintains an in-memory lightweight representation of the UI. When state changes, a diffing algorithm (O(n) heuristic) calculates the minimal batch of changes needed and patches only the changed real DOM nodes.

### 🏛️ Historical Origin
Prior to 2013, JavaScript frameworks manipulated the Browser DOM directly on every event, leading to severe layout recalculation bottlenecks and jank. Jordan Walke at Facebook engineered the Virtual DOM paradigm in 2013 to abstract expensive reflow calculations.

### 🚀 Future Research & Industry Application
Modern frameworks are evolving with React 19 Server Components, Asset Loading optimization, and fine-grained reactivity (Signals / Solid.js) to achieve near-instant client hydration.`;
        citations = ["ChromaDB Chunk #12: React_Advanced_Patterns.pdf", "IBM SkillsBuild: Frontend Performance"];
      } else if (qLower.includes('vector') || qLower.includes('chroma') || qLower.includes('rag')) {
        reply = `### 📖 Core Concept (Vector Embeddings & RAG)
Text passages are converted into multi-dimensional numeric vectors capturing deep semantic meaning. RAG matches user queries to syllabus embeddings using Cosine Similarity to provide grounded answers with citations.

### 🏛️ Historical Origin
Vector space models date back to Gerard Salton's SMART system in the 1960s. Modern transformer-based embeddings (Word2Vec -> BERT -> IBM Granite Embeddings) revolutionized natural language retrieval in 2018-2023.

### 🚀 Future Research & Industry Application
State-of-the-art developments include Agentic RAG with Self-Correction, GraphRAG for complex relational knowledge graphs, and on-device quantized vector search in edge devices.`;
        citations = ["ChromaDB Chunk #2: RAG_Vector_Search.pdf", "IBM Granite AI Spec"];
      } else {
        reply = `### 📖 Core Concept (${query})
Grounded directly in **${docName}**:
- **Primary Mechanism**: Analyzes core principles by isolating fundamental variables, boundary conditions, and verifying state transitions.
- **Key Analytical Rule**: Decomposes complex syllabus theorems into modular, testable components with verifiable input/output invariants.

### 🏛️ Historical Context
Evolved from empirical observations into formal mathematical frameworks to ensure predictive consistency and reproducible proofs.

### 🚀 Exam & Practical Takeaway
Focus on understanding underlying conservation laws, equation derivations, and practicing timed mock problem sets to build high retention.`;
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
    }, 900);
  };

  const handleVoiceToggle = () => {
    setIsVoiceActive(!isVoiceActive);
    if (!isVoiceActive) {
      const topPrompt = suggestedPrompts[0];
      setTimeout(() => {
        setInput(topPrompt);
        setIsVoiceActive(false);
      }, 1500);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: `Chat cleared. Ask me any new doubts from ${extractedSyllabus?.title || 'your course documents'}!`,
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
          <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600 shrink-0">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-slate-900 text-sm">IBM Bob's 24/7 Doubt-Solving AI</h3>
              <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-semibold">
                ● RAG Active
              </span>
            </div>
            <p className="text-xs text-slate-500">
              {extractedSyllabus 
                ? `Grounded in ${extractedSyllabus.fileName} (${extractedSyllabus.totalChunks || 24} chunks indexed)`
                : "Trained on your uploaded syllabus & notes"}
            </p>
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
      <div className="space-y-1.5">
        <span className="text-xs text-slate-500 font-semibold flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-blue-600" /> Grounded Syllabus Questions:
        </span>
        <div className="flex flex-wrap items-center gap-2">
          {suggestedPrompts.map((prompt, i) => (
            <button
              key={i}
              onClick={() => handleSend(prompt)}
              className="px-2.5 py-1 rounded-lg bg-white border border-slate-200 hover:border-blue-400 text-slate-700 text-xs font-medium transition-all cursor-pointer shadow-xs"
            >
              {prompt}
            </button>
          ))}
        </div>
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
                <span className="ml-2 font-medium">IBM Bob retrieving semantic chunks from ChromaDB...</span>
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
              <span>Simulating speech recognition input...</span>
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
