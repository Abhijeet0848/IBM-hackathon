import React, { useState, useEffect } from 'react';
import { 
  Upload, FileText, CheckCircle2, Database, Trash2, 
  Sparkles, ArrowRight, RefreshCw, FileUp, 
  Calendar, Lightbulb, Bot, Trophy, BookOpen, Eye, EyeOff, Tag
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { parseUploadedDocument } from '../utils/pdfExtractor';

const SyllabusUploader = ({ 
  onAddXP, 
  onNavigateTab, 
  extractedSyllabus, 
  onSyllabusExtracted 
}) => {
  const [docs, setDocs] = useState(extractedSyllabus ? [extractedSyllabus] : []);
  const [isIngesting, setIsIngesting] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [pasteMode, setPasteMode] = useState(false);
  const [pastedText, setPastedText] = useState('');
  const [showRawText, setShowRawText] = useState(false);

  useEffect(() => {
    if (extractedSyllabus) {
      setDocs([extractedSyllabus]);
    }
  }, [extractedSyllabus]);

  const totalChunks = docs.reduce((acc, d) => acc + (d.totalChunks || d.chunks || 20), 0);

  const processFile = async (file) => {
    setIsIngesting(true);
    try {
      const parsed = await parseUploadedDocument(file);
      setDocs(prev => [parsed, ...prev.filter(d => d.fileName !== parsed.fileName)]);
      if (onSyllabusExtracted) onSyllabusExtracted(parsed);
      if (onAddXP) onAddXP(60);

      confetti({
        particleCount: 60,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (err) {
      console.error("Extraction error:", err);
    } finally {
      setIsIngesting(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) processFile(file);
  };

  const handlePasteSubmit = () => {
    if (!pastedText.trim()) return;
    const fakeFile = new File([pastedText], "Course_Syllabus_Notes.txt", { type: "text/plain" });
    processFile(fakeFile);
    setPastedText('');
    setPasteMode(false);
  };

  const handleSimulateSample = (sampleName = "Nuclear_Physics_&_Quantum_Structure.pdf") => {
    const sampleText = `Unit 1: Nuclear Structure, Binding Energy & Liquid Drop Model
- Atomic Nucleus properties: charge, radius, mass defect, binding energy curve
- Semi-empirical mass formula & nuclear stability N/Z ratio
- Liquid Drop Model and Bohr-Wheeler theory of nuclear fission

Unit 2: Radioactivity, Alpha, Beta & Gamma Decay
- Law of radioactive decay, half-life, mean lifetime, radioactive equilibrium
- Alpha decay: Gamow theory of barrier penetration and Geiger-Nuttall law
- Beta decay: continuous beta spectrum, Pauli neutrino hypothesis, Fermi theory
- Gamma decay: internal conversion and nuclear isomerism

Unit 3: Nuclear Reactions & Fission/Fusion Dynamics
- Conservation laws in nuclear reactions, Q-value and threshold energy
- Nuclear fission: prompt and delayed neutrons, four-factor formula, nuclear reactors
- Thermonuclear fusion: p-p chain, CNO cycle, stellar nucleosynthesis, Tokamak confinement

Unit 4: Particle Detectors, Accelerators & Standard Model
- Ionization chambers, Proportional counters, GM counter dead time and quenching
- Cyclotron, Synchrotron, and Linear Accelerators
- Elementary particles: Leptons, Hadrons, Baryons, Mesons, and Quark model`;

    const sampleBlob = new Blob([sampleText], { type: "text/plain" });
    const sampleFile = new File([sampleBlob], sampleName, { type: "text/plain" });
    processFile(sampleFile);
  };

  const handleClearDocs = () => {
    setDocs([]);
    if (onSyllabusExtracted) onSyllabusExtracted(null);
  };

  const currentExtracted = docs[0];

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

      {/* Upload Dropzone Card */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <FileUp className="w-4 h-4 text-blue-600" />
            Upload Syllabus PDF or Course Notes
          </h3>
          <button
            onClick={() => setPasteMode(!pasteMode)}
            className="text-xs text-blue-600 hover:text-blue-700 font-semibold cursor-pointer"
          >
            {pasteMode ? "← Switch to File Upload" : "Or Paste Syllabus Text"}
          </button>
        </div>

        {!pasteMode ? (
          <label
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDragLeave={() => setDragActive(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragActive(false);
              const file = e.dataTransfer.files?.[0];
              if (file) processFile(file);
            }}
            className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer block ${
              dragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-slate-300 hover:border-blue-500 bg-slate-50 hover:bg-slate-100/60'
            }`}
          >
            <input
              type="file"
              accept=".pdf,.txt,.md,.docx,.csv"
              onChange={handleFileUpload}
              className="hidden"
            />

            {isIngesting ? (
              <div className="space-y-2 py-4">
                <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto" />
                <p className="text-sm font-bold text-slate-900">Extracting content and parsing syllabus structure...</p>
                <p className="text-xs text-slate-500">Extracting pages, generating vector embeddings & grounding topics</p>
              </div>
            ) : (
              <div className="space-y-2">
                <div className="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center mx-auto">
                  <Upload className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-bold text-slate-900">Drag & drop your PDF or notes here, or click to browse</p>
                  <p className="text-xs text-slate-500 mt-0.5">Full PDF text parser active (supports multi-page PDFs, TXT, MD)</p>
                </div>
                <div className="pt-2">
                  <span
                    onClick={(e) => {
                      e.preventDefault();
                      handleSimulateSample();
                    }}
                    className="inline-flex items-center gap-1.5 px-3 py-1 bg-white text-blue-700 border border-slate-200 rounded-lg text-xs font-semibold shadow-xs hover:border-blue-300"
                  >
                    <span>Click to test sample Nuclear Physics syllabus (+60 XP)</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </div>
            )}
          </label>
        ) : (
          <div className="space-y-3">
            <textarea
              rows={5}
              className="w-full p-3.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 text-xs sm:text-sm focus:bg-white focus:outline-none focus:border-blue-600 font-mono"
              placeholder="Paste course syllabus, unit modules, or textbook outline here..."
              value={pastedText}
              onChange={(e) => setPastedText(e.target.value)}
            ></textarea>
            <button
              onClick={handlePasteSubmit}
              disabled={!pastedText.trim()}
              className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-xl text-xs sm:text-sm font-semibold shadow-xs transition-all cursor-pointer"
            >
              Parse & Ingest Syllabus Text
            </button>
          </div>
        )}
      </div>

      {/* Extracted Content & Structure Box (When PDF/Doc is Uploaded) */}
      {currentExtracted && (
        <div className="p-6 rounded-2xl bg-white border border-blue-200 shadow-sm space-y-4 animate-in fade-in duration-200">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-600 flex items-center justify-center shrink-0">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div>
                <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider block">
                  Content Extracted from Document
                </span>
                <h4 className="text-sm sm:text-base font-bold text-slate-900 truncate">
                  {currentExtracted.fileName || currentExtracted.name}
                </h4>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowRawText(!showRawText)}
                className="text-xs text-slate-600 hover:text-blue-600 border border-slate-200 px-2.5 py-1 rounded-lg flex items-center gap-1 cursor-pointer bg-slate-50"
              >
                {showRawText ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                <span>{showRawText ? "Hide Text" : "View Extracted Text"}</span>
              </button>
              <button
                onClick={handleClearDocs}
                className="text-xs text-rose-600 hover:text-rose-700 border border-rose-100 px-2.5 py-1 rounded-lg flex items-center gap-1 cursor-pointer bg-rose-50/50"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Clear</span>
              </button>
            </div>
          </div>

          {/* Extracted Topics Tags */}
          {currentExtracted.extractedTopics && currentExtracted.extractedTopics.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                <Tag className="w-3 h-3 text-blue-600" /> Extracted Syllabus Topics:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {currentExtracted.extractedTopics.map((topic, i) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg text-xs font-medium"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Extracted Content Overview */}
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 space-y-1">
            <div className="font-bold text-slate-900 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-blue-600" />
              <span>Extracted Summary Snippet:</span>
            </div>
            <p className="text-slate-600 line-clamp-3 leading-relaxed font-mono text-[11px]">
              {currentExtracted.extractedSnippet || `Extracted ${currentExtracted.totalChunks || 24} semantic vector chunks from syllabus.`}
            </p>
          </div>

          {/* Full Extracted Text Preview Drawer */}
          {showRawText && currentExtracted.rawText && (
            <div className="p-4 rounded-xl bg-slate-900 text-slate-100 text-xs font-mono space-y-2 max-h-64 overflow-y-auto">
              <div className="flex items-center justify-between text-slate-400 border-b border-slate-800 pb-2 text-[11px]">
                <span>Full Raw Extracted Document Text</span>
                <span>{currentExtracted.rawText.length} characters parsed</span>
              </div>
              <pre className="whitespace-pre-wrap leading-relaxed text-slate-300">
                {currentExtracted.rawText}
              </pre>
            </div>
          )}

          {/* Instant Generation Actions */}
          <div className="space-y-2 pt-1">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Generate from Uploaded Syllabus:
            </span>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              
              <button
                onClick={() => onNavigateTab && onNavigateTab('revision')}
                className="p-3.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
              >
                <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                  <Calendar className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h5 className="text-xs sm:text-sm font-bold text-slate-900 truncate">1. Generate Study Plan</h5>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:translate-x-1 group-hover:text-blue-600" />
                  </div>
                  <p className="text-[11px] text-slate-500">Populates weekly milestones from parsed modules.</p>
                </div>
              </button>

              <button
                onClick={() => onNavigateTab && onNavigateTab('eli10')}
                className="p-3.5 rounded-xl border border-slate-200 hover:border-amber-500 hover:bg-amber-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
              >
                <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
                  <Lightbulb className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h5 className="text-xs sm:text-sm font-bold text-slate-900 truncate">2. Explain Topics (ELI10)</h5>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:translate-x-1 group-hover:text-amber-600" />
                  </div>
                  <p className="text-[11px] text-slate-500">Simplifies extracted concepts into analogies.</p>
                </div>
              </button>

              <button
                onClick={() => onNavigateTab && onNavigateTab('doubts')}
                className="p-3.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
              >
                <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h5 className="text-xs sm:text-sm font-bold text-slate-900 truncate">3. Ask Course Doubts</h5>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:translate-x-1 group-hover:text-blue-600" />
                  </div>
                  <p className="text-[11px] text-slate-500">24/7 AI tutor grounded in your PDF chunks.</p>
                </div>
              </button>

              <button
                onClick={() => onNavigateTab && onNavigateTab('kahoot')}
                className="p-3.5 rounded-xl border border-slate-200 hover:border-purple-500 hover:bg-purple-50/40 text-left transition-all group flex items-start gap-3 cursor-pointer shadow-xs"
              >
                <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center shrink-0">
                  <Trophy className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h5 className="text-xs sm:text-sm font-bold text-slate-900 truncate">4. Auto-Generate Quiz</h5>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:translate-x-1 group-hover:text-purple-600" />
                  </div>
                  <p className="text-[11px] text-slate-500">Timed 4-choice practice tests from this syllabus.</p>
                </div>
              </button>

            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default SyllabusUploader;
