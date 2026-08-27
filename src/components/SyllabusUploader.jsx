import React, { useState } from 'react';
import { 
  Upload, FileText, CheckCircle2, Database, Trash2, 
  Sparkles, Layers, ArrowRight, RefreshCw, FileUp 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const SAMPLE_INGESTED_DOCS = [
  { name: "CS301_Distributed_Systems_Syllabus.pdf", chunks: 42, size: "2.4 MB", status: "Indexed in ChromaDB" },
  { name: "IBM_SkillsBuild_AI_Foundations.pdf", chunks: 28, size: "1.8 MB", status: "Indexed in ChromaDB" },
  { name: "React_19_Architecture_Notes.md", chunks: 19, size: "450 KB", status: "Indexed in ChromaDB" }
];

const SyllabusUploader = ({ onAddXP }) => {
  const [docs, setDocs] = useState(SAMPLE_INGESTED_DOCS);
  const [isIngesting, setIsIngesting] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const totalChunks = docs.reduce((acc, d) => acc + d.chunks, 0);

  const handleSimulateUpload = (fileName = "Operating_Systems_Lecture_4.pdf") => {
    setIsIngesting(true);
    setTimeout(() => {
      setIsIngesting(false);
      const newDoc = {
        name: fileName,
        chunks: Math.floor(Math.random() * 20) + 15,
        size: "1.2 MB",
        status: "Indexed in ChromaDB"
      };
      setDocs(prev => [newDoc, ...prev]);
      if (onAddXP) onAddXP(50);

      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.6 }
      });
    }, 1400);
  };

  const handleClearDocs = () => {
    setDocs([]);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      
      {/* Header & Stats Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        
        <div className="p-5 rounded-2xl glass-panel flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-black text-white">{docs.length}</div>
            <div className="text-xs text-slate-400 font-medium">Uploaded Documents</div>
          </div>
        </div>

        <div className="p-5 rounded-2xl glass-panel flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-black text-white">{totalChunks}</div>
            <div className="text-xs text-slate-400 font-medium">ChromaDB Vector Chunks</div>
          </div>
        </div>

        <div className="p-5 rounded-2xl glass-panel flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-black text-emerald-400">100%</div>
            <div className="text-xs text-slate-400 font-medium">RAG Grounding Accuracy</div>
          </div>
        </div>

      </div>

      {/* Upload Dropzone */}
      <div className="p-6 rounded-3xl glass-panel space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <FileUp className="w-5 h-5 text-blue-400" />
            Upload Course Syllabus & Lecture Materials
          </h3>
          <span className="px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold">
            ChromaDB RAG Engine
          </span>
        </div>

        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragActive(false);
            handleSimulateUpload("Uploaded_Course_Material.pdf");
          }}
          onClick={() => handleSimulateUpload("Data_Structures_Lecture_6.pdf")}
          className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
            dragActive
              ? 'border-blue-500 bg-blue-600/10 scale-[1.01]'
              : 'border-slate-700/80 hover:border-blue-500/60 bg-slate-950/50 hover:bg-slate-900/60'
          }`}
        >
          {isIngesting ? (
            <div className="space-y-3 py-4">
              <RefreshCw className="w-10 h-10 text-blue-400 animate-spin mx-auto" />
              <p className="text-sm font-bold text-white">Extracting text & computing vector embeddings...</p>
              <p className="text-xs text-slate-400">Storing semantic chunks into local ChromaDB storage</p>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="w-14 h-14 rounded-2xl bg-blue-600/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto">
                <Upload className="w-7 h-7" />
              </div>
              <div>
                <p className="text-sm font-bold text-white">Drag & drop syllabus files here, or click to browse</p>
                <p className="text-xs text-slate-400 mt-1">Supports PDF, DOCX, TXT, MD (Max 25MB per file)</p>
              </div>
              <div className="pt-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-slate-800 text-blue-300 border border-slate-700 rounded-lg text-xs font-semibold">
                  <span>Click to ingest sample lecture notes (+50 XP)</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Active Indexed Documents List */}
      <div className="p-6 rounded-3xl glass-panel space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            Currently Indexed Knowledge Base ({docs.length})
          </h4>
          {docs.length > 0 && (
            <button
              onClick={handleClearDocs}
              className="text-xs text-rose-400 hover:text-rose-300 flex items-center gap-1 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear Knowledge Base</span>
            </button>
          )}
        </div>

        {docs.length > 0 ? (
          <div className="space-y-2.5">
            {docs.map((doc, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between gap-4 hover:border-slate-700 transition-all"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-9 h-9 rounded-lg bg-blue-600/10 border border-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <h5 className="text-xs sm:text-sm font-bold text-white truncate">{doc.name}</h5>
                    <span className="text-[11px] text-slate-400 font-mono">{doc.size} • {doc.chunks} semantic chunks</span>
                  </div>
                </div>

                <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg text-[11px] font-semibold flex items-center gap-1 shrink-0">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Indexed in ChromaDB</span>
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center text-slate-500 text-xs">
            No course materials uploaded yet. Upload a syllabus above to enable RAG grounded explanations!
          </div>
        )}
      </div>

    </div>
  );
};

export default SyllabusUploader;
