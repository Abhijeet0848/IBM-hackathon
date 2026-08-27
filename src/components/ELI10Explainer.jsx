import React, { useState } from 'react';
import { 
  Sparkles, Lightbulb, Volume2, 
  VolumeX, Copy, Check, Wand2, RefreshCw 
} from 'lucide-react';
import confetti from 'canvas-confetti';


const SIMPLICITY_MODES = [
  { id: 'eli10', name: '👶 Like I’m 10', desc: 'Fun metaphors, real-world toys & simple language' },
  { id: 'story', name: '🧙 Story / Adventure', desc: 'Explains concept through a hero’s journey' },
  { id: 'highschool', name: '🎒 High School', desc: 'Clear diagrams, direct logic & structured bullet points' },
  { id: 'professor', name: '🎓 University Deep-Dive', desc: 'Rigorous definitions, math foundations & technical nuances' },
];

const PRESET_TOPICS = [
  {
    topic: "Retrieval-Augmented Generation (RAG)",
    eli10: "Imagine you're taking an open-book exam! A regular AI tries to answer everything from pure memory (which can make it guess or hallucinate). But RAG gives the AI a superpower: whenever you ask a question, a little librarian instantly flips to the exact page in your textbook, highlights the proof, and hands it to the AI to answer with 100% accuracy!",
    analogy: "An open-book exam with an instant superhero librarian.",
    keyTakeaway: "Connects external textbook search directly to the AI to eliminate false guesses."
  },
  {
    topic: "Neural Networks & Machine Learning",
    eli10: "Think of a Neural Network like a team of detectives identifying mystery animals. The first detective only looks at colors. The second checks if it has fur or scales. The third counts legs. By combining all their small clues together, they can confidently shout: 'That’s a Golden Retriever puppy!'",
    analogy: "A team of detectives solving clues together one layer at a time.",
    keyTakeaway: "Layers of simple mathematical filters work together to recognize complex patterns."
  },
  {
    topic: "Dynamic Programming & Memoization",
    eli10: "If I write '1 + 1 + 1 + 1' on a chalkboard, you count and say '4'. If I add one more '+ 1' at the end, do you start counting from the beginning again? No! You remember it was 4, add 1, and say '5'. That is Dynamic Programming—remembering previous work so you never do it twice!",
    analogy: "Remembering your previous math answer instead of recalculating from zero.",
    keyTakeaway: "Cache intermediate sub-problem results to turn slow exponential tasks into lightning fast algorithms."
  }
];

