import React, { useMemo } from 'react';
import { CATEGORIES, QUESTION_BANK } from '../data/questions';
import { 
  Code2, 
  Binary, 
  Globe, 
  Database, 
  GitBranch, 
  Cpu, 
  HelpCircle, 
  Layers, 
  Play, 
  Zap,
  CheckCircle2,
  Terminal
} from 'lucide-react';

interface SetupScreenProps {
  category: string;
  questionCount: number;
  onCategoryChange: (cat: string) => void;
  onCountChange: (count: number) => void;
  onStartQuiz: () => void;
  onStartTerminalMode: () => void;
}

export const SetupScreen: React.FC<SetupScreenProps> = ({
  category,
  questionCount,
  onCategoryChange,
  onCountChange,
  onStartQuiz,
  onStartTerminalMode
}) => {
  // Compute counts per category
  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = { 'All Categories': QUESTION_BANK.length };
    QUESTION_BANK.forEach(q => {
      counts[q.category] = (counts[q.category] || 0) + 1;
    });
    return counts;
  }, []);

  const maxAvailable = categoryCounts[category] || QUESTION_BANK.length;
  const currentCount = Math.min(questionCount, maxAvailable);

  const getCategoryIcon = (cat: string) => {
    switch (cat) {
      case 'Python':
        return <Code2 className="w-4 h-4 text-amber-400" />;
      case 'DSA':
        return <Binary className="w-4 h-4 text-sky-400" />;
      case 'Web':
        return <Globe className="w-4 h-4 text-emerald-400" />;
      case 'Databases':
        return <Database className="w-4 h-4 text-violet-400" />;
      case 'Git & DevOps':
        return <GitBranch className="w-4 h-4 text-orange-400" />;
      case 'CS Basics':
        return <Cpu className="w-4 h-4 text-pink-400" />;
      case 'General Trivia':
        return <HelpCircle className="w-4 h-4 text-teal-400" />;
      default:
        return <Layers className="w-4 h-4 text-indigo-400" />;
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 sm:py-12">
      {/* Hero Welcome banner */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-mono font-medium mb-4">
          <Zap className="w-3.5 h-3.5" />
          Technical & CS Knowledge Assessment
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-100 tracking-tight mb-3">
          Sharpen Your Computer Science Mind
        </h1>
        <p className="text-slate-400 text-sm sm:text-base max-w-xl mx-auto leading-relaxed">
          Test your mastery across Python, data structures, networking, SQL, Git, and computer architecture with real-time feedback and explanation tips.
        </p>
      </div>

      {/* Main Configuration Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl backdrop-blur-sm mb-8">
        {/* Category Selection */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <label className="text-sm font-semibold text-slate-200">
              1. Select Domain / Category
            </label>
            <span className="text-xs text-slate-400">
              Total {QUESTION_BANK.length} curated questions
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            {CATEGORIES.map((cat) => {
              const count = categoryCounts[cat] || 0;
              const isSelected = category === cat;

              return (
                <button
                  key={cat}
                  onClick={() => {
                    onCategoryChange(cat);
                    const newMax = categoryCounts[cat] || QUESTION_BANK.length;
                    if (questionCount > newMax) {
                      onCountChange(newMax);
                    }
                  }}
                  className={`p-3 rounded-xl border text-left transition-all duration-150 flex flex-col justify-between h-20 ${
                    isSelected
                      ? 'bg-indigo-600/20 border-indigo-500 text-indigo-100 shadow-sm shadow-indigo-500/20 ring-1 ring-indigo-500'
                      : 'bg-slate-800/60 hover:bg-slate-800 border-slate-700/60 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    {getCategoryIcon(cat)}
                    <span className={`text-[11px] font-mono px-1.5 py-0.5 rounded ${
                      isSelected ? 'bg-indigo-500/30 text-indigo-200' : 'bg-slate-700/60 text-slate-400'
                    }`}>
                      {count}
                    </span>
                  </div>
                  <span className="text-xs font-medium truncate mt-1">
                    {cat}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Question Count Selection */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <label className="text-sm font-semibold text-slate-200">
              2. Number of Questions
            </label>
            <span className="text-xs font-mono text-indigo-400 bg-indigo-950/60 border border-indigo-800/60 px-2 py-0.5 rounded-md">
              {currentCount} of {maxAvailable} questions
            </span>
          </div>

          {/* Preset Buttons */}
          <div className="flex flex-wrap items-center gap-2 mb-4">
            {[5, 10, 15, 20].map((preset) => {
              if (preset > maxAvailable) return null;
              const isSelected = currentCount === preset;
              return (
                <button
                  key={preset}
                  onClick={() => onCountChange(preset)}
                  className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                    isSelected
                      ? 'bg-indigo-600 text-white font-semibold shadow-md shadow-indigo-600/30'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/60'
                  }`}
                >
                  {preset} Questions
                </button>
              );
            })}
            <button
              onClick={() => onCountChange(maxAvailable)}
              className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                currentCount === maxAvailable
                  ? 'bg-indigo-600 text-white font-semibold shadow-md shadow-indigo-600/30'
                  : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/60'
              }`}
            >
              All {maxAvailable} Questions
            </button>
          </div>

          {/* Slider */}
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-slate-500">1</span>
            <input
              type="range"
              min={1}
              max={maxAvailable}
              value={currentCount}
              onChange={(e) => onCountChange(parseInt(e.target.value, 10))}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
            />
            <span className="text-xs font-mono text-slate-500">{maxAvailable}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center gap-3 pt-4 border-t border-slate-800">
          <button
            onClick={onStartQuiz}
            className="w-full sm:flex-1 py-3.5 px-6 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all transform active:scale-[0.99]"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>Start Interactive Quiz</span>
          </button>

          <button
            onClick={onStartTerminalMode}
            className="w-full sm:w-auto py-3.5 px-5 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-300 hover:text-white border border-slate-700 text-xs font-mono font-medium flex items-center justify-center gap-2 transition-colors"
          >
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span>Launch CLI Mode</span>
          </button>
        </div>
      </div>

      {/* Feature Highlights / Original Spec */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-400">
        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/70 flex items-start gap-3">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-slate-300 mb-1">Randomized Options</h4>
            <p className="leading-relaxed">Answer choices shuffle every round with dynamic A-D key bindings.</p>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/70 flex items-start gap-3">
          <Zap className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-slate-300 mb-1">Immediate Explanations</h4>
            <p className="leading-relaxed">Learn as you play with built-in explanation tips on every answer.</p>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/70 flex items-start gap-3">
          <Binary className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-slate-300 mb-1">Review Missed Topics</h4>
            <p className="leading-relaxed">Target weak areas with tailored round reviews and retry practice.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
