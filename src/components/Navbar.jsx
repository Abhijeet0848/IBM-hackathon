import React from 'react';
import { Flame, Award, Brain, Zap } from 'lucide-react';

const Navbar = ({ onOpenInterview, xp = 150, streak = 3, onHomeClick }) => {

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand */}
        <div 
          onClick={onHomeClick} 
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-xs group-hover:scale-105 transition-transform">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold tracking-tight text-slate-900 text-base sm:text-lg flex items-center gap-1.5">
                <span className="text-blue-600 font-extrabold tracking-wider text-sm bg-blue-50 border border-blue-200 px-1.5 py-0.5 rounded">IBM</span> 
                SkillsBuild <span className="text-slate-500 font-normal">| Study Buddy</span>
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium hidden sm:block">AI Personalized Learning & Career Copilot</p>
          </div>
        </div>

        {/* Gamification Stats */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-xl shadow-xs text-xs font-semibold">
            <span className="flex items-center gap-1 text-orange-600">
              <Flame className="w-4 h-4 text-orange-500 fill-orange-500 animate-pulse" />
              <span>{streak} Day Streak</span>
            </span>
            <span className="text-slate-300">|</span>
            <span className="flex items-center gap-1 text-purple-700">
              <Award className="w-4 h-4 text-purple-600" />
              <span>{xp} XP</span>
            </span>
          </div>

          <button
            onClick={onOpenInterview}
            className="hidden md:flex items-center gap-2 px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-xs transition-all hover:scale-[1.02] cursor-pointer"
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
