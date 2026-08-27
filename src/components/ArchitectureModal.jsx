import React from 'react';
import { 
  X, Layers, Database, Bot, Calendar, Trophy, 
  Sparkles, FileText, ArrowDown, ArrowRight, CheckCircle2 
} from 'lucide-react';

const ArchitectureModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl bg-white border border-slate-200 shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-xs">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base">AI Study Buddy System Architecture</h3>
              <p className="text-xs text-slate-500">Gamified & Personalized Learning Pipeline Dataflow</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-200 rounded-lg transition-colors cursor-pointer"
            title="Close Architecture"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Architecture Diagram */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50">
          
          {/* Top User Entry */}
          <div className="flex justify-center">
            <div className="px-6 py-2.5 bg-slate-900 text-white rounded-xl font-bold text-xs shadow-xs flex items-center gap-2">
              <span>👤 Student Learner</span>
            </div>
          </div>

          <div className="flex justify-center">
            <ArrowDown className="w-4 h-4 text-slate-400" />
          </div>

          {/* Layer 1: Syllabus Ingestion & Personalization (SLLM and Paths) */}
          <div className="p-6 rounded-2xl bg-white border border-blue-200 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-blue-700 flex items-center gap-1.5">
                <Calendar className="w-4 h-4" /> Layer 1: Syllabus Ingestion & Personalization (SLLM & Paths)
              </span>
              <span className="text-[10px] bg-blue-50 text-blue-700 border border-blue-200 px-2 py-0.5 rounded font-mono">
                SLLM Core
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                <span className="font-bold text-slate-900 block">Input 1: Days / Free Hours</span>
                <p className="text-slate-500">Configures daily study commitment (1-8 hrs) and target exam date.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                <span className="font-bold text-slate-900 block">Input 2: Document Parsing (PDF/Text)</span>
                <p className="text-slate-500">Extracts syllabus topics and indexes text chunks for vector search.</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-200 text-xs space-y-1">
                <span className="font-bold text-blue-900 block">Syllabus Analyzer (Topic Sequencing)</span>
                <p className="text-blue-800">Breaks syllabus into logical prerequisite chains and learning modules.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-200 text-xs space-y-1">
                <span className="font-bold text-blue-900 block">Personalized Schedule Generator (IBM Bob LLM)</span>
                <p className="text-blue-800">Generates optimal spaced repetition calendar with milestone checklists.</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900 text-white text-xs font-mono flex items-center justify-between">
              <span>Personalized Study Plan (JSON Store)</span>
              <span className="text-emerald-400">✓ Context Ready</span>
            </div>
          </div>

          <div className="flex justify-center">
            <ArrowDown className="w-4 h-4 text-slate-400" />
          </div>

          {/* Layer 2: Knowledge Management & Retrieval */}
          <div className="p-6 rounded-2xl bg-white border border-indigo-200 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-700 flex items-center gap-1.5">
                <Database className="w-4 h-4" /> Layer 2: Knowledge Management & Retrieval
              </span>
              <span className="text-[10px] bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded font-mono">
                ChromaDB Vector DB
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                <span className="font-bold text-slate-900 block">Frontend UI (Direct Student Query)</span>
                <p className="text-slate-500">Receives student questions with active topic context from study plan.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                <span className="font-bold text-slate-900 block">Vector Database (Embeddings)</span>
                <p className="text-slate-500">ChromaDB semantic index storing chunk embeddings with cosine search.</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-indigo-50 border border-indigo-200 text-xs flex items-center justify-between">
              <div>
                <span className="font-bold text-indigo-950 block">RAG Pipeline + IBM Bob / LLM Content Engine</span>
                <span className="text-indigo-800">Grounds explanations in course materials with 0 hallucination.</span>
              </div>
              <Bot className="w-5 h-5 text-indigo-600 shrink-0" />
            </div>
          </div>

          <div className="flex justify-center">
            <ArrowDown className="w-4 h-4 text-slate-400" />
          </div>

          {/* Layer 3: Gamification & Delivery */}
          <div className="p-6 rounded-2xl bg-white border border-emerald-200 shadow-xs space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1.5">
                <Trophy className="w-4 h-4" /> Layer 3: Gamification & Delivery
              </span>
              <span className="text-[10px] bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded font-mono">
                Delivery Loop
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3.5 rounded-xl bg-emerald-50/50 border border-emerald-200 text-xs space-y-1">
                <span className="font-bold text-emerald-950 block">Enriched Content Delivery</span>
                <p className="text-emerald-800">Core concepts, historical origins, and future research / industry applications.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-amber-50/50 border border-amber-200 text-xs space-y-1">
                <span className="font-bold text-amber-950 block">Smart Reminders</span>
                <p className="text-amber-800">Motivational quotes and scheduled spaced repetition alerts.</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-purple-50/60 border border-purple-200 text-xs space-y-1">
              <span className="font-bold text-purple-950 block">Gamification Engine</span>
              <p className="text-purple-800">Student XP points, study streak multipliers, and Kahoot-style timed quizzes.</p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900 text-white text-xs font-bold text-center">
              Frontend UI (Student Dashboard & Interactive Learning Companion)
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-white flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-xs cursor-pointer"
          >
            Close Architecture
          </button>
        </div>

      </div>
    </div>
  );
};

export default ArchitectureModal;
