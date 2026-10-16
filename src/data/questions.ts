import { QuestionBankItem } from '../types';

export const QUESTION_BANK: QuestionBankItem[] = [
  // ---------------- Python ----------------
  {
    id: 'py-1',
    category: 'Python',
    question: 'Which keyword is used to define a function in Python?',
    correctAnswer: 'def',
    wrongAnswers: ['func', 'function', 'define'],
    explanation: "Functions in Python are defined with the 'def' keyword."
  },
  {
    id: 'py-2',
    category: 'Python',
    question: 'Which of these data types is immutable?',
    correctAnswer: 'tuple',
    wrongAnswers: ['list', 'dict', 'set'],
    explanation: 'Tuples cannot be changed after creation; lists, dicts and sets can.'
  },
  {
    id: 'py-3',
    category: 'Python',
    question: 'What does the // operator do?',
    correctAnswer: 'Floor division',
    wrongAnswers: ['Exponentiation', 'Modulus', 'Regular division'],
    explanation: '7 // 2 gives 3 - the result is rounded down to the nearest whole number.'
  },
  {
    id: 'py-4',
    category: 'Python',
    question: 'What is the output of print(2 ** 3)?',
    correctAnswer: '8',
    wrongAnswers: ['6', '9', '5'],
    explanation: '** is the exponent operator, so 2 ** 3 = 2 x 2 x 2 = 8.'
  },
  {
    id: 'py-5',
    category: 'Python',
    question: 'Which list method adds an item to the end of a list?',
    correctAnswer: 'append()',
    wrongAnswers: ['add()', 'push()', 'insert_end()'],
    explanation: 'list.append(x) adds x to the end of the list.'
  },
  {
    id: 'py-6',
    category: 'Python',
    question: 'What is a decorator in Python?',
    correctAnswer: 'A function that modifies the behavior of another function',
    wrongAnswers: ['A way to style output', 'A type of loop', 'A built-in data type'],
    explanation: 'Decorators wrap a function to extend its behavior, e.g. @staticmethod.'
  },
  {
    id: 'py-7',
    category: 'Python',
    question: 'Which block is used to handle exceptions in Python?',
    correctAnswer: 'try / except',
    wrongAnswers: ['do / catch', 'begin / rescue', 'check / error'],
    explanation: 'Python uses try/except (and optionally else/finally).'
  },
  {
    id: 'py-8',
    category: 'Python',
    question: 'What does PEP 8 describe?',
    correctAnswer: 'The Python style guide',
    wrongAnswers: ["Python's package manager", "Python's memory model", "The Python license"],
    explanation: 'PEP 8 is the official style guide for writing readable Python code.'
  },
  {
    id: 'py-9',
    category: 'Python',
    question: 'What is the output of print(bool([]))?',
    correctAnswer: 'False',
    wrongAnswers: ['True', 'None', 'Error'],
    explanation: "Empty collections are 'falsy' in Python."
  },
  {
    id: 'py-10',
    category: 'Python',
    question: 'Which keyword creates a generator function?',
    correctAnswer: 'yield',
    wrongAnswers: ['return', 'generate', 'async'],
    explanation: "'yield' pauses the function and produces a value lazily."
  },

  // ---------------- Data Structures & Algorithms ----------------
  {
    id: 'dsa-1',
    category: 'DSA',
    question: 'What is the time complexity of binary search?',
    correctAnswer: 'O(log n)',
    wrongAnswers: ['O(n)', 'O(n log n)', 'O(1)'],
    explanation: 'Binary search halves the search space each step.'
  },
  {
    id: 'dsa-2',
    category: 'DSA',
    question: 'Which data structure follows the LIFO principle?',
    correctAnswer: 'Stack',
    wrongAnswers: ['Queue', 'Linked list', 'Heap'],
    explanation: 'Last In, First Out - the last item pushed is the first popped.'
  },
  {
    id: 'dsa-3',
    category: 'DSA',
    question: 'Which data structure follows the FIFO principle?',
    correctAnswer: 'Queue',
    wrongAnswers: ['Stack', 'Tree', 'Graph'],
    explanation: 'First In, First Out - like a line of people waiting.'
  },
  {
    id: 'dsa-4',
    category: 'DSA',
    question: 'What is the average time complexity of a hash table lookup?',
    correctAnswer: 'O(1)',
    wrongAnswers: ['O(n)', 'O(log n)', 'O(n^2)'],
    explanation: 'Hashing lets you jump straight to the bucket, so lookups are constant time on average.'
  },
  {
    id: 'dsa-5',
    category: 'DSA',
    question: 'Which sorting algorithm guarantees O(n log n) even in the worst case?',
    correctAnswer: 'Merge sort',
    wrongAnswers: ['Quick sort', 'Bubble sort', 'Insertion sort'],
    explanation: 'Quick sort can degrade to O(n^2); merge sort is always O(n log n).'
  },
  {
    id: 'dsa-6',
    category: 'DSA',
    question: 'Which graph traversal algorithm uses a queue?',
    correctAnswer: 'Breadth-First Search (BFS)',
    wrongAnswers: ['Depth-First Search (DFS)', 'Dijkstra with a stack', 'Binary search'],
    explanation: 'BFS explores level by level using a queue; DFS uses a stack/recursion.'
  },
  {
    id: 'dsa-7',
    category: 'DSA',
    question: 'How many children can a node in a binary tree have at most?',
    correctAnswer: '2',
    wrongAnswers: ['1', '3', 'Unlimited'],
    explanation: "'Binary' means each node has at most two children (left and right)."
  },
  {
    id: 'dsa-8',
    category: 'DSA',
    question: 'What data structure does the system use to track function calls?',
    correctAnswer: 'Call stack',
    wrongAnswers: ['Heap', 'Queue', 'Hash table'],
    explanation: 'Each function call is pushed onto the call stack and popped on return.'
  },

  // ---------------- Web & Networking ----------------
  {
    id: 'web-1',
    category: 'Web',
    question: "Which HTTP status code means 'Not Found'?",
    correctAnswer: '404',
    wrongAnswers: ['200', '403', '500'],
    explanation: "404 means the server can't find the requested resource."
  },
  {
    id: 'web-2',
    category: 'Web',
    question: "Which HTTP status code means 'Internal Server Error'?",
    correctAnswer: '500',
    wrongAnswers: ['401', '404', '301'],
    explanation: '5xx codes indicate a server-side problem.'
  },
  {
    id: 'web-3',
    category: 'Web',
    question: 'What is the default port for HTTPS?',
    correctAnswer: '443',
    wrongAnswers: ['80', '21', '8080'],
    explanation: 'HTTP uses 80, HTTPS uses 443.'
  },
  {
    id: 'web-4',
    category: 'Web',
    question: 'What does DNS do?',
    correctAnswer: 'Translates domain names into IP addresses',
    wrongAnswers: ['Encrypts web traffic', 'Stores website files', 'Assigns MAC addresses'],
    explanation: "DNS is the internet's phone book for domain names."
  },
  {
    id: 'web-5',
    category: 'Web',
    question: 'Which HTTP method is normally used to retrieve data without changing it?',
    correctAnswer: 'GET',
    wrongAnswers: ['POST', 'DELETE', 'PUT'],
    explanation: 'GET is safe and idempotent - it only reads data.'
  },
  {
    id: 'web-6',
    category: 'Web',
    question: 'What does API stand for?',
    correctAnswer: 'Application Programming Interface',
    wrongAnswers: ['Applied Program Integration', 'Automated Process Interface', 'Application Protocol Index'],
    explanation: 'An API defines how software components talk to each other.'
  },
  {
    id: 'web-7',
    category: 'Web',
    question: 'What does JSON stand for?',
    correctAnswer: 'JavaScript Object Notation',
    wrongAnswers: ['Java Standard Output Network', 'JavaScript Online Node', 'Joint Syntax Object Name'],
    explanation: 'JSON is a lightweight text format for exchanging data.'
  },
  {
    id: 'web-8',
    category: 'Web',
    question: 'Which protocol is commonly used to securely log into a remote machine?',
    correctAnswer: 'SSH',
    wrongAnswers: ['FTP', 'Telnet', 'SMTP'],
    explanation: 'SSH (Secure Shell) encrypts the connection, unlike Telnet.'
  },

  // ---------------- Databases ----------------
  {
    id: 'db-1',
    category: 'Databases',
    question: 'Which SQL command is used to retrieve data from a table?',
    correctAnswer: 'SELECT',
    wrongAnswers: ['GET', 'FETCH', 'EXTRACT'],
    explanation: 'SELECT is the core SQL query command.'
  },
  {
    id: 'db-2',
    category: 'Databases',
    question: 'What is a primary key?',
    correctAnswer: 'A column that uniquely identifies each row',
    wrongAnswers: ['A column that stores passwords', 'The first column in a table', 'An index that allows duplicates'],
    explanation: 'Primary keys must be unique and not NULL.'
  },
  {
    id: 'db-3',
    category: 'Databases',
    question: 'Which JOIN returns only the rows that have matches in both tables?',
    correctAnswer: 'INNER JOIN',
    wrongAnswers: ['LEFT JOIN', 'FULL OUTER JOIN', 'CROSS JOIN'],
    explanation: 'INNER JOIN keeps only matching rows.'
  },
  {
    id: 'db-4',
    category: 'Databases',
    question: "In ACID, what does the 'A' stand for?",
    correctAnswer: 'Atomicity',
    wrongAnswers: ['Availability', 'Accuracy', 'Authorization'],
    explanation: 'Atomicity means a transaction either fully completes or not at all.'
  },
  {
    id: 'db-5',
    category: 'Databases',
    question: 'Which of these is a NoSQL database?',
    correctAnswer: 'MongoDB',
    wrongAnswers: ['MySQL', 'PostgreSQL', 'SQLite'],
    explanation: 'MongoDB is a document-oriented NoSQL database.'
  },

  // ---------------- Git & DevOps ----------------
  {
    id: 'git-1',
    category: 'Git & DevOps',
    question: 'Which command creates a local copy of a remote repository?',
    correctAnswer: 'git clone',
    wrongAnswers: ['git copy', 'git pull', 'git fork'],
    explanation: 'git clone downloads the full repository and its history.'
  },
  {
    id: 'git-2',
    category: 'Git & DevOps',
    question: "What does 'git commit' do?",
    correctAnswer: 'Saves staged changes to the local repository',
    wrongAnswers: ['Uploads changes to GitHub', 'Creates a new branch', 'Downloads remote changes'],
    explanation: "Committing records a snapshot locally; 'git push' sends it to the remote."
  },
  {
    id: 'git-3',
    category: 'Git & DevOps',
    question: "'git pull' is a combination of which two commands?",
    correctAnswer: 'git fetch + git merge',
    wrongAnswers: ['git add + git commit', 'git clone + git push', 'git stash + git apply'],
    explanation: 'Pull fetches remote changes and merges them into your branch.'
  },
  {
    id: 'git-4',
    category: 'Git & DevOps',
    question: 'What does CI/CD stand for?',
    correctAnswer: 'Continuous Integration / Continuous Delivery',
    wrongAnswers: ['Code Inspection / Code Debugging', 'Central Integration / Central Deployment', 'Compiled Instructions / Compiled Data'],
    explanation: 'CI/CD automates building, testing and releasing software.'
  },

  // ---------------- CS Fundamentals ----------------
  {
    id: 'cs-1',
    category: 'CS Basics',
    question: 'What is the binary representation of decimal 10?',
    correctAnswer: '1010',
    wrongAnswers: ['1001', '1100', '1110'],
    explanation: '8 + 2 = 10, so the bits are 1010.'
  },
  {
    id: 'cs-2',
    category: 'CS Basics',
    question: 'How many bits are in one byte?',
    correctAnswer: '8',
    wrongAnswers: ['4', '16', '10'],
    explanation: '1 byte = 8 bits.'
  },
  {
    id: 'cs-3',
    category: 'CS Basics',
    question: 'What does a compiler do?',
    correctAnswer: 'Translates source code into machine code',
    wrongAnswers: ['Runs code line by line', 'Fixes bugs automatically', 'Stores variables in memory'],
    explanation: 'A compiler converts the whole program before it runs; an interpreter runs it line by line.'
  },
  {
    id: 'cs-4',
    category: 'CS Basics',
    question: 'What does the DRY principle stand for?',
    correctAnswer: "Don't Repeat Yourself",
    wrongAnswers: ['Debug, Run, Yield', 'Data Reduction Yield', 'Do Recursion Yearly'],
    explanation: 'DRY encourages reusing code instead of duplicating logic.'
  },
  {
    id: 'cs-5',
    category: 'CS Basics',
    question: "What does 'encapsulation' mean in OOP?",
    correctAnswer: 'Bundling data and methods together and restricting direct access',
    wrongAnswers: ['Creating a new class from an existing one', 'Using one interface for many types', 'Converting objects to text'],
    explanation: "Encapsulation hides internal state behind a class's methods."
  },
  {
    id: 'cs-6',
    category: 'CS Basics',
    question: 'RAM is best described as which type of memory?',
    correctAnswer: 'Volatile, temporary memory',
    wrongAnswers: ['Permanent storage', 'Read-only memory', 'Cloud memory'],
    explanation: 'RAM loses its contents when the power is turned off.'
  },
  {
    id: 'cs-7',
    category: 'CS Basics',
    question: 'Which of these is an operating system kernel?',
    correctAnswer: 'Linux',
    wrongAnswers: ['Python', 'Oracle', 'Chrome'],
    explanation: 'Linux is a kernel; Python is a language, Oracle a database, Chrome a browser.'
  },

  // ---------------- General Trivia (from quiz_game.py) ----------------
  {
    id: 'gen-1',
    category: 'General Trivia',
    question: 'Which planet is known as the Red Planet?',
    correctAnswer: 'Mars',
    wrongAnswers: ['Venus', 'Jupiter', 'Saturn'],
    explanation: 'Mars appears reddish because of widespread iron oxide (rust) on its surface.'
  },
  {
    id: 'gen-2',
    category: 'General Trivia',
    question: 'Which language is used to create this original program?',
    correctAnswer: 'Python',
    wrongAnswers: ['C++', 'Java', 'Ruby'],
    explanation: 'The original quiz game repository was authored in Python.'
  },
  {
    id: 'gen-3',
    category: 'General Trivia',
    question: 'What is the boiling point of water at sea level (in °C)?',
    correctAnswer: '100',
    wrongAnswers: ['90', '110', '120'],
    explanation: 'Pure water boils at 100°C (212°F) at standard atmospheric pressure (1 atm).'
  },
  {
    id: 'gen-4',
    category: 'General Trivia',
    question: "Which animal is known as the 'King of the Jungle'?",
    correctAnswer: 'Lion',
    wrongAnswers: ['Tiger', 'Elephant', 'Bear'],
    explanation: "The lion is traditionally dubbed the 'King of the Jungle' for its regal pride and top-predator status."
  },
  {
    id: 'gen-5',
    category: 'General Trivia',
    question: 'How many continents are there on Earth?',
    correctAnswer: '7',
    wrongAnswers: ['5', '6', '8'],
    explanation: 'Earth has 7 continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia.'
  }
];

export const CATEGORIES = [
  'All Categories',
  'Python',
  'DSA',
  'Web',
  'Databases',
  'Git & DevOps',
  'CS Basics',
  'General Trivia'
] as const;

export const LETTERS: readonly ('A' | 'B' | 'C' | 'D')[] = ['A', 'B', 'C', 'D'];

export function shuffleArray<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

export function buildShuffledQuestion(item: QuestionBankItem): import('../types').ShuffledQuestion {
  const options = shuffleArray([...item.wrongAnswers, item.correctAnswer]);
  const correctIndex = options.indexOf(item.correctAnswer);
  const answer = LETTERS[correctIndex] || 'A';

  return {
    id: item.id,
    category: item.category,
    question: item.question,
    options,
    answer,
    correctText: item.correctAnswer,
    explanation: item.explanation
  };
}
