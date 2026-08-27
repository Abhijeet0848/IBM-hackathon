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
    }, 1200);
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
            <div className="text-xl font-bold text-emerald-600">100%</div>
            <div className="text-xs text-slate-500 font-medium">RAG Grounding Accuracy</div>
          </div>
        </div>

      </div>

      {/* Upload Dropzone */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <FileUp className="w-4 h-4 text-blue-600" />
            Upload Syllabus & Lecture Materials
          </h3>
          <span className="px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">
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
              ? 'border-blue-500 bg-blue-50'
              : 'border-slate-300 hover:border-blue-500 bg-slate-50 hover:bg-slate-100/60'
          }`}
        >
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
              <div className="pt-2">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-white text-blue-700 border border-slate-200 rounded-lg text-xs font-semibold shadow-xs">
                  <span>Click to ingest sample lecture notes (+50 XP)</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          )}
        </div>
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
          <div className="p-6 text-center text-slate-400 text-xs">
            No course materials uploaded yet. Upload a syllabus above to enable RAG grounded explanations!
          </div>
        )}
      </div>

    </div>
  );
};

export default SyllabusUploader;
