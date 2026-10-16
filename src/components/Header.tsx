import { Terminal, LayoutDashboard, RotateCcw } from 'lucide-react';

interface HeaderProps {
  mode: 'gui' | 'terminal';
  onToggleMode: () => void;
  onReset: () => void;
  inQuiz: boolean;
  score: number;
  totalAnswered: number;
}

export const Header: React.FC<HeaderProps> = ({
  mode,
  onToggleMode,
  onReset,
  inQuiz,
  score,
  totalAnswered
}) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer" onClick={onReset} role="button" tabIndex={0}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white font-mono font-bold text-lg">
            &gt;_
          </div>
          <div>
            <h1 className="font-semibold text-slate-100 text-base sm:text-lg flex items-center gap-2">
              Quiz Master
              <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">
                Tech & Trivia
              </span>
            </h1>
            <p className="text-xs text-slate-400 hidden sm:block">
              Python • DSA • Web • Databases • Git • CS Basics
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-4">
          {inQuiz && (
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300 font-mono">
              <span className="text-slate-400">Score:</span>
              <span className="text-emerald-400 font-bold">{score}</span>
              <span className="text-slate-500">/</span>
              <span>{totalAnswered}</span>
            </div>
          )}

          {inQuiz && (
            <button
              onClick={onReset}
              className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors flex items-center gap-1.5 text-xs"
              title="Restart Quiz"
            >
              <RotateCcw className="w-4 h-4" />
              <span className="hidden md:inline">Restart</span>
            </button>
          )}

          <button
            onClick={onToggleMode}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-2 transition-all border ${
              mode === 'terminal'
                ? 'bg-emerald-950/80 text-emerald-300 border-emerald-700/60 shadow-sm shadow-emerald-900/40'
                : 'bg-slate-800 hover:bg-slate-700/80 text-slate-300 border-slate-700'
            }`}
            title={mode === 'terminal' ? 'Switch to Modern GUI' : 'Switch to CLI Terminal'}
          >
            {mode === 'terminal' ? (
              <>
                <LayoutDashboard className="w-3.5 h-3.5" />
                <span>Modern GUI</span>
              </>
            ) : (
              <>
                <Terminal className="w-3.5 h-3.5 text-emerald-400" />
                <span>CLI Terminal</span>
              </>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
