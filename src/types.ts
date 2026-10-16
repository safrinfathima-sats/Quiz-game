export interface QuestionBankItem {
  id: string;
  category: string;
  question: string;
  correctAnswer: string;
  wrongAnswers: string[];
  explanation: string;
}

export interface ShuffledQuestion {
  id: string;
  category: string;
  question: string;
  options: string[];
  answer: 'A' | 'B' | 'C' | 'D';
  correctText: string;
  explanation: string;
  userAnswer?: 'A' | 'B' | 'C' | 'D';
  isCorrect?: boolean;
}

export type QuizStatus = 'setup' | 'in_progress' | 'completed';

export interface QuizSettings {
  category: string;
  questionCount: number;
}
