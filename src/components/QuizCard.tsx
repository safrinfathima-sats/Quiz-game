import React, { useEffect, useCallback } from 'react';
import { ShuffledQuestion } from '../types';
import { LETTERS } from '../data/questions';
import { Check, X, Lightbulb, ArrowRight, CornerDownLeft } from 'lucide-react';

interface QuizCardProps {
  question: ShuffledQuestion;
  currentIndex: number;
  totalQuestions: number;
  selectedAnswer?: 'A' | 'B' | 'C' | 'D';
  onSelectAnswer: (letter: 'A' | 'B' | 'C' | 'D') => void;
  onNextQuestion: () => void;
  isLastQuestion: boolean;
}

export const QuizCard: React.FC<QuizCardProps> = ({
  question,
  currentIndex,
  totalQuestions,
  selectedAnswer,
  onSelectAnswer,
  onNextQuestion,
  isLastQuestion
}) => {
  const isAnswered = selectedAnswer !== undefined;
  const isCorrect = isAnswered && selectedAnswer === question.answer;

  // Keyboard shortcut listener
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    // If inside an input or textarea, ignore
    if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;

    const key = e.key.toUpperCase();

    if (!isAnswered) {
      if (['A', 'B', 'C', 'D'].includes(key)) {
        e.preventDefault();
        onSelectAnswer(key as 'A' | 'B' | 'C' | 'D');
      } else if (['1', '2', '3', '4'].includes(key)) {
        e.preventDefault();
        const index = parseInt(key, 10) - 1;
        const letter = LETTERS[index];
        if (letter) onSelectAnswer(letter);
      }
    } else {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') {
        e.preventDefault();
        onNextQuestion();
      }
    }
  }, [isAnswered, onSelectAnswer, onNextQuestion]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  const progressPercent = ((currentIndex + 1) / totalQuestions) * 100;

  return (
    <div className="max-w-3xl mx-auto px-4 py-6 sm:py-10">
      {/* Progress & Meta Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-200">
              Question {currentIndex + 1}
            </span>
            <span className="text-slate-600">/</span>
            <span>{totalQuestions}</span>
            <span className="px-2 py-0.5 rounded-full bg-slate-800 text-indigo-400 border border-slate-700/60 font-medium ml-1">
              {question.category}
            </span>
          </div>
          <div className="text-slate-500 hidden sm:block">
            Keyboard: <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">A</kbd> <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">B</kbd> <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">C</kbd> <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">D</kbd>
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-300 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl backdrop-blur-sm">
        <h2 className="text-lg sm:text-xl font-semibold text-slate-100 mb-6 leading-relaxed font-sans">
          {question.question}
        </h2>

        {/* Options Grid */}
        <div className="space-y-3 mb-6">
          {question.options.map((option, index) => {
            const letter = LETTERS[index];
            const isSelected = selectedAnswer === letter;
            const isOptionCorrect = letter === question.answer;

            let optionStyle = 'bg-slate-800/70 hover:bg-slate-800 hover:border-slate-600 border-slate-700/60 text-slate-200';
            let badgeStyle = 'bg-slate-700/60 text-slate-300 border-slate-600';

            if (isAnswered) {
              if (isOptionCorrect) {
                // Correct answer is always green
                optionStyle = 'bg-emerald-950/60 border-emerald-500 text-emerald-100 shadow-sm shadow-emerald-500/10 ring-1 ring-emerald-500';
                badgeStyle = 'bg-emerald-600 text-white border-emerald-500';
              } else if (isSelected && !isOptionCorrect) {
                // Chosen wrong answer is red
                optionStyle = 'bg-rose-950/60 border-rose-500 text-rose-100 ring-1 ring-rose-500';
                badgeStyle = 'bg-rose-600 text-white border-rose-500';
              } else {
                // Other options muted
                optionStyle = 'bg-slate-800/30 border-slate-800/60 text-slate-500 opacity-60';
                badgeStyle = 'bg-slate-800 text-slate-600 border-slate-700';
              }
            }

            return (
              <button
                key={letter}
                onClick={() => !isAnswered && onSelectAnswer(letter)}
                disabled={isAnswered}
                className={`w-full p-4 rounded-xl border text-left flex items-center justify-between transition-all duration-150 group ${optionStyle} ${
                  !isAnswered ? 'cursor-pointer active:scale-[0.99]' : 'cursor-default'
                }`}
              >
                <div className="flex items-center gap-3.5 pr-2">
                  <span className={`w-8 h-8 rounded-lg border font-mono text-xs font-bold flex items-center justify-center shrink-0 transition-colors ${badgeStyle}`}>
                    {letter}
                  </span>
                  <span className="text-sm sm:text-base font-medium leading-snug">
                    {option}
                  </span>
                </div>

                {isAnswered && (
                  <div className="shrink-0 pl-2">
                    {isOptionCorrect ? (
                      <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                        <Check className="w-4 h-4 stroke-[3]" />
                      </span>
                    ) : isSelected ? (
                      <span className="w-6 h-6 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center">
                        <X className="w-4 h-4 stroke-[3]" />
                      </span>
                    ) : null}
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Feedback Section (Shown after answering) */}
        {isAnswered && (
          <div className="pt-4 border-t border-slate-800 animate-in fade-in duration-200">
            {/* Status callout */}
            <div className={`p-4 rounded-xl mb-4 border flex items-start gap-3 ${
              isCorrect
                ? 'bg-emerald-950/40 border-emerald-800/60 text-emerald-200'
                : 'bg-rose-950/40 border-rose-800/60 text-rose-200'
            }`}>
              <div className="mt-0.5">
                {isCorrect ? (
                  <Check className="w-5 h-5 text-emerald-400" />
                ) : (
                  <X className="w-5 h-5 text-rose-400" />
                )}
              </div>
              <div className="flex-1">
                <div className="font-semibold text-sm">
                  {isCorrect ? 'Correct!' : (
                    <span>
                      Wrong! The correct answer is <span className="underline font-bold">{question.answer}</span>. {question.correctText}
                    </span>
                  )}
                </div>
                {/* Tip as requested in original QUIZ GAME.py */}
                <div className="mt-2 text-xs flex items-start gap-1.5 opacity-90 font-sans">
                  <Lightbulb className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                  <span>
                    <strong className="text-amber-300">Tip:</strong> {question.explanation}
                  </span>
                </div>
              </div>
            </div>

            {/* Next Question Button */}
            <div className="flex justify-end">
              <button
                onClick={onNextQuestion}
                className="py-3 px-6 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center gap-2 shadow-lg shadow-indigo-600/20 transition-all cursor-pointer active:scale-95"
              >
                <span>{isLastQuestion ? 'View Final Results' : 'Next Question'}</span>
                <ArrowRight className="w-4 h-4" />
                <span className="text-[11px] font-mono opacity-70 hidden sm:inline-flex items-center gap-0.5 bg-indigo-700/60 px-1.5 py-0.5 rounded">
                  <CornerDownLeft className="w-3 h-3" /> Enter
                </span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
