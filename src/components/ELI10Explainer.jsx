import React, { useState } from 'react';
import { 
  Sparkles, Lightbulb, Volume2, 
  VolumeX, Copy, Check, Wand2, RefreshCw 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const SIMPLICITY_MODES = [
  { id: 'eli10', name: '👶 Like I’m 10', desc: 'Everyday metaphors & simple toys' },
  { id: 'story', name: '🧙 Story Adventure', desc: 'Hero’s journey narrative' },
  { id: 'highschool', name: '🎒 High School', desc: 'Structured logic & bullet points' },
  { id: 'professor', name: '🎓 University Level', desc: 'Rigorous definitions & math foundations' },
];

const ELI10Explainer = ({ onAddXP }) => {
  const [topicInput, setTopicInput] = useState('');
  const [selectedMode, setSelectedMode] = useState('eli10');
  const [currentResult, setCurrentResult] = useState(null);
  const [isSimplifying, setIsSimplifying] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const handleSimplify = () => {
    if (!topicInput.trim()) return;
    const targetTopic = topicInput.trim();
    setIsSimplifying(true);

    setTimeout(() => {
      setIsSimplifying(false);
      let simplifiedText = `Imagine ${targetTopic} as a friendly playground game where every participant has a specific rule to follow. When everyone works together, the system produces the expected outcome effortlessly!`;
      let analogyText = `A playground puzzle where each player takes their turn smoothly.`;
      let takeaway = `Breaks complex domain barriers into intuitive, bite-sized components.`;

      const tLower = targetTopic.toLowerCase();
      if (tLower.includes('rag') || tLower.includes('retrieval')) {
        simplifiedText = "Imagine taking an open-book exam! Instead of the AI guessing from pure memory, a smart librarian instantly flips to the exact page in your textbook and gives the AI the exact proof before answering!";
        analogyText = "An open-book exam with an instant superhero librarian.";
        takeaway = "Connects external textbook search directly to the AI to eliminate false guesses.";
      } else if (tLower.includes('neural') || tLower.includes('machine learning') || tLower.includes('ai')) {
        simplifiedText = "Think of a Neural Network like a team of detectives identifying mystery animals. The first checks colors, the second checks fur, and the third counts legs to confidently shout the answer!";
        analogyText = "A team of detectives solving clues together one layer at a time.";
        takeaway = "Layers of mathematical filters work together to recognize complex patterns.";
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
    }, 900);
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
      setTimeout(() => setIsPlayingAudio(false), 6000);
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
        
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <Wand2 className="w-4 h-4 text-blue-600" />
            Enter concept or question
          </label>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              className="flex-1 px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:bg-white focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
              placeholder="Type any difficult concept (e.g. Asynchronous event loops, Neural networks, Fourier transforms)..."
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
          <p className="text-xs text-slate-400">Type any concept in the box above and click "Explain It!"</p>
        </div>
      )}

    </div>
  );
};

export default ELI10Explainer;
