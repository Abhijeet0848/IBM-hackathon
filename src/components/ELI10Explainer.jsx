import React, { useState } from 'react';
import { 
  Sparkles, Lightbulb, Volume2, 
  VolumeX, Copy, Check, Wand2, RefreshCw, BookOpen, Tag 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const SIMPLICITY_MODES = [
  { id: 'eli10', name: '👶 Like I’m 10', desc: 'Everyday metaphors & simple toys' },
  { id: 'story', name: '🧙 Story Adventure', desc: 'Hero’s journey narrative' },
  { id: 'highschool', name: '🎒 High School', desc: 'Structured logic & bullet points' },
  { id: 'professor', name: '🎓 University Level', desc: 'Rigorous definitions & math foundations' },
];

const ELI10Explainer = ({ onAddXP, extractedSyllabus }) => {
  const [topicInput, setTopicInput] = useState('');
  const [selectedMode, setSelectedMode] = useState('eli10');
  const [currentResult, setCurrentResult] = useState(null);
  const [isSimplifying, setIsSimplifying] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const handleSimplify = (overrideTopic) => {
    const targetTopic = (overrideTopic || topicInput).trim();
    if (!targetTopic) return;
    if (overrideTopic) setTopicInput(overrideTopic);
    setIsSimplifying(true);

    setTimeout(() => {
      setIsSimplifying(false);
      const tLower = targetTopic.toLowerCase();
      let simplifiedText = "";
      let analogyText = "";
      let takeaway = "";

      if (tLower.includes('nuclear') || tLower.includes('binding') || tLower.includes('mass defect')) {
        simplifiedText = "Imagine the nucleus of an atom like a group of friendly magnets squeezed super tightly into a tiny ball! When they snap together, a tiny bit of their weight turns into pure superpower glue (Binding Energy) to keep them from flying apart.";
        analogyText = "A super-glue magnetic hug that releases energy when it locks in place.";
        takeaway = "Mass defect is converted into binding energy according to Einstein's E = mc².";
      } else if (tLower.includes('decay') || tLower.includes('radioactiv') || tLower.includes('half-life')) {
        simplifiedText = "Think of radioactive atoms like popcorn kernels in a hot pan! You can't predict which exact kernel will pop next, but you know that after exactly 2 minutes (one half-life), exactly half of all the kernels will have popped!";
        analogyText = "A pan of popcorn where exactly 50% pop every fixed round of time.";
        takeaway = "Radioactivity is random individually, but follows exact exponential decay as a group.";
      } else if (tLower.includes('fission') || tLower.includes('fusion') || tLower.includes('reactor')) {
        simplifiedText = "Fission is like shooting a bowling ball at a giant water balloon until it splits in two and throws out smaller balls. Fusion is the opposite: smashing two tiny droplets together so hard that they merge into one big droplet, powering the Sun!";
        analogyText = "Fission splits a giant balloon; Fusion smashes droplets together to build a sun.";
        takeaway = "Both fission and fusion convert mass difference into vast amounts of usable energy.";
      } else if (tLower.includes('rag') || tLower.includes('retrieval')) {
        simplifiedText = "Imagine taking an open-book exam! Instead of the AI guessing from pure memory, a smart librarian instantly flips to the exact page in your textbook and gives the AI the exact proof before answering!";
        analogyText = "An open-book exam with an instant superhero librarian.";
        takeaway = "Connects external textbook search directly to the AI to eliminate false guesses.";
      } else {
        simplifiedText = `Imagine ${targetTopic} as a specialized team system where every rule ensures stability and precision. When applied to real-world problems, it transforms confusing complexities into manageable, predictable steps.`;
        analogyText = `A finely tuned clockwork mechanism where each gear performs its role smoothly.`;
        takeaway = `Breaks down complex domain concepts into intuitive, verified fundamentals.`;
      }

      setCurrentResult({
        topic: targetTopic,
        eli10: simplifiedText,
        analogy: analogyText,
        keyTakeaway: takeaway
      });

      if (onAddXP) onAddXP(30);

      confetti({
        particleCount: 40,
        spread: 50,
        origin: { y: 0.6 }
      });
    }, 700);
  };

  const handleCopy = () => {
    if (currentResult) {
      navigator.clipboard.writeText(currentResult.eli10);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const toggleAudio = () => {
    setIsPlayingAudio(!isPlayingAudio);
    if (!isPlayingAudio) {
      setTimeout(() => setIsPlayingAudio(false), 5000);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      
      {/* Top Banner Card */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600">
            <Lightbulb className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-slate-900">“Explain Like I’m 10” Learning Assistant</h2>
              <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-xs font-semibold">
                ELI10 Mode
              </span>
            </div>
            <p className="text-xs text-slate-500">Turn complex syllabus concepts into simple everyday analogies.</p>
          </div>
        </div>
      </div>

      {/* Input & Mode Configuration */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-5">
        
        {/* Extracted Syllabus Quick Topic Chips */}
        {extractedSyllabus?.extractedTopics && extractedSyllabus.extractedTopics.length > 0 && (
          <div className="p-3 rounded-xl bg-amber-50/60 border border-amber-200/80 space-y-2">
            <div className="flex items-center gap-1.5 text-xs font-bold text-amber-900">
              <BookOpen className="w-3.5 h-3.5 text-amber-700" />
              <span>Suggested topics from {extractedSyllabus.title}:</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {extractedSyllabus.extractedTopics.map((topic, i) => (
                <button
                  key={i}
                  onClick={() => handleSimplify(topic)}
                  className="px-2.5 py-1 bg-white hover:bg-amber-100/70 border border-amber-300 text-amber-900 rounded-lg text-xs font-medium transition-colors cursor-pointer flex items-center gap-1 shadow-2xs"
                >
                  <Tag className="w-2.5 h-2.5 text-amber-600" />
                  <span>{topic}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <Wand2 className="w-4 h-4 text-blue-600" />
            Enter concept or question
          </label>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              className="flex-1 px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:bg-white focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
              placeholder="Type any difficult concept (e.g. Binding Energy, Radioactive Half-Life, Gamow Barrier)..."
              value={topicInput}
              onChange={(e) => setTopicInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSimplify()}
            />
            <button
              onClick={() => handleSimplify()}
              disabled={isSimplifying || !topicInput.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold rounded-xl text-xs sm:text-sm flex items-center justify-center gap-2 shadow-xs transition-all cursor-pointer"
            >
              {isSimplifying ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Simplifying...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Explain It!</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Simplicity Mode Selector */}
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Explanation Style
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {SIMPLICITY_MODES.map((mode) => (
              <button
                key={mode.id}
                onClick={() => setSelectedMode(mode.id)}
                className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                  selectedMode === mode.id
                    ? 'bg-blue-50 border-blue-500 text-blue-900 shadow-xs'
                    : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100 hover:border-slate-300'
                }`}
              >
                <div className="font-bold text-xs sm:text-sm text-slate-900 mb-0.5">{mode.name}</div>
                <div className="text-[11px] text-slate-500 leading-tight">{mode.desc}</div>
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* Output Card */}
      {currentResult ? (
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4 animate-in fade-in duration-200">
          
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">Concept Summary</span>
              <h3 className="text-lg font-bold text-slate-900 mt-0.5">{currentResult.topic}</h3>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={toggleAudio}
                className={`px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                  isPlayingAudio
                    ? 'bg-red-50 border-red-300 text-red-600 animate-pulse'
                    : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                }`}
                title="Listen to audio simulation"
              >
                {isPlayingAudio ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
                <span>{isPlayingAudio ? "Speaking..." : "Listen"}</span>
              </button>

              <button
                onClick={handleCopy}
                className="px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-700 hover:bg-slate-100 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
                title="Copy text"
              >
                {isCopied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{isCopied ? "Copied!" : "Copy"}</span>
              </button>
            </div>
          </div>

          {/* Analogy Box */}
          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start gap-3">
            <span className="text-xl shrink-0">💡</span>
            <div>
              <span className="text-xs font-bold text-amber-800 uppercase tracking-wider block">The 10-Year-Old Metaphor</span>
              <p className="text-sm font-semibold text-amber-950 mt-0.5">{currentResult.analogy}</p>
            </div>
          </div>

          {/* Explanation Body */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm leading-relaxed">
            <p className="whitespace-pre-line">{currentResult.eli10}</p>
          </div>

          {/* Key Takeaway */}
          <div className="flex items-center gap-2 text-xs text-slate-600 pt-1">
            <Sparkles className="w-4 h-4 text-blue-600 shrink-0" />
            <span><strong className="text-slate-900">Key Takeaway:</strong> {currentResult.keyTakeaway}</span>
          </div>

        </div>
      ) : (
        <div className="p-8 rounded-2xl bg-white border border-dashed border-slate-300 text-center text-slate-400 text-sm space-y-1">
          <Lightbulb className="w-8 h-8 mx-auto text-slate-300 mb-2" />
          <p className="font-semibold text-slate-600">No concept entered yet</p>
          <p className="text-xs text-slate-400">Type any concept in the box above or click a topic chip to generate an instant explanation</p>
        </div>
      )}

    </div>
  );
};

export default ELI10Explainer;