const ELI10Explainer = ({ onAddXP }) => {
  const [topicInput, setTopicInput] = useState('');
  const [selectedMode, setSelectedMode] = useState('eli10');
  const [currentResult, setCurrentResult] = useState(PRESET_TOPICS[0]);
  const [isSimplifying, setIsSimplifying] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const handleSimplify = (topicOverride) => {
    const targetTopic = topicOverride || topicInput || PRESET_TOPICS[0].topic;
    setIsSimplifying(true);

    setTimeout(() => {
      setIsSimplifying(false);
      const match = PRESET_TOPICS.find(t => t.topic.toLowerCase().includes(targetTopic.toLowerCase())) || {
        topic: targetTopic,
        eli10: `Imagine ${targetTopic} as a giant playground game where every participant has a specific rule to follow. When everything works in harmony, the system produces the expected outcome effortlessly without getting confused!`,
        analogy: `A friendly playground puzzle where everyone plays their exact turn.`,
        keyTakeaway: `Breaks complex domain barriers into intuitive, bite-sized components.`
      };

      setCurrentResult(match);
      if (onAddXP) onAddXP(30);

      confetti({
        particleCount: 40,
        spread: 50,
        origin: { y: 0.6 }
      });
    }, 1100);
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
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      
      {/* Header Banner */}
      <div className="p-6 rounded-3xl glass-panel bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/40 border border-blue-500/20 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Lightbulb className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg sm:text-xl font-bold text-white">IBM Bob's "Explain Like I'm 10" Learning Assistant</h2>
              <span className="px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-semibold">
                ELI10 Engine
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">Turn heavy, complex syllabus topics into crystal-clear everyday analogies.</p>
          </div>
        </div>

        {/* Quick Topic Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-2">
          <span className="text-xs text-slate-400 font-semibold">Try sample topics:</span>
          {PRESET_TOPICS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => {
                setTopicInput(p.topic);
                handleSimplify(p.topic);
              }}
              className="px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-blue-500/50 text-slate-300 hover:text-white text-xs font-medium transition-all"
            >
              {p.topic}
            </button>
          ))}
        </div>
      </div>

      {/* Input & Simplicity Controls */}
      <div className="p-6 rounded-3xl glass-panel space-y-5">
        
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Wand2 className="w-4 h-4 text-blue-400" />
            Enter any difficult concept or paste textbook excerpt
          </label>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              className="flex-1 px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-2xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500"
              placeholder="e.g. Asynchronous event loops, Fourier transforms, Polymorphism..."
              value={topicInput}
              onChange={(e) => setTopicInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSimplify()}
            />
            <button
              onClick={() => handleSimplify()}
              disabled={isSimplifying}
              className="px-6 py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 text-white font-bold rounded-2xl text-xs sm:text-sm flex items-center justify-center gap-2 shadow-lg shadow-blue-600/20 transition-all hover:scale-105"
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
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Select Explanation Style
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {SIMPLICITY_MODES.map((mode) => (
              <button
                key={mode.id}
                onClick={() => setSelectedMode(mode.id)}
                className={`p-3 rounded-2xl border text-left transition-all ${
                  selectedMode === mode.id
                    ? 'bg-blue-600/20 border-blue-500 text-blue-300 shadow-md shadow-blue-500/10'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                <div className="font-bold text-xs sm:text-sm text-slate-200 mb-1">{mode.name}</div>
                <div className="text-[11px] text-slate-500 line-clamp-2 leading-tight">{mode.desc}</div>
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* Explanation Output Card */}
      {currentResult && (
        <div className="p-8 rounded-3xl glass-panel bg-gradient-to-b from-slate-900/90 to-slate-950 border border-slate-800 shadow-2xl space-y-6 animate-in fade-in duration-300">
          
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <span className="text-[11px] font-bold text-blue-400 uppercase tracking-wider">Concept Breakdown</span>
              <h3 className="text-xl font-black text-white mt-0.5">{currentResult.topic}</h3>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={toggleAudio}
                className={`p-2.5 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-all ${
                  isPlayingAudio
                    ? 'bg-red-500/20 border-red-500/40 text-red-400 animate-pulse'
                    : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
                }`}
                title="Listen to Bob's Voice"
              >
                {isPlayingAudio ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                <span>{isPlayingAudio ? "Speaking..." : "Listen"}</span>
              </button>

              <button
                onClick={handleCopy}
                className="p-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-all"
                title="Copy to notes"
              >
                {isCopied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                <span>{isCopied ? "Copied!" : "Copy"}</span>
              </button>
            </div>
          </div>

          {/* Analogy Pill */}
          <div className="p-4 rounded-2xl bg-amber-950/30 border border-amber-500/30 flex items-start gap-3">
            <span className="text-xl shrink-0">💡</span>
            <div>
              <span className="text-xs font-bold text-amber-300 uppercase tracking-wider block">The 10-Year-Old Metaphor</span>
              <p className="text-sm font-semibold text-slate-200 mt-0.5">{currentResult.analogy}</p>
            </div>
          </div>

          {/* Full Simplified Text */}
          <div className="p-6 rounded-2xl bg-slate-950/80 border border-slate-800/80 text-slate-200 text-sm sm:text-base leading-relaxed space-y-4">
            <p className="whitespace-pre-line">{currentResult.eli10}</p>
          </div>

          {/* Key Takeaway */}
          <div className="flex items-center gap-2 text-xs text-slate-400 pt-2">
            <Sparkles className="w-4 h-4 text-blue-400 shrink-0" />
            <span><strong className="text-slate-200">Key Takeaway:</strong> {currentResult.keyTakeaway}</span>
          </div>

        </div>
      )}

    </div>
  );
};

export default ELI10Explainer;
