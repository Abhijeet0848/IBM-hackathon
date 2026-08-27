import React, { useState } from 'react';
import { 
  Lightbulb, Trophy, Bot, Calendar, FileUp, 
  Flame, Award, Home 
} from 'lucide-react';
import ELI10Explainer from './ELI10Explainer';
import KahootQuiz from './KahootQuiz';
import DoubtSolverChat from './DoubtSolverChat';
import RevisionPlanner from './RevisionPlanner';
import SyllabusUploader from './SyllabusUploader';

const Dashboard = ({ initialTab = 'eli10', onHomeClick }) => {
  const [activeTab, setActiveTab] = useState(initialTab);

  // Gamification Global State
  const [studentXP, setStudentXP] = useState(320);
  const [studyStreak] = useState(4);

  const handleAddXP = (amount) => {
    setStudentXP(prev => prev + amount);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      
      {/* Clean Light Header Navigation */}
      <header className="border-b border-slate-200 bg-white/95 backdrop-blur-md sticky top-0 z-30 shadow-xs">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          
          <div className="flex items-center justify-between h-16">
            {/* Brand / Home Toggle */}
            <div 
              onClick={onHomeClick}
              className="flex items-center gap-3 cursor-pointer group"
              title="Return to Home Overview"
            >
              <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-xs">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <div className="font-bold text-slate-900 tracking-tight text-base flex items-center gap-1.5">
                  <span className="text-blue-600 font-extrabold text-xs bg-blue-50 border border-blue-200 px-1.5 py-0.5 rounded">IBM</span>
                  Bob <span className="text-slate-500 font-normal text-sm">| Study Buddy</span>
                </div>
              </div>
            </div>

            {/* Quick Actions & Stats */}
            <div className="flex items-center gap-2 sm:gap-3">
              <button
                onClick={onHomeClick}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-all cursor-pointer"
              >
                <Home className="w-3.5 h-3.5" />
                <span>Home</span>
              </button>

              <div className="flex items-center gap-2 bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-1 text-orange-600">
                  <Flame className="w-3.5 h-3.5 fill-orange-500 text-orange-500" />
                  <span>{studyStreak}d Streak</span>
                </span>
                <span className="text-slate-300">|</span>
                <span className="flex items-center gap-1 text-purple-700">
                  <Award className="w-3.5 h-3.5 text-purple-600" />
                  <span>{studentXP} XP</span>
                </span>
              </div>
            </div>
          </div>

          {/* Clean Light Tab Navigation */}
          <div className="flex overflow-x-auto space-x-1 py-2 border-t border-slate-100 no-scrollbar">
            <button
              onClick={() => setActiveTab('eli10')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all shrink-0 cursor-pointer ${
                activeTab === 'eli10'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Lightbulb className="w-4 h-4" />
              <span>“Explain Like I’m 10”</span>
            </button>

            <button
              onClick={() => setActiveTab('kahoot')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all shrink-0 cursor-pointer ${
                activeTab === 'kahoot'
                  ? 'bg-purple-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Trophy className="w-4 h-4" />
              <span>Kahoot Practice Tests</span>
            </button>

            <button
              onClick={() => setActiveTab('doubts')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all shrink-0 cursor-pointer ${
                activeTab === 'doubts'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Bot className="w-4 h-4" />
              <span>Doubt-Solving Chatbot</span>
            </button>

            <button
              onClick={() => setActiveTab('revision')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all shrink-0 cursor-pointer ${
                activeTab === 'revision'
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Calendar className="w-4 h-4" />
              <span>Revision & Study Plans</span>
            </button>

            <button
              onClick={() => setActiveTab('syllabus')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-semibold transition-all shrink-0 cursor-pointer ${
                activeTab === 'syllabus'
                  ? 'bg-cyan-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <FileUp className="w-4 h-4" />
              <span>Upload Syllabus / Notes</span>
            </button>
          </div>

        </div>
      </header>

      {/* Main Tab Area */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8 flex-1 w-full">
        {activeTab === 'eli10' && <ELI10Explainer onAddXP={handleAddXP} />}
        {activeTab === 'kahoot' && <KahootQuiz onAddXP={handleAddXP} />}
        {activeTab === 'doubts' && <DoubtSolverChat onAddXP={handleAddXP} />}
        {activeTab === 'revision' && <RevisionPlanner onAddXP={handleAddXP} />}
        {activeTab === 'syllabus' && <SyllabusUploader onAddXP={handleAddXP} />}
      </main>

    </div>
  );
};

export default Dashboard;
