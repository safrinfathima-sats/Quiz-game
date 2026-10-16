import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { ShuffledQuestion } from '../types';
import { 
  Trophy, 
  RotateCcw, 
  Sparkles, 
  BookOpen, 
  CheckCircle2, 
  XCircle, 
  Sliders, 
  Lightbulb
} from 'lucide-react';

interface ResultScreenProps {
  score: number;
  total: number;
  questions: ShuffledQuestion[];
  onPlayAgain: () => void;
  onRetryMissed: () => void;
  onNewSettings: () => void;
}

export const ResultScreen: React.FC<ResultScreenProps> = ({
  score,
  total,
  questions,
  onPlayAgain,
  onRetryMissed,
  onNewSettings
}) => {
  const percent = Math.round((score / total) * 100);
  const missed = questions.filter(q => !q.isCorrect);

  // Determine feedback tier from original QUIZ GAME.py lines 215-223
  let evaluationMessage = '';
  let evaluationSub = '';

  if (percent === 100) {
    evaluationMessage = 'Perfect! You really know your stuff.';
    evaluationSub = 'Flawless execution across every question.';
  } else if (percent >= 70) {
    evaluationMessage = 'Great job! Keep it up.';
    evaluationSub = 'Solid mastery of technical concepts and principles.';
  } else if (percent >= 40) {
    evaluationMessage = 'Not bad - review the tips and try again.';
    evaluationSub = 'Good effort! Check the review notes below to solidify your understanding.';
  } else {
    evaluationMessage = 'Keep practicing - every attempt makes you better!';
    evaluationSub = 'Every master was once a beginner. Study the missed topics and try again.';
  }

  // Fire confetti on high score
  useEffect(() => {
    if (percent >= 70) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
  }, [percent]);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 sm:py-12 animate-in fade-in duration-300">
      {/* Result Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl backdrop-blur-md mb-8 text-center relative overflow-hidden">
        {/* Decorative background glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex p-3 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-4">
          <Trophy className="w-8 h-8" />
        </div>

        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100 mb-2">
          Quiz Completed!
        </h2>
        
        {/* Score & Percentage */}
        <div className="my-6">
          <div className="text-5xl sm:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-sky-300 to-emerald-400 font-mono tracking-tight">
            {score} <span className="text-slate-600 font-light">/</span> {total}
          </div>
          <div className="mt-2 text-slate-400 text-sm font-medium">
            Final Score: <span className="text-slate-200 font-bold">{percent}%</span> accuracy
          </div>
        </div>

        {/* Evaluation Banner */}
        <div className="max-w-md mx-auto p-4 rounded-2xl bg-slate-800/80 border border-slate-700/80 mb-6">
          <p className="font-semibold text-slate-100 text-base mb-1">
            "{evaluationMessage}"
          </p>
          <p className="text-xs text-slate-400">
            {evaluationSub}
          </p>
        </div>

        {/* Quick summary stats */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 max-w-lg mx-auto mb-8 text-left">
          <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
            <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Correct
            </div>
            <div className="text-lg font-bold text-emerald-400 font-mono">{score}</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
            <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
              <XCircle className="w-3.5 h-3.5 text-rose-400" />
              Missed
            </div>
            <div className="text-lg font-bold text-rose-400 font-mono">{missed.length}</div>
          </div>
          <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40 col-span-2 sm:col-span-1">
            <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
              Accuracy
            </div>
            <div className="text-lg font-bold text-indigo-300 font-mono">{percent}%</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={onPlayAgain}
            className="w-full sm:w-auto px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all cursor-pointer"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Play Again</span>
          </button>

          {missed.length > 0 && (
            <button
              onClick={onRetryMissed}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm shadow-lg shadow-emerald-600/20 flex items-center justify-center gap-2 transition-all cursor-pointer"
            >
              <BookOpen className="w-4 h-4" />
              <span>Retry {missed.length} Missed Question{missed.length > 1 ? 's' : ''}</span>
            </button>
          )}

          <button
            onClick={onNewSettings}
            className="w-full sm:w-auto px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-sm font-medium flex items-center justify-center gap-2 transition-colors cursor-pointer"
          >
            <Sliders className="w-4 h-4" />
            <span>Change Settings</span>
          </button>
        </div>
      </div>

      {/* Topics to Review Section (matching line 224-228 of QUIZ GAME.py) */}
      {missed.length > 0 && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 sm:p-8">
          <div className="flex items-center gap-2 text-slate-200 font-bold text-base mb-4">
            <BookOpen className="w-5 h-5 text-indigo-400" />
            <span>Topics to Review ({missed.length})</span>
          </div>
          <p className="text-xs text-slate-400 mb-6">
            Reviewing these explanations will help reinforce the concepts you missed during this round:
          </p>

          <div className="space-y-4">
            {missed.map((q, idx) => (
              <div 
                key={idx}
                className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 text-slate-300"
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    [{q.category}]
                  </span>
                  {q.userAnswer && (
                    <span className="text-xs text-rose-400">
                      Your answer: {q.userAnswer}
                    </span>
                  )}
                </div>

                <div className="font-medium text-slate-100 text-sm mb-2">
                  {q.question}
                </div>

                <div className="text-xs text-emerald-400 font-semibold mb-2">
                  Correct Answer: {q.answer}. {q.correctText}
                </div>

                <div className="text-xs text-slate-300 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 flex items-start gap-2">
                  <Lightbulb className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                  <span>
                    <strong className="text-amber-300">Tip:</strong> {q.explanation}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
