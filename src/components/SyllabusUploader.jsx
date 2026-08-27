import React, { useState } from 'react';
import { 
  Upload, FileText, CheckCircle2, Database, Trash2, 
  Sparkles, Layers, ArrowRight, RefreshCw, FileUp, 
  Calendar, Lightbulb, Bot, Trophy 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const SyllabusUploader = ({ onAddXP, onNavigateTab }) => {
  const [docs, setDocs] = useState([]);
  const [isIngesting, setIsIngesting] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const totalChunks = docs.reduce((acc, d) => acc + d.chunks, 0);

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsIngesting(true);
    setTimeout(() => {
      setIsIngesting(false);
      const newDoc = {
        name: file.name,
        chunks: Math.floor(Math.random() * 20) + 14,
        size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
        status: "Indexed in ChromaDB"
      };
      setDocs(prev => [newDoc, ...prev]);
      if (onAddXP) onAddXP(50);

      confetti({
        particleCount: 60,
        spread: 70,
        origin: { y: 0.6 }
      });
    }, 1100);
  };

  const handleSimulateDrop = (fileName = "Computer_Science_Syllabus.pdf") => {
    setIsIngesting(true);
    setTimeout(() => {
      setIsIngesting(false);
      const newDoc = {
        name: fileName,
        chunks: 18,
        size: "1.4 MB",
        status: "Indexed in ChromaDB"
      };
      setDocs(prev => [newDoc, ...prev]);
      if (onAddXP) onAddXP(50);

      confetti({
        particleCount: 60,
        spread: 70,
        origin: { y: 0.6 }
      });
    }, 1100);
  };

  const handleClearDocs = () => {
    setDocs([]);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      
      {/* Stats Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        
        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center gap-4">
          <div className="w-11 h-11 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600 shrink-0">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-900">{docs.length}</div>
            <div className="text-xs text-slate-500 font-medium">Uploaded Documents</div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center gap-4">
          <div className="w-11 h-11 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600 shrink-0">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-900">{totalChunks}</div>
            <div className="text-xs text-slate-500 font-medium">ChromaDB Vector Chunks</div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center gap-4">
          <div className="w-11 h-11 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xl font-bold text-emerald-600">{docs.length > 0 ? "100%" : "0%"}</div>
            <div className="text-xs text-slate-500 font-medium">RAG Grounding Ready</div>
          </div>
        </div>

      </div>

      {/* Upload Dropzone */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <FileUp className="w-4 h-4 text-blue-600" />
            Upload Syllabus & Lecture Notes
          </h3>
          <span className="px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">
            ChromaDB RAG Engine
          </span>
        </div>

        <label
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragActive(false);
            handleSimulateDrop(e.dataTransfer.files?.[0]?.name || "Uploaded_Syllabus.pdf");
          }}
          className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer block ${
            dragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-slate-300 hover:border-blue-500 bg-slate-50 hover:bg-slate-100/60'
          }`}
        >
          <input
            type="file"
            accept=".pdf,.txt,.md,.docx"
            onChange={handleFileUpload}
            className="hidden"
          />

          {isIngesting ? (
            <div className="space-y-2 py-3">
              <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto" />
              <p className="text-sm font-bold text-slate-900">Extracting text & computing vector embeddings...</p>
              <p className="text-xs text-slate-500">Storing semantic chunks into ChromaDB</p>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center mx-auto">
                <Upload className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-bold text-slate-900">Drag & drop syllabus files here, or click to browse</p>
                <p className="text-xs text-slate-500 mt-0.5">Supports PDF, DOCX, TXT, MD (Max 25MB)</p>
              </div>
            </div>
          )}
        </label>
      </div>

      {/* Document List */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-600" />
            Currently Indexed Materials ({docs.length})
          </h4>
          {docs.length > 0 && (
            <button
              onClick={handleClearDocs}
              className="text-xs text-rose-600 hover:text-rose-700 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear Vector Index</span>
            </button>
          )}
        </div>

        {docs.length > 0 ? (
          <div className="space-y-2">
            {docs.map((doc, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <h5 className="text-xs sm:text-sm font-bold text-slate-900 truncate">{doc.name}</h5>
                    <span className="text-[11px] text-slate-500">{doc.size} • {doc.chunks} semantic chunks</span>
                  </div>
                </div>

                <span className="px-2.5 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md text-[11px] font-semibold flex items-center gap-1 shrink-0">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="hidden sm:inline">Indexed in ChromaDB</span>
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center text-slate-400 text-xs border border-dashed border-slate-200 rounded-xl">
            No course materials uploaded yet. Upload a syllabus above to start indexing course concepts.
          </div>
        )}
      </div>

      {/* Generation Options: Appears When Syllabus is Uploaded */}
      {docs.length > 0 && (
        <div className="p-6 rounded-2xl bg-white border border-blue-200 shadow-sm space-y-4 animate-in fade-in duration-200">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4" /> Syllabus Ingested Successfully
              </span>
              <h3 className="text-base font-bold text-slate-900 mt-0.5">What would you like IBM Bob to generate?</h3>
            </div>
            <span className="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold">
              Ready to Generate
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
            
            {/* Option 1: Study Plan */}
            <button
              onClick={() => onNavigateTab && onNavigateTab('revision')}
              className="p-4 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
            >
              <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <Calendar className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">1. Generate Revision & Study Plan</h4>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-blue-600 transition-all" />
                </div>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">
                  Sequences syllabus topics into an adaptive spaced repetition schedule based on your target date.
                </p>
              </div>
            </button>

            {/* Option 2: ELI10 Breakdowns */}
            <button
              onClick={() => onNavigateTab && onNavigateTab('eli10')}
              className="p-4 rounded-xl border border-slate-200 hover:border-amber-500 hover:bg-amber-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
            >
              <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <Lightbulb className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">2. Generate ELI10 Concept Metaphors</h4>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-amber-600 transition-all" />
                </div>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">
                  Simplifies complex syllabus topics into 10-year-old intuitive analogies and mental models.
                </p>
              </div>
            </button>

            {/* Option 3: Doubt Solver */}
            <button
              onClick={() => onNavigateTab && onNavigateTab('doubts')}
              className="p-4 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
            >
              <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <Bot className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">3. Ask Doubts with RAG Citations</h4>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-blue-600 transition-all" />
                </div>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">
                  Ask natural language questions grounded directly in your newly uploaded course text chunks.
                </p>
              </div>
            </button>

            {/* Option 4: Kahoot Practice Test */}
            <button
              onClick={() => onNavigateTab && onNavigateTab('kahoot')}
              className="p-4 rounded-xl border border-slate-200 hover:border-purple-500 hover:bg-purple-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
            >
              <div className="w-10 h-10 rounded-xl bg-purple-50 border border-purple-200 text-purple-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                <Trophy className="w-5 h-5" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs sm:text-sm font-bold text-slate-900">4. Auto-Generate Kahoot Practice Test</h4>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 group-hover:text-purple-600 transition-all" />
                </div>
                <p className="text-[11px] text-slate-500 mt-0.5 leading-snug">
                  Creates timed 4-choice practice quizzes from the uploaded syllabus with combo multipliers.
                </p>
              </div>
            </button>

          </div>
        </div>
      )}

    </div>
  );
};

export default SyllabusUploader;
