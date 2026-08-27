import React from 'react';
import { Flame, Award, Brain, Zap } from 'lucide-react';

const Navbar = ({ onOpenInterview, xp = 150, streak = 3, onHomeClick }) => {

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand */}
        <div 
          onClick={onHomeClick} 
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 p-[1px] shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center">
              <Brain className="w-5 h-5 text-blue-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold tracking-tight text-white text-base sm:text-lg flex items-center gap-1.5">
                <span className="text-blue-500 font-extrabold tracking-wider text-sm bg-blue-500/10 border border-blue-500/20 px-1.5 py-0.5 rounded">IBM</span> 
                SkillsBuild <span className="text-slate-400 font-normal">| Study Buddy</span>
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium hidden sm:block">AI Personalized Learning & Career Copilot</p>
          </div>
        </div>

        {/* Gamification Stats */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-xl shadow-inner text-xs font-semibold">
            <span className="flex items-center gap-1 text-amber-400">
              <Flame className="w-4 h-4 text-orange-500 fill-orange-500 animate-pulse" />
              <span>{streak} Day Streak</span>
            </span>
            <span className="text-slate-600">|</span>
            <span className="flex items-center gap-1 text-purple-400">
              <Award className="w-4 h-4 text-purple-400" />
              <span>{xp} XP</span>
            </span>
          </div>

          <button
            onClick={onOpenInterview}
            className="hidden md:flex items-center gap-2 px-3.5 py-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-blue-600/25 transition-all hover:scale-[1.02]"
          >
            <Zap className="w-3.5 h-3.5" />
            <span>Mock Interview</span>
          </button>
        </div>

      </div>
    </header>
  );
};

export default Navbar;
