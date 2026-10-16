import React, { useState, useEffect, useRef } from 'react';
import { QUESTION_BANK, LETTERS, buildShuffledQuestion, shuffleArray } from '../data/questions';
import { ShuffledQuestion } from '../types';
import { Terminal, CornerDownLeft, RefreshCw } from 'lucide-react';

interface TerminalLine {
  text: string;
  type: 'output' | 'input' | 'system' | 'success' | 'error' | 'tip' | 'header';
}

type TerminalPhase = 
  | 'ask_count' 
  | 'ask_answer' 
  | 'ask_replay' 
  | 'finished';

export const TerminalView: React.FC<{ onExitTerminal: () => void }> = ({ onExitTerminal }) => {
  const [lines, setLines] = useState<TerminalLine[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [phase, setPhase] = useState<TerminalPhase>('ask_count');
  
  // Game state
  const [activeQuestions, setActiveQuestions] = useState<ShuffledQuestion[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [score, setScore] = useState(0);
  const [missedQuestions, setMissedQuestions] = useState<ShuffledQuestion[]>([]);
  const [totalCount, setTotalCount] = useState(10);

  const terminalEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [lines]);

  // Initial boot message
  useEffect(() => {
    initGame();
  }, []);

  const initGame = () => {
    const initialLines: TerminalLine[] = [
      { text: '$ python3 "QUIZ GAME.py"', type: 'system' },
      { text: '========================================', type: 'header' },
      { text: '       === Technical Quiz Game ===       ', type: 'header' },
      { text: '========================================', type: 'header' },
      { text: `Question bank size: ${QUESTION_BANK.length} questions\n`, type: 'output' },
      { text: `How many questions would you like? (1-${QUESTION_BANK.length}, default 10): `, type: 'system' }
    ];
    setLines(initialLines);
    setPhase('ask_count');
    setInputValue('');
  };

  const startRoundWithCount = (count: number) => {
    const selectedBank = shuffleArray([...QUESTION_BANK]).slice(0, count);
    const questions = selectedBank.map(item => buildShuffledQuestion(item));
    setActiveQuestions(questions);
    setCurrentIdx(0);
    setScore(0);
    setMissedQuestions([]);
    setTotalCount(count);

    printQuestion(questions[0], 0, count);
    setPhase('ask_answer');
  };

  const printQuestion = (q: ShuffledQuestion, idx: number, total: number) => {
    const newLines: TerminalLine[] = [
      { text: `\nQuestion ${idx + 1}/${total}  [${q.category}]`, type: 'header' },
      { text: q.question, type: 'output' },
      ...q.options.map((opt: string, optIdx: number) => ({
        text: `  ${LETTERS[optIdx]}. ${opt}`,
        type: 'output' as const
      })),
      { text: 'Enter your answer (A/B/C/D): ', type: 'system' }
    ];
    setLines(prev => [...prev, ...newLines]);
  };

  const handleInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const raw = inputValue.trim();
    setInputValue('');

    if (phase === 'ask_count') {
      // Record user input line
      setLines(prev => [...prev, { text: raw || '10', type: 'input' }]);

      let count = 10;
      if (raw === '') {
        count = Math.min(10, QUESTION_BANK.length);
      } else {
        const parsed = parseInt(raw, 10);
        if (!isNaN(parsed) && parsed >= 1 && parsed <= QUESTION_BANK.length) {
          count = parsed;
        } else {
          setLines(prev => [
            ...prev,
            { text: `Please enter a number between 1 and ${QUESTION_BANK.length}.`, type: 'error' },
            { text: `How many questions would you like? (1-${QUESTION_BANK.length}, default 10): `, type: 'system' }
          ]);
          return;
        }
      }

      startRoundWithCount(count);

    } else if (phase === 'ask_answer') {
      const userAns = raw.toUpperCase() as 'A' | 'B' | 'C' | 'D';
      setLines(prev => [...prev, { text: raw, type: 'input' }]);

      if (!['A', 'B', 'C', 'D'].includes(userAns)) {
        setLines(prev => [
          ...prev,
          { text: 'Invalid input. Please enter A, B, C or D.', type: 'error' },
          { text: 'Enter your answer (A/B/C/D): ', type: 'system' }
        ]);
        return;
      }

      const q = activeQuestions[currentIdx];
      const isCorrect = userAns === q.answer;

      let newScore = score;
      let newMissed = [...missedQuestions];

      if (isCorrect) {
        newScore += 1;
        setScore(newScore);
        setLines(prev => [...prev, { text: 'Correct!', type: 'success' }]);
      } else {
        newMissed.push({ ...q, userAnswer: userAns });
        setMissedQuestions(newMissed);
        setLines(prev => [
          ...prev, 
          { text: `Wrong! The correct answer is ${q.answer}. ${q.correctText}`, type: 'error' }
        ]);
      }

      // Tip explanation (matching original line 194)
      setLines(prev => [...prev, { text: `Tip: ${q.explanation}`, type: 'tip' }]);

      const nextIdx = currentIdx + 1;
      if (nextIdx < totalCount) {
        setCurrentIdx(nextIdx);
        printQuestion(activeQuestions[nextIdx], nextIdx, totalCount);
      } else {
        // Round Finished
        finishRound(newScore, totalCount, newMissed);
      }

    } else if (phase === 'ask_replay') {
      setLines(prev => [...prev, { text: raw, type: 'input' }]);
      if (raw.toLowerCase() === 'y') {
        initGame();
      } else {
        setLines(prev => [
          ...prev,
          { text: 'Thanks for playing!', type: 'success' },
          { text: '\nType "exit" to switch to GUI or "reset" to start over.', type: 'system' }
        ]);
        setPhase('finished');
      }
    } else if (phase === 'finished') {
      setLines(prev => [...prev, { text: raw, type: 'input' }]);
      if (raw.toLowerCase() === 'exit') {
        onExitTerminal();
      } else {
        initGame();
      }
    }
  };

  const finishRound = (finalScore: number, total: number, missed: ShuffledQuestion[]) => {
    const percent = Math.round((finalScore / total) * 100);
    const summaryLines: TerminalLine[] = [
      { text: '\n' + '='.repeat(40), type: 'header' },
      { text: `Your final score is ${finalScore}/${total} (${percent}%)`, type: 'header' }
    ];

    if (percent === 100) {
      summaryLines.push({ text: 'Perfect! You really know your stuff.', type: 'success' });
    } else if (percent >= 70) {
      summaryLines.push({ text: 'Great job! Keep it up.', type: 'success' });
    } else if (percent >= 40) {
      summaryLines.push({ text: 'Not bad - review the tips and try again.', type: 'output' });
    } else {
      summaryLines.push({ text: 'Keep practicing - every attempt makes you better!', type: 'output' });
    }

    if (missed.length > 0) {
      summaryLines.push({ text: '\nTopics to review:', type: 'header' });
      missed.forEach(q => {
        summaryLines.push({
          text: `  - [${q.category}] ${q.question} -> ${q.correctText}`,
          type: 'output'
        });
      });
    }

    summaryLines.push({ text: '\nPlay again? (y/n): ', type: 'system' });

    setLines(prev => [...prev, ...summaryLines]);
    setPhase('ask_replay');
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      {/* Terminal window shell */}
      <div 
        className="rounded-2xl border border-slate-700 bg-slate-950 shadow-2xl overflow-hidden font-mono text-xs sm:text-sm"
        onClick={() => inputRef.current?.focus()}
      >
        {/* Terminal Title Bar */}
        <div className="bg-slate-900 border-b border-slate-800 px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-rose-500/80" />
            <div className="w-3 h-3 rounded-full bg-amber-500/80" />
            <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
            <span className="text-slate-400 text-xs ml-2 font-mono flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5 text-emerald-400" />
              bash - python3 "QUIZ GAME.py"
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                initGame();
              }}
              className="px-2 py-1 text-[11px] text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded transition-colors flex items-center gap-1"
              title="Restart CLI Session"
            >
              <RefreshCw className="w-3 h-3" />
              <span>Reset</span>
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onExitTerminal();
              }}
              className="px-2 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-200 rounded transition-colors"
            >
              Exit to GUI
            </button>
          </div>
        </div>

        {/* Terminal Content Screen */}
        <div className="p-4 sm:p-6 min-h-[480px] max-h-[640px] overflow-y-auto space-y-1 text-slate-200 leading-relaxed selection:bg-emerald-500/30">
          {lines.map((line, index) => {
            let colorClass = 'text-slate-300';
            if (line.type === 'system') colorClass = 'text-emerald-400 font-medium';
            if (line.type === 'header') colorClass = 'text-indigo-300 font-bold';
            if (line.type === 'success') colorClass = 'text-emerald-300 font-semibold';
            if (line.type === 'error') colorClass = 'text-rose-400 font-semibold';
            if (line.type === 'tip') colorClass = 'text-amber-300/90 italic';
            if (line.type === 'input') colorClass = 'text-sky-300 font-semibold';

            return (
              <div key={index} className={`whitespace-pre-wrap break-words ${colorClass}`}>
                {line.text}
              </div>
            );
          })}

          {/* Interactive Input Line */}
          <form onSubmit={handleInputSubmit} className="flex items-center gap-2 pt-2">
            <span className="text-emerald-400 font-bold">&gt;</span>
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              autoFocus
              className="flex-1 bg-transparent border-none outline-none text-sky-300 font-mono text-xs sm:text-sm caret-emerald-400 p-0"
              placeholder={phase === 'ask_answer' ? 'Type A, B, C, or D' : ''}
            />
            <button
              type="submit"
              className="text-slate-500 hover:text-slate-300 p-1"
              title="Send"
            >
              <CornerDownLeft className="w-3.5 h-3.5" />
            </button>
          </form>

          <div ref={terminalEndRef} />
        </div>
      </div>

      <div className="mt-3 text-center text-xs text-slate-500 font-mono">
        Authentic Python CLI emulation with real A-D response parsing & score evaluation.
      </div>
    </div>
  );
};
