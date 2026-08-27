import React, { useState, useEffect, useCallback } from 'react';
import { 
  RefreshCw, Check, Flame, Clock, 
  Sparkles, Trophy, ArrowRight 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const KAHOOT_COLORS = [
  { bg: 'bg-red-600 hover:bg-red-500', border: 'border-red-500', shape: '▲', shapeColor: 'text-white' },
  { bg: 'bg-blue-600 hover:bg-blue-500', border: 'border-blue-500', shape: '◆', shapeColor: 'text-white' },
  { bg: 'bg-amber-500 hover:bg-amber-400', border: 'border-amber-400', shape: '●', shapeColor: 'text-white' },
  { bg: 'bg-emerald-600 hover:bg-emerald-500', border: 'border-emerald-500', shape: '◼', shapeColor: 'text-white' },
];

const SAMPLE_QUESTIONS = [
  {
    id: 1,
    topic: "Computer Science & React",
    question: "What is the Virtual DOM and why does React use it?",
    options: [
      "A complete copy of the browser operating system",
      "A lightweight JavaScript representation of the real DOM to minimize slow browser re-paints",
      "A database stored in the user's cookies",
      "A CSS engine that compiles Tailwind styles"
    ],
    correctIndex: 1,
    eli10: "Think of the real DOM like building a Lego castle. Instead of tearing down the entire castle every time you want to change one window, the Virtual DOM plans which single Lego brick to swap in seconds!",
    points: 1000
  },
  {
    id: 2,
    topic: "AI & Vector Search",
    question: "How does IBM Bob find answers from your uploaded syllabus using RAG?",
    options: [
      "It randomly guesses what sounds good",
      "It cuts docs into chunks, creates mathematical number embeddings, and retrieves the most similar concepts",
      "It sends an email to your university professor",
      "It runs a simple Ctrl+F exact word search only"
    ],
    correctIndex: 1,
    eli10: "Imagine your textbook is a giant library. RAG turns every paragraph into a coordinate on a treasure map. When you ask a question, IBM Bob instantly flies directly to the exact treasure chest page!",
    points: 1200
  },
  {
    id: 3,
    topic: "Algorithms & Time Complexity",
    question: "Why is Binary Search faster than Linear Search on sorted lists?",
    options: [
      "It cuts the search space in half with every single comparison (O(log n))",
      "It uses twice as much RAM memory",
      "It only checks the first and last element",
      "It sorts the list backwards in reverse"
    ],
    correctIndex: 0,
    eli10: "If you're guessing a number between 1 and 100 and I say 'Higher' or 'Lower', guessing 50 immediately eliminates half the numbers at once!",
    points: 1000
  }
];

const KahootQuiz = ({ onAddXP }) => {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedOpt, setSelectedOpt] = useState(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [streakMultiplier, setStreakMultiplier] = useState(1);
  const [timeLeft, setTimeLeft] = useState(20);
  const [isQuizComplete, setIsQuizComplete] = useState(false);

  const currentQ = SAMPLE_QUESTIONS[currentIdx];

  const handleOptionClick = useCallback((idx) => {
    if (isAnswered) return;
    setSelectedOpt(idx);
    setIsAnswered(true);

    const isCorrect = idx === currentQ.correctIndex;
    if (isCorrect) {
      const earnedScore = Math.round(currentQ.points * (timeLeft / 20) * streakMultiplier);
      setScore(s => s + earnedScore);
      setStreakMultiplier(m => Math.min(3, m + 0.5));
      if (onAddXP) onAddXP(75);

      confetti({
        particleCount: 60,
        spread: 70,
        origin: { y: 0.6 }
      });
    } else {
      setStreakMultiplier(1);
    }
  }, [isAnswered, currentQ, timeLeft, streakMultiplier, onAddXP]);

  useEffect(() => {
    if (isAnswered || isQuizComplete) return;

    if (timeLeft <= 0) {
      handleOptionClick(-1); // Timed out
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft(t => t - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, isAnswered, isQuizComplete, handleOptionClick]);




  const handleNextQuestion = () => {
    if (currentIdx + 1 < SAMPLE_QUESTIONS.length) {
      setCurrentIdx(i => i + 1);
      setSelectedOpt(null);
      setIsAnswered(false);
      setTimeLeft(20);
      setShowEli10Tip(false);
    } else {
      setIsQuizComplete(true);
      confetti({
        particleCount: 100,
        spread: 90,
        origin: { y: 0.5 }
      });
    }
  };

  const handleRestart = () => {
    setCurrentIdx(0);
    setSelectedOpt(null);
    setIsAnswered(false);
    setScore(0);
    setStreakMultiplier(1);
    setTimeLeft(20);
    setIsQuizComplete(false);
    setShowEli10Tip(false);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      
      {/* Top Kahoot Status Bar */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <Trophy className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-white text-sm">Kahoot-Style Practice Arena</span>
              <span className="px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20 text-[11px] font-semibold">
                IBM Bob Quiz
              </span>
            </div>
            <p className="text-xs text-slate-400">Topic: {currentQ?.topic || "Syllabus Mastery"}</p>
          </div>
        </div>

        {/* Live Score & Streak */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-bold text-amber-400">
            <Flame className="w-4 h-4 text-orange-500 fill-orange-500" />
            <span>{streakMultiplier}x Combo</span>
          </div>

          <div className="text-right">
            <div className="text-lg font-black text-blue-400 tracking-tight">{score} PTS</div>
            <div className="text-[10px] text-slate-400 uppercase font-semibold">
              Q {currentIdx + 1} / {SAMPLE_QUESTIONS.length}
            </div>
          </div>
        </div>
      </div>

      {!isQuizComplete ? (
        <div className="space-y-6">
          
          {/* Question Card with Timer bar */}
          <div className="p-8 rounded-3xl glass-panel bg-gradient-to-b from-slate-900/90 to-slate-950 border border-slate-800 shadow-2xl relative overflow-hidden">
            
            {/* Timer Progress Bar */}
            <div className="w-full h-2 bg-slate-800 rounded-full mb-6 overflow-hidden">
              <div
                className={`h-full transition-all duration-1000 ${
                  timeLeft > 10 ? 'bg-blue-500' : timeLeft > 5 ? 'bg-amber-500' : 'bg-rose-500 animate-pulse'
                }`}
                style={{ width: `${(timeLeft / 20) * 100}%` }}
              ></div>
            </div>

            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-2">
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-blue-400" /> {timeLeft}s remaining
              </span>
              <span className="text-purple-400 font-mono">+{currentQ.points} Max Pts</span>
            </div>

            <h3 className="text-xl sm:text-2xl font-extrabold text-white text-center py-4 leading-snug">
              {currentQ.question}
            </h3>

            {/* Answer Result Banner */}
            {isAnswered && (
              <div
                className={`mt-4 p-4 rounded-2xl border text-center animate-in zoom-in-95 duration-200 ${
                  selectedOpt === currentQ.correctIndex
                    ? 'bg-emerald-950/60 border-emerald-500/50 text-emerald-300'
                    : 'bg-rose-950/60 border-rose-500/50 text-rose-300'
                }`}
              >
                <div className="font-bold text-base flex items-center justify-center gap-2">
                  {selectedOpt === currentQ.correctIndex ? (
                    <>
                      <Check className="w-5 h-5 text-emerald-400" />
                      <span>Spot on! Correct Answer 🎉 (+{Math.round(currentQ.points * (timeLeft / 20) * streakMultiplier)} PTS)</span>
                    </>
                  ) : (
                    <span>Incorrect! The correct answer was option {currentQ.correctIndex + 1}.</span>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* 4 Colored Kahoot Style Grid Options */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {currentQ.options.map((option, idx) => {
              const colorInfo = KAHOOT_COLORS[idx];
              let cardState = `${colorInfo.bg} shadow-lg text-white`;

              if (isAnswered) {
                if (idx === currentQ.correctIndex) {
                  cardState = 'bg-emerald-600 ring-4 ring-emerald-300 scale-[1.02] text-white';
                } else if (selectedOpt === idx) {
                  cardState = 'bg-rose-700 opacity-80 text-white';
                } else {
                  cardState = 'bg-slate-900 border border-slate-800 opacity-40 text-slate-400';
                }
              }

              return (
                <button
                  key={idx}
                  onClick={() => handleOptionClick(idx)}
                  disabled={isAnswered}
                  className={`p-6 rounded-2xl text-left font-semibold text-sm sm:text-base transition-all duration-200 flex items-start gap-4 cursor-pointer disabled:cursor-default ${cardState}`}
                >
                  <div className="w-8 h-8 rounded-lg bg-black/25 flex items-center justify-center font-bold text-sm shrink-0">
                    <span className={colorInfo.shapeColor}>{colorInfo.shape}</span>
                  </div>
                  <span className="flex-1 mt-0.5 leading-relaxed">{option}</span>
                </button>
              );
            })}
          </div>

          {/* "Explain Like I'm 10" Section Toggle */}
          {isAnswered && (
            <div className="p-5 rounded-2xl bg-gradient-to-r from-amber-950/30 via-slate-900 to-indigo-950/30 border border-amber-500/30 space-y-3 animate-in fade-in duration-300">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-amber-400" />
                  <span className="text-xs font-bold text-amber-300 uppercase tracking-wider">
                    IBM Bob's "Explain Like I'm 10" Breakdown
                  </span>
                </div>
                <button
                  onClick={handleNextQuestion}
                  className="px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-md shadow-blue-600/20 transition-all hover:scale-105"
                >
                  <span>{currentIdx + 1 < SAMPLE_QUESTIONS.length ? "Next Question" : "See Final Score"}</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
                "{currentQ.eli10}"
              </p>
            </div>
          )}

        </div>
      ) : (
        /* Final Leaderboard / Score Screen */
        <div className="p-10 rounded-3xl glass-panel bg-gradient-to-b from-slate-900 to-slate-950 text-center space-y-6 border border-purple-500/30">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-amber-500 to-orange-400 p-[1px] mx-auto shadow-xl shadow-amber-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[23px] flex items-center justify-center">
              <Trophy className="w-10 h-10 text-amber-400" />
            </div>
          </div>

          <div className="space-y-1">
            <h3 className="text-3xl font-black text-white">Quiz Completed!</h3>
            <p className="text-sm text-slate-400">You earned high rank on the syllabus leaderboard.</p>
          </div>

          <div className="inline-block p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-1">
            <div className="text-4xl font-extrabold text-blue-400 tracking-tight">{score}</div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Total Score Points</div>
          </div>

          <div className="pt-2 flex justify-center gap-4">
            <button
              onClick={handleRestart}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-blue-600/20 transition-all hover:scale-105"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Play Again</span>
            </button>
          </div>
        </div>
      )}

    </div>
  );
};

export default KahootQuiz;
