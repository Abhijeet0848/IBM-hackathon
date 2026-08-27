import React, { useState, useEffect, useCallback } from 'react';
import { 
  RefreshCw, Check, Flame, Clock, 
  Sparkles, Trophy, ArrowRight 
} from 'lucide-react';
import confetti from 'canvas-confetti';

const KAHOOT_COLORS = [
  { bg: 'bg-red-500 hover:bg-red-600', border: 'border-red-600', shape: '▲', shapeColor: 'text-white' },
  { bg: 'bg-blue-500 hover:bg-blue-600', border: 'border-blue-600', shape: '◆', shapeColor: 'text-white' },
  { bg: 'bg-amber-500 hover:bg-amber-600', border: 'border-amber-600', shape: '●', shapeColor: 'text-white' },
  { bg: 'bg-emerald-500 hover:bg-emerald-600', border: 'border-emerald-600', shape: '◼', shapeColor: 'text-white' },
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
      handleOptionClick(-1);
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
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      
      {/* Top Status Bar */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-white border border-slate-200 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-purple-50 border border-purple-200 flex items-center justify-center text-purple-700">
            <Trophy className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 text-sm">Kahoot-Style Practice Arena</span>
              <span className="px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200 text-[11px] font-semibold">
                IBM Bob Quiz
              </span>
            </div>
            <p className="text-xs text-slate-500">Topic: {currentQ?.topic || "Syllabus Mastery"}</p>
          </div>
        </div>

        {/* Live Score & Streak */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-xs font-bold text-orange-600">
            <Flame className="w-4 h-4 fill-orange-500 text-orange-500" />
            <span>{streakMultiplier}x Combo</span>
          </div>

          <div className="text-right">
            <div className="text-base font-extrabold text-blue-600 tracking-tight">{score} PTS</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold">
              Q {currentIdx + 1} / {SAMPLE_QUESTIONS.length}
            </div>
          </div>
        </div>
      </div>

      {!isQuizComplete ? (
        <div className="space-y-5">
          
          {/* Question Card with Timer */}
          <div className="p-8 rounded-2xl bg-white border border-slate-200 shadow-xs relative overflow-hidden">
            
            {/* Timer Progress Bar */}
            <div className="w-full h-2 bg-slate-100 rounded-full mb-6 overflow-hidden">
              <div
                className={`h-full transition-all duration-1000 ${
                  timeLeft > 10 ? 'bg-blue-600' : timeLeft > 5 ? 'bg-amber-500' : 'bg-rose-500 animate-pulse'
                }`}
                style={{ width: `${(timeLeft / 20) * 100}%` }}
              ></div>
            </div>

            <div className="flex items-center justify-between text-xs font-semibold text-slate-500 mb-2">
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-blue-600" /> {timeLeft}s remaining
              </span>
              <span className="text-purple-600 font-mono">+{currentQ.points} Max Pts</span>
            </div>

            <h3 className="text-xl sm:text-2xl font-extrabold text-slate-900 text-center py-3 leading-snug">
              {currentQ.question}
            </h3>

            {/* Answer Result Banner */}
            {isAnswered && (
              <div
                className={`mt-4 p-4 rounded-xl border text-center animate-in zoom-in-95 duration-200 ${
                  selectedOpt === currentQ.correctIndex
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-800'
                    : 'bg-rose-50 border-rose-300 text-rose-800'
                }`}
              >
                <div className="font-bold text-sm sm:text-base flex items-center justify-center gap-2">
                  {selectedOpt === currentQ.correctIndex ? (
                    <>
                      <Check className="w-5 h-5 text-emerald-600" />
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
              let cardState = `${colorInfo.bg} shadow-xs text-white`;

              if (isAnswered) {
                if (idx === currentQ.correctIndex) {
                  cardState = 'bg-emerald-600 ring-4 ring-emerald-300 text-white scale-101';
                } else if (selectedOpt === idx) {
                  cardState = 'bg-rose-600 opacity-85 text-white';
                } else {
                  cardState = 'bg-slate-200 text-slate-400 opacity-50';
                }
              }

              return (
                <button
                  key={idx}
                  onClick={() => handleOptionClick(idx)}
                  disabled={isAnswered}
                  className={`p-5 rounded-2xl text-left font-semibold text-sm transition-all flex items-start gap-3.5 cursor-pointer disabled:cursor-default ${cardState}`}
                >
                  <div className="w-7 h-7 rounded-lg bg-black/20 flex items-center justify-center font-bold text-xs shrink-0">
                    <span className={colorInfo.shapeColor}>{colorInfo.shape}</span>
                  </div>
                  <span className="flex-1 mt-0.5 leading-relaxed">{option}</span>
                </button>
              );
            })}
          </div>

          {/* Explanation & Next */}
          {isAnswered && (
            <div className="p-5 rounded-2xl bg-amber-50 border border-amber-200 space-y-3 animate-in fade-in duration-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-amber-600" />
                  <span className="text-xs font-bold text-amber-900 uppercase tracking-wider">
                    IBM Bob's ELI10 Breakdown
                  </span>
                </div>
                <button
                  onClick={handleNextQuestion}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-xs transition-all cursor-pointer"
                >
                  <span>{currentIdx + 1 < SAMPLE_QUESTIONS.length ? "Next Question" : "See Final Score"}</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              <p className="text-xs sm:text-sm text-amber-950 leading-relaxed bg-white/70 p-3 rounded-xl border border-amber-200">
                "{currentQ.eli10}"
              </p>
            </div>
          )}

        </div>
      ) : (
        /* Final Leaderboard / Score Screen */
        <div className="p-8 rounded-2xl bg-white border border-slate-200 text-center space-y-5 shadow-xs">
          <div className="w-16 h-16 rounded-2xl bg-amber-50 border border-amber-200 mx-auto flex items-center justify-center">
            <Trophy className="w-8 h-8 text-amber-600" />
          </div>

          <div className="space-y-1">
            <h3 className="text-2xl font-bold text-slate-900">Quiz Completed!</h3>
            <p className="text-xs text-slate-500">You earned high rank on the syllabus leaderboard.</p>
          </div>

          <div className="inline-block p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-3xl font-extrabold text-blue-600">{score}</div>
            <div className="text-xs text-slate-500 font-medium uppercase tracking-wider">Total Score Points</div>
          </div>

          <div className="pt-2 flex justify-center">
            <button
              onClick={handleRestart}
              className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl text-xs sm:text-sm flex items-center gap-2 shadow-xs transition-all cursor-pointer"
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
