import React, { useState, useEffect, useRef } from 'react';
import { 
  X, Mic, MicOff, Send, Bot, User, 
  CheckCircle2, Award 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const MockInterviewModal = ({ onClose, initialRole = "Frontend React Developer" }) => {
  const [role] = useState(initialRole);
  const [messages, setMessages] = useState([
    {
      role: 'system',
      content: `Hello! I'm your AI Technical Screener for the **${initialRole}** position at IBM partner network. Let's begin: Can you walk me through how you approach architecting scalable state management in modern React applications?`,
      timestamp: 'Just now'
    }
  ]);

  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [interviewComplete, setInterviewComplete] = useState(false);
  const [overallScore, setOverallScore] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim() || isTyping) return;

    const userText = input.trim();
    const newMessages = [
      ...messages,
      { role: 'user', content: userText, timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
    ];
    setMessages(newMessages);
    setInput('');
    setIsTyping(true);

    const turnCount = newMessages.filter(m => m.role === 'user').length;

    setTimeout(() => {
      setIsTyping(false);
      let aiReply = '';

      if (turnCount === 1) {
        aiReply = "Excellent structure! You touched on component re-renders. How would you handle asynchronous side-effects and server-state caching (e.g., TanStack Query or SWR) in that architecture?";
      } else if (turnCount === 2) {
        aiReply = "Solid answer on cache invalidation and optimistic updates. Let's shift to testing & reliability: What is your strategy for unit and integration testing with tools like Vitest and React Testing Library?";
      } else {
        aiReply = "Great job! That concludes our technical screening interview. I have compiled your competency feedback rubric and scoring analysis below.";
        setInterviewComplete(true);
        setOverallScore({
          technicalAccuracy: 88,
          communicationClarity: 92,
          problemSolving: 85,
          overallGrade: 'A-',
          feedback: [
            "Strong command of modern React architecture and component lifecycle paradigms.",
            "Clear explanation of state segregation between UI state and server cache.",
            "Bonus: Keep elaborating on automated end-to-end testing with Playwright for enterprise-grade applications."
          ]
        });
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      setMessages(prev => [
        ...prev,
        { role: 'system', content: aiReply, timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
      ]);
    }, 1400);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      setTimeout(() => {
        setInput(prev => (prev ? prev + ' ' : '') + "In my previous project, we decoupled client state using Zustand and handled server caching via TanStack Query for optimal performance.");
        setIsRecording(false);
      }, 2500);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-4xl h-[85vh] flex flex-col rounded-2xl glass-panel bg-slate-900/95 border border-slate-700/60 shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/80 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-semibold text-slate-100 text-base">AI Technical Mock Interview</h3>
                <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Live Screener
                </span>
              </div>
              <p className="text-xs text-slate-400">Target Role: {role}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg transition-colors"
              title="Close Interview"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-3 max-w-[88%] ${
                msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto flex-row'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30'
                }`}
              >
                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div className="space-y-1">
                <div
                  className={`p-4 rounded-2xl text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-tr-none'
                      : 'bg-slate-800/90 text-slate-200 border border-slate-700/60 rounded-tl-none'
                  }`}
                >
                  <p className="whitespace-pre-line">{msg.content}</p>
                </div>
                <span className={`text-[10px] text-slate-500 block px-1 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                  {msg.timestamp}
                </span>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4" />
              </div>
              <div className="p-4 rounded-2xl bg-slate-800/90 border border-slate-700/60 rounded-tl-none flex items-center gap-1.5 text-slate-400 text-xs">
                <span className="w-2 h-2 rounded-full bg-blue-400 animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-blue-400 animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 rounded-full bg-blue-400 animate-bounce [animation-delay:0.4s]"></span>
                <span className="ml-2 font-medium">AI interviewer evaluating...</span>
              </div>
            </div>
          )}

          {/* Assessment Report when completed */}
          {interviewComplete && overallScore && (
            <div className="mt-6 p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950/40 border border-indigo-500/30 shadow-xl space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="flex items-center justify-between border-b border-indigo-500/20 pb-4">
                <div className="flex items-center gap-2">
                  <Award className="w-6 h-6 text-amber-400" />
                  <h4 className="font-bold text-slate-100 text-lg">Interview Performance Evaluation</h4>
                </div>
                <div className="px-3 py-1 bg-amber-400/10 text-amber-300 border border-amber-400/30 rounded-lg text-sm font-bold">
                  Score Grade: {overallScore.overallGrade}
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                  <div className="text-xs text-slate-400 mb-1">Technical Depth</div>
                  <div className="text-2xl font-bold text-blue-400">{overallScore.technicalAccuracy}%</div>
                </div>
                <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                  <div className="text-xs text-slate-400 mb-1">Clarity & Communication</div>
                  <div className="text-2xl font-bold text-emerald-400">{overallScore.communicationClarity}%</div>
                </div>
                <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/50">
                  <div className="text-xs text-slate-400 mb-1">Problem-Solving Approach</div>
                  <div className="text-2xl font-bold text-purple-400">{overallScore.problemSolving}%</div>
                </div>
              </div>

              <div>
                <h5 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Key Feedback & Suggestions</h5>
                <ul className="space-y-2">
                  {overallScore.feedback.map((item, i) => (
                    <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/90 flex flex-col gap-2">
          {isRecording && (
            <div className="flex items-center gap-2 text-xs text-red-400 px-2 py-1 bg-red-950/40 border border-red-900/50 rounded-lg animate-pulse">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              Listening to microphone speech simulation... Click Mic again to stop.
            </div>
          )}

          <div className="flex items-center gap-2">
            <button
              onClick={toggleRecording}
              type="button"
              className={`p-3 rounded-xl border transition-all ${
                isRecording
                  ? 'bg-red-500/20 text-red-400 border-red-500/40 animate-pulse'
                  : 'bg-slate-800 text-slate-400 border-slate-700/60 hover:text-slate-200 hover:bg-slate-700'
              }`}
              title={isRecording ? 'Stop voice input' : 'Speak answer (Voice simulation)'}
            >
              {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            <input
              type="text"
              className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
              placeholder={interviewComplete ? "Interview finished! Feel free to ask any closing questions..." : "Type your technical response here..."}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />

            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              className="px-5 py-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl flex items-center gap-2 transition-all shadow-lg shadow-blue-600/20"
            >
              <span>Send</span>
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default MockInterviewModal;
