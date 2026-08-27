import React, { useState } from 'react';
import { 
  Calendar, Clock, CheckCircle2, 
  Layers, Sparkles, RefreshCw 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const REVISION_WEEKS = [
  {
    week: 1,
    title: "Phase 1: Core Fundamentals & Concept Review",
    hours: "10 Hours",
    tasks: [
      { id: 'w1-1', title: "Review core architecture and key component patterns", xp: 25 },
      { id: 'w1-2', title: "Practice 3 practical coding implementations with memoization", xp: 25 },
      { id: 'w1-3', title: "Solve Big-O time and space complexity exercises", xp: 25 }
    ]
  },
  {
    week: 2,
    title: "Phase 2: Deep Dive & State Architecture",
    hours: "12 Hours",
    tasks: [
      { id: 'w2-1', title: "Set up central state management and asynchronous data fetching", xp: 25 },
      { id: 'w2-2', title: "Implement error handling and optimistic UI updates", xp: 25 },
      { id: 'w2-3', title: "Audit edge case handling and network boundaries", xp: 25 }
    ]
  },
  {
    week: 3,
    title: "Phase 3: RAG Vectors & Knowledge Grounding",
    hours: "14 Hours",
    tasks: [
      { id: 'w3-1', title: "Index syllabus documents and test semantic retrieval", xp: 25 },
      { id: 'w3-2', title: "Review topic summaries and eliminate weak knowledge gaps", xp: 25 },
      { id: 'w3-3', title: "Validate prompt responses against course lecture notes", xp: 25 }
    ]
  },
  {
    week: 4,
    title: "Phase 4: Kahoot Practice & Final Review",
    hours: "15 Hours",
    tasks: [
      { id: 'w4-1', title: "Score >90% on timed Kahoot practice tests", xp: 50 },
      { id: 'w4-2', title: "Resolve remaining course doubts with IBM Bob", xp: 50 },
      { id: 'w4-3', title: "Complete comprehensive syllabus mastery checklist", xp: 50 }
    ]
  }
];

const RevisionPlanner = ({ onAddXP }) => {
  const [selectedDuration, setSelectedDuration] = useState('14'); // '7' | '14' | '30'
  const [studyHours, setStudyHours] = useState('2');
  const [completedTasks, setCompletedTasks] = useState({});
  const [isGenerating, setIsGenerating] = useState(false);

  const toggleTask = (taskId, xpVal = 25) => {
    setCompletedTasks(prev => {
      const isNowDone = !prev[taskId];
      const updated = { ...prev, [taskId]: isNowDone };
      if (isNowDone) {
        if (onAddXP) onAddXP(xpVal);
        confetti({
          particleCount: 40,
          spread: 50,
          origin: { y: 0.7 }
        });
      }
      return updated;
    });
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setIsGenerating(false);
      setCompletedTasks({});
      if (onAddXP) onAddXP(40);
      confetti({
        particleCount: 60,
        spread: 70,
        origin: { y: 0.6 }
      });
    }, 700);
  };

  const totalTasksCount = REVISION_WEEKS.reduce((acc, w) => acc + w.tasks.length, 0);
  const completedCount = Object.values(completedTasks).filter(Boolean).length;
  const progressPct = Math.round((completedCount / totalTasksCount) * 100);

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      
      {/* Clean Simple Header */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-5">
        
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Revision & Study Planner</h2>
            <p className="text-xs text-slate-500">Plan your syllabus revision with spaced repetition milestones.</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-32 bg-slate-100 h-2.5 rounded-full overflow-hidden">
              <div 
                className="bg-emerald-500 h-full transition-all duration-300 rounded-full"
                style={{ width: `${progressPct}%` }}
              ></div>
            </div>
            <span className="text-xs font-bold text-slate-700">{progressPct}% Done</span>
          </div>
        </div>

        {/* Simple Clean Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-slate-100">
          
          {/* Target Duration */}
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-blue-600" /> Target Duration
            </label>
            <div className="grid grid-cols-3 gap-1.5">
              {['7', '14', '30'].map((d) => (
                <button
                  key={d}
                  onClick={() => setSelectedDuration(d)}
                  className={`py-2 rounded-lg text-xs font-semibold border transition-all cursor-pointer ${
                    selectedDuration === d
                      ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {d} Days
                </button>
              ))}
            </div>
          </div>

          {/* Daily Study Hours */}
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-indigo-600" /> Daily Study Time
            </label>
            <div className="grid grid-cols-3 gap-1.5">
              {['1', '2', '3+'].map((h) => (
                <button
                  key={h}
                  onClick={() => setStudyHours(h)}
                  className={`py-2 rounded-lg text-xs font-semibold border transition-all cursor-pointer ${
                    studyHours === h
                      ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                      : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  {h} {h === '3+' ? 'Hours' : 'Hr'}
                </button>
              ))}
            </div>
          </div>

          {/* Generate Button */}
          <div className="space-y-1 flex flex-col justify-end">
            <button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs sm:text-sm font-semibold transition-all shadow-xs flex items-center justify-center gap-1.5 cursor-pointer"
            >
              {isGenerating ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Planning...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Generate Plan</span>
                </>
              )}
            </button>
          </div>

        </div>
      </div>

      {/* Structured Milestones */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" />
          Study Checklist ({selectedDuration}-Day Schedule)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {REVISION_WEEKS.map((w) => {
            const weekDoneCount = w.tasks.filter(t => completedTasks[t.id]).length;
            const isWeekAllDone = weekDoneCount === w.tasks.length;

            return (
              <div
                key={w.week}
                className={`p-5 rounded-2xl bg-white border transition-all ${
                  isWeekAllDone
                    ? 'border-emerald-300 bg-emerald-50/20'
                    : 'border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2.5 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 rounded-lg text-xs font-bold">
                    Week {w.week} ({w.hours})
                  </span>
                  {isWeekAllDone && (
                    <span className="text-xs font-bold text-emerald-600 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Complete
                    </span>
                  )}
                </div>

                <h4 className="text-sm font-bold text-slate-900 mb-3">{w.title}</h4>

                <div className="pt-2 border-t border-slate-100 space-y-2">
                  {w.tasks.map((task) => (
                    <label
                      key={task.id}
                      className="flex items-start gap-2.5 text-xs text-slate-700 cursor-pointer p-1.5 rounded-lg hover:bg-slate-50 transition-all"
                    >
                      <input
                        type="checkbox"
                        checked={!!completedTasks[task.id]}
                        onChange={() => toggleTask(task.id, task.xp)}
                        className="mt-0.5 rounded border-slate-300 text-blue-600 focus:ring-0 cursor-pointer"
                      />
                      <div className="flex-1">
                        <span className={completedTasks[task.id] ? 'line-through text-slate-400' : ''}>
                          {task.title}
                        </span>
                        <span className="text-[10px] text-purple-700 ml-1.5 font-mono">+{task.xp} XP</span>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
};

export default RevisionPlanner;
