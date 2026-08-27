import React from 'react';
import { 
  ArrowRight, BrainCircuit, Sparkles, 
  Lightbulb, Trophy, Bot, Zap, ChevronRight 
} from 'lucide-react';


const LandingPage = ({ onStart, onOpenInterview }) => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-blue-600 selection:text-white">
      
      {/* Top Ambient Glows */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[350px] bg-gradient-to-br from-blue-600/15 via-indigo-600/10 to-transparent blur-3xl pointer-events-none -z-10"></div>
      <div className="fixed top-1/3 right-10 w-[400px] h-[300px] bg-purple-600/10 blur-3xl pointer-events-none -z-10"></div>

      {/* Header */}
      <header className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-xl sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 p-[1px] shadow-lg shadow-blue-500/25">
              <div className="w-full h-full bg-slate-950 rounded-[15px] flex items-center justify-center">
                <Bot className="w-5 h-5 text-blue-400" />
              </div>
            </div>
            <div className="font-extrabold text-white tracking-tight text-base sm:text-lg flex items-center gap-1.5">
              <span className="text-blue-500 font-extrabold bg-blue-500/10 border border-blue-500/20 px-1.5 py-0.5 rounded text-xs">IBM</span>
              Bob <span className="text-slate-400 font-normal text-sm">| AI Study Buddy</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onStart}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs sm:text-sm font-bold shadow-md shadow-blue-600/20 transition-all hover:scale-105 flex items-center gap-1.5"
            >
              <span>Meet IBM Bob</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-16 sm:py-24 text-center max-w-6xl mx-auto w-full">
        
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-8 shadow-inner animate-in fade-in slide-in-from-top-3 duration-500">
          <Sparkles className="w-3.5 h-3.5 text-blue-400 animate-spin [animation-duration:8s]" />
          <span>Personalized AI Learning Companion & LLM Tutor</span>
        </div>

        {/* Main Heading */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-slate-100 max-w-4xl leading-[1.15] mb-6">
          Every student learns differently. Meet <span className="gradient-text-ibm">IBM Bob</span>, your AI Study Buddy.
        </h1>

        {/* Subtitle */}
        <p className="text-slate-400 text-base sm:text-lg lg:text-xl max-w-2xl leading-relaxed mb-10">
          Upload your syllabus and course notes. Get simplified <strong>“Explain Like I’m 10”</strong> analogies, auto-generated <strong>Kahoot practice tests</strong>, adaptive <strong>revision roadmaps</strong>, and 24/7 grounded doubt resolution.
        </p>

        {/* Call to Actions */}
        <div className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto mb-16">
          <button
            onClick={onStart}
            className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-2xl text-base shadow-xl shadow-blue-600/30 transition-all hover:scale-[1.03] flex items-center justify-center gap-2 group"
          >
            <span>Start Learning with Bob</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>

          <button
            onClick={onOpenInterview}
            className="w-full sm:w-auto px-7 py-4 bg-slate-900/80 hover:bg-slate-800 border border-slate-700/80 text-slate-200 font-semibold rounded-2xl text-base transition-all hover:border-slate-600 flex items-center justify-center gap-2"
          >
            <Zap className="w-5 h-5 text-amber-400" />
            <span>Practice Technical Screener</span>
          </button>
        </div>

        {/* Metrics Counter */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-4xl mb-20 text-left">
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm">
            <div className="text-2xl sm:text-3xl font-extrabold text-amber-400 mb-0.5">ELI10</div>
            <div className="text-xs text-slate-400 font-medium">Simplified Analogies</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm">
            <div className="text-2xl sm:text-3xl font-extrabold text-purple-400 mb-0.5">Kahoot</div>
            <div className="text-xs text-slate-400 font-medium">Gamified Practice Tests</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm">
            <div className="text-2xl sm:text-3xl font-extrabold text-blue-400 mb-0.5">SLLM</div>
            <div className="text-xs text-slate-400 font-medium">Spaced Revision Plans</div>
          </div>
          <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-sm">
            <div className="text-2xl sm:text-3xl font-extrabold text-emerald-400 mb-0.5">24/7 RAG</div>
            <div className="text-xs text-slate-400 font-medium">Course Doc Doubt Solver</div>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full text-left">
          
          <div className="glass-panel-interactive p-6 rounded-2xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center mb-4">
                <Lightbulb className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-100 mb-2">“Explain Like I’m 10” Mode</h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-4">
                Demystify any complex theory into fun real-world metaphors, Lego castle analogies, and story adventures.
              </p>
            </div>
            <div className="flex items-center text-xs font-semibold text-amber-400 gap-1 mt-2">
              <span>Interactive Simplicity Slider</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div className="glass-panel-interactive p-6 rounded-2xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center mb-4">
                <Trophy className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-100 mb-2">Kahoot-Style Practice Tests</h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-4">
                Auto-generate 4-choice timed MCQ arenas directly from your uploaded syllabus notes with streak combos and leaderboards.
              </p>
            </div>
            <div className="flex items-center text-xs font-semibold text-purple-400 gap-1 mt-2">
              <span>Speed Timers & Multipliers</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </div>
          </div>

          <div className="glass-panel-interactive p-6 rounded-2xl flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mb-4">
                <Bot className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-100 mb-2">Doubt-Solving Chatbot</h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-4">
                Trained on your course notes via ChromaDB vector embeddings. Ask questions in natural language and receive grounded citations.
              </p>
            </div>
            <div className="flex items-center text-xs font-semibold text-blue-400 gap-1 mt-2">
              <span>Vector Grounded Citations</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </div>
          </div>

        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-8 bg-slate-950/90 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>© 2026 IBM Bob — AI Study Buddy & Personalized Learning Companion. Powered by IBM SkillsBuild.</p>
          <div className="flex items-center gap-6">
            <span className="hover:text-slate-400 cursor-pointer">Syllabus RAG</span>
            <span className="hover:text-slate-400 cursor-pointer">Kahoot Arena</span>
            <span className="hover:text-slate-400 cursor-pointer">ELI10 Engine</span>
          </div>
        </div>
      </footer>

    </div>
  );
};

export default LandingPage;
