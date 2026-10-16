import React, { useState, useMemo, useCallback } from 'react';
import { Header } from './components/Header';
import { SetupScreen } from './components/SetupScreen';
import { QuizCard } from './components/QuizCard';
import { ResultScreen } from './components/ResultScreen';
import { TerminalView } from './components/TerminalView';
import { QUESTION_BANK, buildShuffledQuestion, shuffleArray } from './data/questions';
import { ShuffledQuestion, QuizStatus } from './types';

export const App: React.FC = () => {
  const [viewMode, setViewMode] = useState<'gui' | 'terminal'>('gui');
  const [status, setStatus] = useState<QuizStatus>('setup');
  
  // Settings
  const [selectedCategory, setSelectedCategory] = useState<string>('All Categories');
  const [questionCount, setQuestionCount] = useState<number>(10);

  // Active Quiz State
  const [questions, setQuestions] = useState<ShuffledQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [selectedAnswer, setSelectedAnswer] = useState<'A' | 'B' | 'C' | 'D' | undefined>(undefined);
  const [score, setScore] = useState<number>(0);

  // Available questions in the selected category
  const filteredBank = useMemo(() => {
    if (selectedCategory === 'All Categories') {
      return QUESTION_BANK;
    }
    return QUESTION_BANK.filter(q => q.category === selectedCategory);
  }, [selectedCategory]);

  // Start a new round
  const startQuiz = useCallback((countOverride?: number) => {
    const countToUse = countOverride || Math.min(questionCount, filteredBank.length);
    const shuffledItems = shuffleArray([...filteredBank]).slice(0, countToUse);
    const preparedQuestions = shuffledItems.map(item => buildShuffledQuestion(item));

    setQuestions(preparedQuestions);
    setCurrentIndex(0);
    setSelectedAnswer(undefined);
    setScore(0);
    setStatus('in_progress');
  }, [filteredBank, questionCount]);

  // Handle answering
  const handleSelectAnswer = useCallback((letter: 'A' | 'B' | 'C' | 'D') => {
    if (selectedAnswer !== undefined || !questions[currentIndex]) return;

    const currentQ = questions[currentIndex];
    const isCorrect = letter === currentQ.answer;

    setSelectedAnswer(letter);

    // Update score
    if (isCorrect) {
      setScore(prev => prev + 1);
    }

    // Save answer state onto question object
    setQuestions(prev => {
      const copy = [...prev];
      copy[currentIndex] = {
        ...copy[currentIndex],
        userAnswer: letter,
        isCorrect
      };
      return copy;
    });
  }, [selectedAnswer, questions, currentIndex]);

  // Next question or view results
  const handleNextQuestion = useCallback(() => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(prev => prev + 1);
      setSelectedAnswer(undefined);
    } else {
      setStatus('completed');
    }
  }, [currentIndex, questions.length]);

  // Retry missed questions
  const handleRetryMissed = useCallback(() => {
    const missed = questions.filter(q => !q.isCorrect);
    if (missed.length === 0) return;

    // Reshuffle options for the retry
    const retryPrepared = missed.map(q => {
      const originalItem = QUESTION_BANK.find(item => item.id === q.id);
      return originalItem ? buildShuffledQuestion(originalItem) : buildShuffledQuestion({
        id: q.id,
        category: q.category,
        question: q.question,
        correctAnswer: q.correctText,
        wrongAnswers: q.options.filter(opt => opt !== q.correctText),
        explanation: q.explanation
      });
    });

    setQuestions(retryPrepared);
    setCurrentIndex(0);
    setSelectedAnswer(undefined);
    setScore(0);
    setStatus('in_progress');
  }, [questions]);

  // Reset to setup screen
  const handleResetToSetup = useCallback(() => {
    setStatus('setup');
    setSelectedAnswer(undefined);
    setCurrentIndex(0);
    setScore(0);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Navigation Header */}
      <Header
        mode={viewMode}
        onToggleMode={() => setViewMode(prev => prev === 'gui' ? 'terminal' : 'gui')}
        onReset={handleResetToSetup}
        inQuiz={status === 'in_progress'}
        score={score}
        totalAnswered={currentIndex + (selectedAnswer !== undefined ? 1 : 0)}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col justify-center">
        {viewMode === 'terminal' ? (
          <TerminalView onExitTerminal={() => setViewMode('gui')} />
        ) : (
          <>
            {status === 'setup' && (
              <SetupScreen
                category={selectedCategory}
                questionCount={questionCount}
                onCategoryChange={setSelectedCategory}
                onCountChange={setQuestionCount}
                onStartQuiz={() => startQuiz()}
                onStartTerminalMode={() => setViewMode('terminal')}
              />
            )}

            {status === 'in_progress' && questions[currentIndex] && (
              <QuizCard
                question={questions[currentIndex]}
                currentIndex={currentIndex}
                totalQuestions={questions.length}
                selectedAnswer={selectedAnswer}
                onSelectAnswer={handleSelectAnswer}
                onNextQuestion={handleNextQuestion}
                isLastQuestion={currentIndex === questions.length - 1}
              />
            )}

            {status === 'completed' && (
              <ResultScreen
                score={score}
                total={questions.length}
                questions={questions}
                onPlayAgain={() => startQuiz()}
                onRetryMissed={handleRetryMissed}
                onNewSettings={handleResetToSetup}
              />
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-4 text-center text-xs text-slate-500">
        <div className="max-w-5xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Technical Quiz Game • Ported from Python to React & Tailwind CSS</span>
          <span>47 Questions • Python, DSA, Web, Databases, Git, CS Basics, Trivia</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
