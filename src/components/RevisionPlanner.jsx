import React, { useState } from 'react';
import { 
  Calendar, Clock, Sparkles, 
  Layers 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const REVISION_WEEKS = [
  {
    week: 1,
    title: "Core Foundations & Mental Models",
    hours: "12 Hours",
    spacedInterval: "Active Recall (Day 1 & Day 3)",
    tasks: [
      { id: 'w1-1', title: "Review Virtual DOM and component reconciliation mechanics", xp: 25 },
      { id: 'w1-2', title: "Implement 3 custom hooks with memoization (`useDebounce`, `useLocalStorage`)", xp: 25 },
      { id: 'w1-3', title: "Solve 5 algorithmic questions on Big-O time complexity", xp: 25 }
    ]
  },
  {
    week: 2,
    title: "Global State Management & Server Caching",
    hours: "14 Hours",
    spacedInterval: "Spaced Repetition (Day 7 Review)",
    tasks: [
      { id: 'w2-1', title: "Configure central Zustand store with persistent storage", xp: 25 },
      { id: 'w2-2', title: "Integrate TanStack Query for cache invalidation & optimistic updates", xp: 25 },
      { id: 'w2-3', title: "Build error boundary wrapper with fallback UI", xp: 25 }
    ]
  },
  {
    week: 3,
    title: "RAG Pipelines & ChromaDB Vector Grounding",
    hours: "15 Hours",
    spacedInterval: "Deep Recall (Day 14 Review)",
    tasks: [
      { id: 'w3-1', title: "Ingest PDF syllabus chunks with overlap sliding windows", xp: 25 },
      { id: 'w3-2', title: "Implement cosine similarity ranking against user query vectors", xp: 25 },
      { id: 'w3-3', title: "Audit prompt engineering templates for zero hallucination", xp: 25 }
    ]
  },
  {
    week: 4,
    title: "Kahoot Practice Arena & Mock Technical Screener",
    hours: "18 Hours",
    spacedInterval: "Final Mastery Simulation",
    tasks: [
      { id: 'w4-1', title: "Achieve >90% score on all syllabus Kahoot quizzes", xp: 50 },
      { id: 'w4-2', title: "Complete 3 AI Technical Mock Interviews with IBM Bob", xp: 50 },
      { id: 'w4-3', title: "Export final IBM SkillsBuild certification dossier", xp: 50 }
    ]
  }
];

const RevisionPlanner = ({ onAddXP }) => {
  const [examDate, setExamDate] = useState('2026-09-20');
  const [studyHours, setStudyHours] = useState(3);
  const [learningStyle, setLearningStyle] = useState('Hands-on Projects & Code');
  const [completedTasks, setCompletedTasks] = useState({});

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

  const totalTasksCount = REVISION_WEEKS.reduce((acc, w) => acc + w.tasks.length, 0);
  const completedCount = Object.values(completedTasks).filter(Boolean).length;
  const progressPct = Math.round((completedCount / totalTasksCount) * 100);

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      
      {/* Configuration Header */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-slate-900">Adaptive Revision Planner (SLLM)</h2>
              <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">
                Spaced Repetition
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Schedules revision intervals based on syllabus cognitive load.</p>
          </div>

          <div className="text-right">
            <div className="text-2xl font-extrabold text-emerald-600">{progressPct}%</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold">Plan Completed</div>
          </div>
        </div>

        {/* Inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-slate-100">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-blue-600" /> Target Exam Date
            </label>
            <input
              type="date"
              value={examDate}
              onChange={(e) => setExamDate(e.target.value)}
              className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-xs focus:bg-white focus:outline-none focus:border-blue-600"
            />
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between items-center text-xs font-semibold text-slate-700">
              <span className="flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-indigo-600" /> Daily Bandwidth
              </span>
              <span className="text-blue-600 font-bold">{studyHours} Hours/day</span>
            </div>
            <input
              type="range"
              min={1}
              max={8}
              value={studyHours}
              onChange={(e) => setStudyHours(Number(e.target.value))}
              className="w-full accent-blue-600"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-purple-600" /> Learning Mode
            </label>
            <select
              value={learningStyle}
              onChange={(e) => setLearningStyle(e.target.value)}
              className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-xs focus:bg-white focus:outline-none focus:border-blue-600"
            >
              <option>Hands-on Projects & Code</option>
              <option>Visual & Architectural Diagrams</option>
              <option>ELI10 Simple Analogies</option>
              <option>Deep Theory & Practice Tests</option>
            </select>
          </div>
        </div>
      </div>

      {/* Structured Milestones */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-600" />
          Weekly Milestones & Checklists
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
                    Week {w.week}: {w.hours}
                  </span>
                  <span className="text-[11px] text-amber-700 font-mono flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>{w.spacedInterval}</span>
                  </span>
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
