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
    }, 1300);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      setTimeout(() => {
        setInput(prev => (prev ? prev + ' ' : '') + "In my previous project, we decoupled client state using Zustand and handled server caching via TanStack Query for optimal performance.");
        setIsRecording(false);
      }, 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-3xl h-[82vh] flex flex-col rounded-2xl bg-white border border-slate-200 shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="px-5 py-3.5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-slate-900 text-sm">AI Technical Mock Screener</h3>
                <span className="px-2 py-0.5 text-[11px] font-semibold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse"></span> Live Screener
                </span>
              </div>
              <p className="text-[11px] text-slate-500">Target Role: {role}</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200 rounded-lg transition-colors cursor-pointer"
            title="Close Interview"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Messages Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-slate-50/50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex gap-2.5 max-w-[85%] ${
                msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto flex-row'
              }`}
            >
              <div
                className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'bg-blue-50 text-blue-600 border border-blue-200'
                }`}
              >
                {msg.role === 'user' ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>

              <div className="space-y-1">
                <div
                  className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-tr-none'
                      : 'bg-white text-slate-800 border border-slate-200 rounded-tl-none shadow-xs'
                  }`}
                >
                  <p className="whitespace-pre-line">{msg.content}</p>
                </div>
                <span className={`text-[10px] text-slate-400 block px-1 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                  {msg.timestamp}
                </span>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-2.5 max-w-[80%]">
              <div className="w-7 h-7 rounded-lg bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center shrink-0">
                <Bot className="w-3.5 h-3.5" />
              </div>
              <div className="p-3 rounded-2xl bg-white border border-slate-200 rounded-tl-none flex items-center gap-1.5 text-slate-500 text-xs">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-bounce"></span>
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-bounce [animation-delay:0.4s]"></span>
                <span className="ml-1.5 font-medium">Interviewer evaluating response...</span>
              </div>
            </div>
          )}

          {/* Score Report */}
          {interviewComplete && overallScore && (
            <div className="mt-4 p-5 rounded-2xl bg-white border border-blue-200 shadow-sm space-y-3 animate-in fade-in duration-200">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2">
                  <Award className="w-5 h-5 text-amber-500" />
                  <h4 className="font-bold text-slate-900 text-base">Interview Evaluation Rubric</h4>
                </div>
                <div className="px-2.5 py-0.5 bg-amber-50 text-amber-800 border border-amber-200 rounded-md text-xs font-bold">
                  Grade: {overallScore.overallGrade}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
                  <div className="text-xs text-slate-500 mb-0.5">Technical Depth</div>
                  <div className="text-xl font-bold text-blue-600">{overallScore.technicalAccuracy}%</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
                  <div className="text-xs text-slate-500 mb-0.5">Clarity & Comm</div>
                  <div className="text-xl font-bold text-emerald-600">{overallScore.communicationClarity}%</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
                  <div className="text-xs text-slate-500 mb-0.5">Problem Solving</div>
                  <div className="text-xl font-bold text-purple-600">{overallScore.problemSolving}%</div>
                </div>
              </div>

              <div>
                <h5 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">Feedback & Suggestions</h5>
                <ul className="space-y-1.5">
                  {overallScore.feedback.map((item, i) => (
                    <li key={i} className="text-xs text-slate-700 flex items-start gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Footer Input */}
        <div className="p-3.5 border-t border-slate-200 bg-white flex flex-col gap-1.5">
          {isRecording && (
            <div className="flex items-center gap-2 text-xs text-red-600 px-3 py-1 bg-red-50 border border-red-200 rounded-lg animate-pulse">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              Listening to microphone speech simulation... Click Mic again to stop.
            </div>
          )}

          <div className="flex items-center gap-2">
            <button
              onClick={toggleRecording}
              className={`p-2.5 rounded-xl border transition-all cursor-pointer ${
                isRecording
                  ? 'bg-red-50 border-red-300 text-red-600 animate-pulse'
                  : 'bg-slate-50 text-slate-600 border-slate-200 hover:text-slate-900 hover:bg-slate-100'
              }`}
              title="Voice recording simulation"
            >
              {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>

            <input
              type="text"
              className="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 text-xs sm:text-sm focus:bg-white focus:outline-none focus:border-blue-600"
              placeholder={interviewComplete ? "Interview finished! Feel free to ask any closing questions..." : "Type your technical response here..."}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            />

            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs sm:text-sm font-semibold rounded-xl flex items-center gap-1.5 transition-all shadow-xs cursor-pointer"
            >
              <span>Send</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default MockInterviewModal;
