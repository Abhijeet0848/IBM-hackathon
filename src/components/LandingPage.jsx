import React from 'react';
import { 
  ArrowRight, Sparkles, Lightbulb, Trophy, 
  Bot, ChevronRight, FileUp, Calendar, ArrowUpRight 
} from 'lucide-react';



const LandingPage = ({ onStart, onOpenInterview }) => {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      
      {/* Clean Light Header */}
      <header className="border-b border-slate-200 bg-white/90 backdrop-blur-md sticky top-0 z-30 shadow-xs">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-sm">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="font-bold text-slate-900 tracking-tight text-base sm:text-lg flex items-center gap-1.5">
                <span className="text-blue-600 font-extrabold bg-blue-50 border border-blue-200 px-1.5 py-0.5 rounded text-xs">IBM</span>
                Bob <span className="text-slate-500 font-normal text-sm">| AI Study Buddy</span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">Personalized Learning Companion</p>
            </div>
          </div>

          {/* Header Action Buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => onStart('eli10')}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs sm:text-sm font-semibold shadow-sm transition-all hover:scale-102 flex items-center gap-1.5 cursor-pointer"
            >
              <span>Open Study Workspace</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-16 sm:py-20 text-center max-w-5xl mx-auto w-full">
        
        {/* Simple Badge */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-6 shadow-xs">
          <Sparkles className="w-3.5 h-3.5 text-blue-600" />
          <span>IBM SkillsBuild & AI Tutoring Companion</span>
        </div>

        {/* Hero Heading */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 max-w-3xl leading-tight mb-5">
          Learn anything faster with <span className="text-blue-600">IBM Bob</span>, your personal AI tutor.
        </h1>

        {/* Subtitle */}
        <p className="text-slate-600 text-base sm:text-lg max-w-2xl leading-relaxed mb-8">
          Upload your syllabus and notes to unlock simplified <strong>“Explain Like I’m 10”</strong> analogies, interactive <strong>Kahoot practice tests</strong>, adaptive <strong>revision schedules</strong>, and 24/7 grounded doubt resolution.
        </p>

        {/* Action CTAs */}
        <div className="flex items-center justify-center gap-3 w-full sm:w-auto mb-14">
          <button
            onClick={() => onStart('eli10')}
            className="w-full sm:w-auto px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-sm shadow-md hover:shadow-lg transition-all hover:scale-102 flex items-center justify-center gap-2 cursor-pointer"
          >
            <span>Start Learning with Bob</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>


        {/* Key Features Section */}
        <div className="w-full text-left space-y-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-500">
              Explore Learning Modules
            </h2>
            <span className="text-xs text-blue-600 font-medium">Click any card to start</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            
            {/* Card 1: ELI10 */}
            <div 
              onClick={() => onStart('eli10')}
              className="bg-white p-6 rounded-2xl border border-slate-200 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                  <Lightbulb className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-1.5">“Explain Like I’m 10” Mode</h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed mb-4">
                  Turn heavy, confusing topics into simple real-world metaphors, Lego castle models, and story adventures.
                </p>
              </div>
              <div className="flex items-center text-xs font-semibold text-blue-600 gap-1 mt-2">
                <span>Try ELI10 Explainer</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>

            {/* Card 2: Kahoot Quiz */}
            <div 
              onClick={() => onStart('kahoot')}
              className="bg-white p-6 rounded-2xl border border-slate-200 hover:border-purple-400 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-purple-50 border border-purple-200 text-purple-600 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                  <Trophy className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-1.5">Kahoot-Style Practice Tests</h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed mb-4">
                  Test your knowledge with 4-choice timed MCQ arenas, combo streak multipliers, and instant explanations.
                </p>
              </div>
              <div className="flex items-center text-xs font-semibold text-purple-600 gap-1 mt-2">
                <span>Launch Kahoot Arena</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>

            {/* Card 3: Doubt Solver */}
            <div 
              onClick={() => onStart('doubts')}
              className="bg-white p-6 rounded-2xl border border-slate-200 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                  <Bot className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-1.5">Doubt-Solving Chatbot</h3>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed mb-4">
                  24/7 AI tutor grounded in your course notes via ChromaDB. Ask doubts in natural language and receive citations.
                </p>
              </div>
              <div className="flex items-center text-xs font-semibold text-blue-600 gap-1 mt-2">
                <span>Ask IBM Bob</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>

          </div>

          {/* Secondary Quick Links Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            
            <div
              onClick={() => onStart('revision')}
              className="bg-white p-4 rounded-xl border border-slate-200 hover:border-emerald-400 hover:shadow-xs transition-all cursor-pointer flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
                  <Calendar className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">Adaptive Revision & Spaced Repetition</h4>
                  <p className="text-[11px] text-slate-500">Day 1, 3, 7, 14 recall schedules with progress checklist</p>
                </div>
              </div>
              <ArrowUpRight className="w-4 h-4 text-slate-400" />
            </div>

            <div
              onClick={() => onStart('syllabus')}
              className="bg-white p-4 rounded-xl border border-slate-200 hover:border-cyan-400 hover:shadow-xs transition-all cursor-pointer flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-cyan-50 text-cyan-600 flex items-center justify-center">
                  <FileUp className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">Upload Syllabus / Notes (PDF / TXT)</h4>
                  <p className="text-[11px] text-slate-500">ChromaDB chunk vector ingestion & indexing</p>
                </div>
              </div>
              <ArrowUpRight className="w-4 h-4 text-slate-400" />
            </div>

          </div>
        </div>

      </main>

      {/* Clean Light Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500 mt-auto">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>© 2026 IBM Bob — AI Study Buddy & Personalized Learning Companion.</p>
          <div className="flex items-center gap-5 font-medium">
            <span onClick={() => onStart('eli10')} className="hover:text-blue-600 cursor-pointer">ELI10 Explainer</span>
            <span onClick={() => onStart('kahoot')} className="hover:text-blue-600 cursor-pointer">Kahoot Practice</span>
            <span onClick={() => onStart('doubts')} className="hover:text-blue-600 cursor-pointer">Doubt Chatbot</span>
            <span onClick={() => onStart('syllabus')} className="hover:text-blue-600 cursor-pointer">Syllabus Ingestion</span>
          </div>
        </div>
      </footer>

    </div>
  );
};

export default LandingPage;
