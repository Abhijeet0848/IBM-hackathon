import React, { useState } from 'react';
import { 
  Lightbulb, Trophy, Bot, Calendar, FileUp, 
  Flame, Award, PlayCircle 
} from 'lucide-react';

import ELI10Explainer from './ELI10Explainer';
import KahootQuiz from './KahootQuiz';
import DoubtSolverChat from './DoubtSolverChat';
import RevisionPlanner from './RevisionPlanner';
import SyllabusUploader from './SyllabusUploader';
import MockInterviewModal from './MockInterviewModal';

const Dashboard = () => {
  // Active Tab State: 'eli10' | 'kahoot' | 'doubts' | 'revision' | 'syllabus'
  const [activeTab, setActiveTab] = useState('eli10');
  const [showInterview, setShowInterview] = useState(false);

  // Gamification Global State
  const [studentXP, setStudentXP] = useState(320);
  const [studyStreak] = useState(4);

  const handleAddXP = (amount) => {
    setStudentXP(prev => prev + amount);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-blue-600 selection:text-white">
      
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-xl sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            
            {/* Brand */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 p-[1px] shadow-lg shadow-blue-500/20">
                <div className="w-full h-full bg-slate-950 rounded-[15px] flex items-center justify-center">
                  <Bot className="w-5 h-5 text-blue-400" />
                </div>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-white tracking-tight text-base sm:text-lg">
                    IBM Bob <span className="text-blue-400 font-normal">| AI Study Buddy</span>
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold">
                    ● Online
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 font-medium hidden sm:block">Personalized AI Learning Companion & LLM Tutor</p>
              </div>
            </div>

            {/* Gamification Stats & Mock Screener CTA */}
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-xl shadow-inner text-xs font-semibold">
                <span className="flex items-center gap-1 text-orange-400">
                  <Flame className="w-4 h-4 text-orange-500 fill-orange-500 animate-pulse" />
                  <span>{studyStreak} Day Streak</span>
                </span>
                <span className="text-slate-700">|</span>
                <span className="flex items-center gap-1 text-purple-400">
                  <Award className="w-4 h-4 text-purple-400" />
                  <span>{studentXP} XP</span>
                </span>
              </div>

              <button
                onClick={() => setShowInterview(true)}
                className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs sm:text-sm font-semibold shadow-md shadow-blue-600/20 transition-all hover:scale-105"
              >
                <PlayCircle className="w-4 h-4" />
                <span className="hidden sm:inline">Practice Interview</span>
                <span className="sm:hidden">Interview</span>
              </button>
            </div>

          </div>

          {/* Navigation Tabs */}
          <div className="flex overflow-x-auto space-x-1 py-2 border-t border-slate-800/60 no-scrollbar">
            
            <button
              onClick={() => setActiveTab('eli10')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
                activeTab === 'eli10'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Lightbulb className="w-4 h-4" />
              <span>“Explain Like I’m 10”</span>
            </button>

            <button
              onClick={() => setActiveTab('kahoot')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
                activeTab === 'kahoot'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Trophy className="w-4 h-4" />
              <span>Kahoot Practice Tests</span>
            </button>

            <button
              onClick={() => setActiveTab('doubts')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
                activeTab === 'doubts'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Bot className="w-4 h-4" />
              <span>Doubt-Solving Chatbot</span>
            </button>

            <button
              onClick={() => setActiveTab('revision')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
                activeTab === 'revision'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Calendar className="w-4 h-4" />
              <span>Revision & Study Plans</span>
            </button>

            <button
              onClick={() => setActiveTab('syllabus')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shrink-0 ${
                activeTab === 'syllabus'
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <FileUp className="w-4 h-4" />
              <span>Upload Syllabus / Notes</span>
            </button>

          </div>

        </div>
      </header>

      {/* Main Tab Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {activeTab === 'eli10' && <ELI10Explainer onAddXP={handleAddXP} />}
        {activeTab === 'kahoot' && <KahootQuiz onAddXP={handleAddXP} currentStreak={studyStreak} />}
        {activeTab === 'doubts' && <DoubtSolverChat onAddXP={handleAddXP} />}
        {activeTab === 'revision' && <RevisionPlanner onAddXP={handleAddXP} />}
        {activeTab === 'syllabus' && <SyllabusUploader onAddXP={handleAddXP} />}
      </main>

      {/* Mock Technical Screener Modal */}
      {showInterview && (
        <MockInterviewModal
          onClose={() => setShowInterview(false)}
          initialRole="Computer Science & AI Engineer"
        />
      )}

    </div>
  );
};

export default Dashboard;
