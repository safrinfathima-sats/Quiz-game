import os
import random
from flask import Flask, jsonify, request, render_template_string

from quiz_game import QUESTION_BANK, build_question, LETTERS

app = Flask(__name__)

# Categories list
CATEGORIES = sorted(list({entry[0] for entry in QUESTION_BANK}))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Technical Quiz Game</title>
  <meta name="description" content="Interactive technical quiz covering Python, Data Structures, Web, Databases, Git, and Computer Science fundamentals.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            display: ['Outfit', 'sans-serif'],
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            slate: {
              850: '#151d2e',
              900: '#0f172a',
              950: '#090d16',
            }
          }
        }
      }
    }
  </script>
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .font-display {
      font-family: 'Outfit', sans-serif;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    .tabular-nums {
      font-variant-numeric: tabular-nums;
    }
    /* Smooth button transitions */
    .option-btn {
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }
    /* Subtle scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-full flex flex-col antialiased selection:bg-emerald-500/20 selection:text-emerald-300">

  <!-- Top Bar Contract: 3 zones, gap-8, single line -->
  <header class="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-8">
      <!-- Zone 1: Single Brand Wordmark -->
      <a href="/" class="flex items-center gap-2.5 text-lg font-bold tracking-tight text-white font-display whitespace-nowrap shrink-0 hover:text-emerald-400 transition-colors">
        <svg class="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="16 18 22 12 16 6"></polyline>
          <polyline points="8 6 2 12 8 18"></polyline>
        </svg>
        <span>Technical Quiz</span>
      </a>

      <!-- Zone 2: Navigation Links -->
      <nav class="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
        <button onclick="setView('play')" id="nav-play" class="hover:text-white transition-colors whitespace-nowrap shrink-0 text-emerald-400 font-semibold">Play Quiz</button>
        <button onclick="setView('browse')" id="nav-browse" class="hover:text-white transition-colors whitespace-nowrap shrink-0">Question Bank (<span id="total-q-badge" class="font-mono">{{ total_questions }}</span>)</button>
        <button onclick="setView('stats')" id="nav-stats" class="hover:text-white transition-colors whitespace-nowrap shrink-0">Session Stats</button>
      </nav>

      <!-- Zone 3: Primary Action -->
      <div class="flex items-center gap-3 shrink-0">
        <button onclick="resetToSetup()" class="px-4 py-2 text-xs font-semibold text-slate-950 bg-emerald-400 hover:bg-emerald-300 rounded-lg transition-colors whitespace-nowrap shrink-0 active:scale-95 shadow-sm shadow-emerald-500/10">
          New Round
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-8 flex flex-col justify-center">

    <!-- VIEW 1: QUIZ SETUP -->
    <section id="view-setup" class="space-y-6">
      <div class="text-center space-y-2 max-w-xl mx-auto">
        <h1 class="text-3xl sm:text-4xl font-bold font-display tracking-tight text-white">
          Sharpen Your Core Technical Knowledge
        </h1>
        <p class="text-sm sm:text-base text-slate-400 leading-relaxed">
          Test and reinforce your understanding of Python, Data Structures, Web, Databases, Git, and Computer Science fundamentals.
        </p>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl">
        <!-- Category Filter -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-semibold text-slate-200">Category Selection</label>
            <span id="category-count-hint" class="text-xs text-slate-400 font-mono">All ({{ total_questions }} questions)</span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2" id="category-selector">
            <button onclick="selectCategory('All')" data-cat="All" class="cat-pill active text-left px-3.5 py-2.5 rounded-lg border text-xs font-medium transition-all bg-emerald-500/15 border-emerald-500/50 text-emerald-300">
              <span class="block font-semibold">All Topics</span>
              <span class="text-[11px] text-slate-400">{{ total_questions }} questions</span>
            </button>
            {% for cat in categories %}
            <button onclick="selectCategory('{{ cat }}')" data-cat="{{ cat }}" class="cat-pill text-left px-3.5 py-2.5 rounded-lg border text-xs font-medium transition-all bg-slate-850/60 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white">
              <span class="block font-semibold truncate">{{ cat }}</span>
              <span class="text-[11px] text-slate-400">{{ category_counts[cat] }} questions</span>
            </button>
            {% endfor %}
          </div>
        </div>

        <!-- Question Count -->
        <div class="space-y-3 pt-4 border-t border-slate-800">
          <div class="flex items-center justify-between">
            <label class="text-sm font-semibold text-slate-200">Number of Questions</label>
            <span id="count-display" class="text-xs font-mono font-semibold text-emerald-400">10 Questions</span>
          </div>
          <div class="grid grid-cols-4 gap-2">
            <button onclick="selectCount(5)" data-count="5" class="count-pill py-2 text-xs font-medium rounded-lg border border-slate-800 bg-slate-850/60 text-slate-300 hover:border-slate-700">5</button>
            <button onclick="selectCount(10)" data-count="10" class="count-pill active py-2 text-xs font-medium rounded-lg border border-emerald-500/50 bg-emerald-500/15 text-emerald-300">10</button>
            <button onclick="selectCount(20)" data-count="20" class="count-pill py-2 text-xs font-medium rounded-lg border border-slate-800 bg-slate-850/60 text-slate-300 hover:border-slate-700">20</button>
            <button onclick="selectCount('max')" data-count="max" class="count-pill py-2 text-xs font-medium rounded-lg border border-slate-800 bg-slate-850/60 text-slate-300 hover:border-slate-700">All</button>
          </div>
        </div>

        <!-- Options / Preferences -->
        <div class="pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
          <label class="flex items-center gap-2 cursor-pointer select-none">
            <input type="checkbox" id="sound-toggle" checked class="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-emerald-500">
            <span>Sound effects (synthesized audio chimes)</span>
          </label>
          <span class="text-slate-400">Keyboard shortcuts: <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-[11px] font-mono text-slate-300">A</kbd> <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-[11px] font-mono text-slate-300">B</kbd> <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-[11px] font-mono text-slate-300">C</kbd> <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-[11px] font-mono text-slate-300">D</kbd></span>
        </div>

        <!-- Start CTA -->
        <button onclick="startQuiz()" class="w-full py-3.5 px-6 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm tracking-wide transition-all shadow-lg shadow-emerald-500/20 active:scale-[0.99] flex items-center justify-center gap-2">
          <span>Start Quiz Session</span>
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </div>
    </section>

    <!-- VIEW 2: ACTIVE QUIZ -->
    <section id="view-quiz" class="hidden space-y-6">
      <!-- Quiz Progress Header -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
        <div class="flex items-center justify-between text-xs text-slate-400">
          <div class="flex items-center gap-2">
            <span id="quiz-cat-label" class="font-semibold text-slate-200">Python</span>
            <span aria-hidden="true">·</span>
            <span>Question <span id="quiz-current-num" class="font-mono text-white font-semibold">1</span> of <span id="quiz-total-num" class="font-mono">10</span></span>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-1.5">
              <span class="text-slate-400">Score:</span>
              <span id="quiz-live-score" class="font-mono font-bold text-emerald-400 tabular-nums">0</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="text-slate-400">Streak:</span>
              <span id="quiz-live-streak" class="font-mono font-semibold text-amber-400 tabular-nums">0</span>
            </div>
          </div>
        </div>
        <!-- Progress bar -->
        <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
          <div id="quiz-progress-bar" class="bg-emerald-500 h-full transition-all duration-300" style="width: 10%;"></div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl">
        <div class="space-y-2">
          <span id="quiz-badge" class="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold">Multiple Choice</span>
          <h2 id="quiz-question-text" class="text-xl sm:text-2xl font-bold font-display text-white leading-snug">
            Question loading...
          </h2>
        </div>

        <!-- Options List -->
        <div id="quiz-options-container" class="space-y-3">
          <!-- Populated by JS -->
        </div>

        <!-- Feedback / Explanation Panel (Visible after answering) -->
        <div id="quiz-feedback-panel" class="hidden rounded-xl p-4 border transition-all space-y-3">
          <div class="flex items-start gap-3">
            <div id="quiz-feedback-icon" class="w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs"></div>
            <div class="space-y-1">
              <p id="quiz-feedback-title" class="text-sm font-bold"></p>
              <p id="quiz-feedback-explanation" class="text-xs sm:text-sm text-slate-300 leading-relaxed"></p>
            </div>
          </div>
          <div class="pt-2 flex justify-end">
            <button id="quiz-next-btn" onclick="nextQuestion()" class="px-5 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs tracking-wide transition-all flex items-center gap-1.5">
              <span id="quiz-next-label">Next Question</span>
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 3: RESULTS SCREEN -->
    <section id="view-results" class="hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 text-center shadow-xl">
        <div class="space-y-2">
          <span class="text-xs font-mono uppercase tracking-wider text-slate-400">Session Complete</span>
          <h2 id="results-headline" class="text-3xl font-bold font-display text-white">Great Job!</h2>
          <p id="results-subtext" class="text-sm text-slate-400 max-w-md mx-auto"></p>
        </div>

        <!-- Score Ring / KPI Grid -->
        <div class="grid grid-cols-3 gap-3 max-w-md mx-auto pt-2 pb-2">
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Score</div>
            <div id="results-score-fraction" class="text-xl sm:text-2xl font-bold font-mono text-emerald-400 tabular-nums">8/10</div>
          </div>
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Accuracy</div>
            <div id="results-percentage" class="text-xl sm:text-2xl font-bold font-mono text-white tabular-nums">80%</div>
          </div>
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Best Streak</div>
            <div id="results-max-streak" class="text-xl sm:text-2xl font-bold font-mono text-amber-400 tabular-nums">6</div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button onclick="restartRound()" class="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs tracking-wide transition-all shadow-md shadow-emerald-500/10">
            Play Another Round
          </button>
          <button id="results-retry-missed-btn" onclick="retryMissedQuestions()" class="hidden px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs tracking-wide transition-all border border-slate-700">
            Practice Missed (<span id="results-missed-count">0</span>)
          </button>
          <button onclick="resetToSetup()" class="px-5 py-2.5 rounded-xl bg-slate-850 hover:bg-slate-800 text-slate-300 font-medium text-xs tracking-wide transition-all border border-slate-800">
            Change Settings
          </button>
        </div>
      </div>

      <!-- Topics to Review Container -->
      <div id="results-review-section" class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-4 shadow-xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold font-display text-white">Topics to Review</h3>
          <span class="text-xs text-slate-400 font-mono">Answers & Tips</span>
        </div>
        <div id="results-review-list" class="space-y-3">
          <!-- Populated by JS -->
        </div>
      </div>
    </section>

    <!-- VIEW 4: BROWSE QUESTION BANK -->
    <section id="view-browse" class="hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-2xl font-bold font-display text-white">Question Bank Directory</h2>
          <p class="text-xs sm:text-sm text-slate-400">Study, filter, or review questions and technical explanations.</p>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" id="browse-search" oninput="filterBrowseQuestions()" placeholder="Search questions..." class="px-3 py-1.5 text-xs bg-slate-900 border border-slate-800 rounded-lg text-white focus:outline-none focus:border-emerald-500 w-48 sm:w-64">
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs" id="browse-cat-filters">
        <button onclick="setBrowseCategory('All')" data-bcat="All" class="bcat-btn active px-3 py-1.5 rounded-lg border bg-emerald-500/15 border-emerald-500/50 text-emerald-300 font-semibold whitespace-nowrap">All ({{ total_questions }})</button>
        {% for cat in categories %}
        <button onclick="setBrowseCategory('{{ cat }}')" data-bcat="{{ cat }}" class="bcat-btn px-3 py-1.5 rounded-lg border bg-slate-900 border-slate-800 text-slate-300 hover:border-slate-700 whitespace-nowrap">{{ cat }} ({{ category_counts[cat] }})</button>
        {% endfor %}
      </div>

      <!-- Questions List -->
      <div id="browse-list" class="space-y-3">
        <!-- Populated by JS -->
      </div>
    </section>

    <!-- VIEW 5: STATS -->
    <section id="view-stats" class="hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl">
        <h2 class="text-2xl font-bold font-display text-white">Session Lifetime Performance</h2>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Rounds Played</div>
            <div id="stat-rounds" class="text-2xl font-bold font-mono text-white mt-1 tabular-nums">0</div>
          </div>
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Total Answered</div>
            <div id="stat-answered" class="text-2xl font-bold font-mono text-white mt-1 tabular-nums">0</div>
          </div>
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Correct Answers</div>
            <div id="stat-correct" class="text-2xl font-bold font-mono text-emerald-400 mt-1 tabular-nums">0</div>
          </div>
          <div class="bg-slate-850 border border-slate-800 rounded-xl p-4">
            <div class="text-xs text-slate-400">Overall Accuracy</div>
            <div id="stat-accuracy" class="text-2xl font-bold font-mono text-emerald-400 mt-1 tabular-nums">0%</div>
          </div>
        </div>

        <div class="pt-4 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400">
          <span>Stats are stored locally in your browser.</span>
          <button onclick="clearStats()" class="text-red-400 hover:text-red-300 transition-colors">Reset Statistics</button>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-950/80 py-4 text-center text-xs text-slate-400">
    <div class="max-w-5xl mx-auto px-4 flex items-center justify-between">
      <span>Technical Quiz Game &middot; Python, DSA, Web, Databases &amp; DevOps</span>
      <span class="font-mono">{{ total_questions }} Verified Questions</span>
    </div>
  </footer>

  <!-- Application State & Interactive Logic -->
  <script>
    // State
    const RAW_QUESTION_BANK = {{ question_bank_json | safe }};
    const CATEGORIES = {{ categories_json | safe }};

    let selectedCategory = 'All';
    let selectedCount = 10;
    let quizQuestions = [];
    let currentQuestionIdx = 0;
    let currentScore = 0;
    let currentStreak = 0;
    let maxStreak = 0;
    let answeredCurrent = false;
    let missedQuestions = [];

    // Web Audio Synthesizer
    let audioCtx = null;
    function playChime(success) {
      if (!document.getElementById('sound-toggle').checked) return;
      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (success) {
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(523.25, now); // C5
          osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.08); // E5
          osc.frequency.exponentialRampToValueAtTime(783.99, now + 0.16); // G5
          gain.gain.setValueAtTime(0.15, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc.start(now);
          osc.stop(now + 0.35);
        } else {
          osc.type = 'sine';
          osc.frequency.setValueAtTime(260, now);
          osc.frequency.exponentialRampToValueAtTime(180, now + 0.2);
          gain.gain.setValueAtTime(0.15, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
          osc.start(now);
          osc.stop(now + 0.3);
        }
      } catch (e) {
        // Audio might be blocked without gesture
      }
    }

    // Navigation
    function setView(viewName) {
      ['setup', 'quiz', 'results', 'browse', 'stats'].forEach(v => {
        const el = document.getElementById('view-' + v);
        if (el) el.classList.add('hidden');
      });
      const activeEl = document.getElementById('view-' + viewName);
      if (activeEl) activeEl.classList.remove('hidden');

      // Update Nav links
      ['play', 'browse', 'stats'].forEach(n => {
        const navEl = document.getElementById('nav-' + n);
        if (navEl) {
          navEl.classList.remove('text-emerald-400', 'font-semibold');
          navEl.classList.add('text-slate-300');
        }
      });
      const currentNav = document.getElementById('nav-' + (viewName === 'setup' || viewName === 'quiz' || viewName === 'results' ? 'play' : viewName));
      if (currentNav) {
        currentNav.classList.add('text-emerald-400', 'font-semibold');
        currentNav.classList.remove('text-slate-300');
      }

      if (viewName === 'browse') {
        renderBrowseList();
      } else if (viewName === 'stats') {
        renderStats();
      }
    }

    function resetToSetup() {
      setView('setup');
    }

    // Setup Selectors
    function selectCategory(cat) {
      selectedCategory = cat;
      document.querySelectorAll('.cat-pill').forEach(btn => {
        if (btn.getAttribute('data-cat') === cat) {
          btn.classList.add('bg-emerald-500/15', 'border-emerald-500/50', 'text-emerald-300');
          btn.classList.remove('bg-slate-850/60', 'border-slate-800', 'text-slate-300');
        } else {
          btn.classList.remove('bg-emerald-500/15', 'border-emerald-500/50', 'text-emerald-300');
          btn.classList.add('bg-slate-850/60', 'border-slate-800', 'text-slate-300');
        }
      });

      // Update count hint
      const totalAvailable = cat === 'All' 
        ? RAW_QUESTION_BANK.length 
        : RAW_QUESTION_BANK.filter(q => q[0] === cat).length;
      document.getElementById('category-count-hint').textContent = `${cat} (${totalAvailable} available)`;
    }

    function selectCount(count) {
      selectedCount = count;
      document.querySelectorAll('.count-pill').forEach(btn => {
        const c = btn.getAttribute('data-count');
        if (c == count) {
          btn.classList.add('bg-emerald-500/15', 'border-emerald-500/50', 'text-emerald-300');
          btn.classList.remove('bg-slate-850/60', 'border-slate-800', 'text-slate-300');
        } else {
          btn.classList.remove('bg-emerald-500/15', 'border-emerald-500/50', 'text-emerald-300');
          btn.classList.add('bg-slate-850/60', 'border-slate-800', 'text-slate-300');
        }
      });
      document.getElementById('count-display').textContent = count === 'max' ? 'All Questions' : `${count} Questions`;
    }

    // Shuffle helper
    function shuffle(arr) {
      const copy = [...arr];
      for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }
      return copy;
    }

    // Start Quiz
    function startQuiz(customQuestions = null) {
      if (customQuestions) {
        quizQuestions = customQuestions;
      } else {
        let pool = RAW_QUESTION_BANK;
        if (selectedCategory !== 'All') {
          pool = pool.filter(q => q[0] === selectedCategory);
        }
        const count = selectedCount === 'max' ? pool.length : Math.min(parseInt(selectedCount), pool.length);
        const shuffled = shuffle(pool).slice(0, count);

        // Transform each into question object with shuffled A-D
        quizQuestions = shuffled.map(item => {
          const [cat, text, correct, wrong, explanation] = item;
          const options = shuffle([...wrong, correct]);
          const letters = ['A', 'B', 'C', 'D'];
          const correctIdx = options.indexOf(correct);
          return {
            category: cat,
            question: text,
            options: options,
            correctLetter: letters[correctIdx],
            correctText: correct,
            explanation: explanation
          };
        });
      }

      currentQuestionIdx = 0;
      currentScore = 0;
      currentStreak = 0;
      maxStreak = 0;
      missedQuestions = [];
      answeredCurrent = false;

      setView('quiz');
      renderQuestion();
    }

    function renderQuestion() {
      answeredCurrent = false;
      const q = quizQuestions[currentQuestionIdx];
      const total = quizQuestions.length;

      document.getElementById('quiz-cat-label').textContent = q.category;
      document.getElementById('quiz-current-num').textContent = currentQuestionIdx + 1;
      document.getElementById('quiz-total-num').textContent = total;
      document.getElementById('quiz-live-score').textContent = currentScore;
      document.getElementById('quiz-live-streak').textContent = currentStreak;
      document.getElementById('quiz-progress-bar').style.width = `${((currentQuestionIdx) / total) * 100}%`;

      document.getElementById('quiz-question-text').textContent = q.question;
      document.getElementById('quiz-feedback-panel').classList.add('hidden');

      const container = document.getElementById('quiz-options-container');
      container.innerHTML = '';

      const letters = ['A', 'B', 'C', 'D'];
      q.options.forEach((optText, idx) => {
        const letter = letters[idx];
        const btn = document.createElement('button');
        btn.className = `option-btn w-full text-left p-4 rounded-xl border border-slate-800 bg-slate-850 hover:border-slate-700 hover:bg-slate-800/80 flex items-center justify-between text-sm sm:text-base font-medium text-slate-200 cursor-pointer`;
        btn.setAttribute('data-letter', letter);
        btn.onclick = () => selectAnswer(letter);

        btn.innerHTML = `
          <div class="flex items-center gap-3">
            <span class="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 font-mono text-xs font-bold text-slate-300 flex items-center justify-center shrink-0">
              ${letter}
            </span>
            <span class="option-text">${optText}</span>
          </div>
          <span class="option-icon hidden text-sm font-bold"></span>
        `;
        container.appendChild(btn);
      });
    }

    function selectAnswer(chosenLetter) {
      if (answeredCurrent) return;
      answeredCurrent = true;

      const q = quizQuestions[currentQuestionIdx];
      const isCorrect = chosenLetter === q.correctLetter;

      if (isCorrect) {
        currentScore++;
        currentStreak++;
        if (currentStreak > maxStreak) maxStreak = currentStreak;
        playChime(true);
      } else {
        currentStreak = 0;
        missedQuestions.push(q);
        playChime(false);
      }

      // Update state in storage
      recordAnswer(isCorrect);

      // Visual styling on options
      const buttons = document.querySelectorAll('#quiz-options-container .option-btn');
      buttons.forEach(btn => {
        const letter = btn.getAttribute('data-letter');
        btn.classList.remove('hover:border-slate-700', 'hover:bg-slate-800/80', 'cursor-pointer');
        btn.classList.add('cursor-default');

        const icon = btn.querySelector('.option-icon');

        if (letter === q.correctLetter) {
          btn.classList.add('bg-emerald-950/40', 'border-emerald-500', 'text-emerald-300');
          icon.innerHTML = `<span class="text-emerald-400 font-bold">&#10003; Correct</span>`;
          icon.classList.remove('hidden');
        } else if (letter === chosenLetter && !isCorrect) {
          btn.classList.add('bg-red-950/40', 'border-red-500', 'text-red-300');
          icon.innerHTML = `<span class="text-red-400 font-bold">&#10005; Your choice</span>`;
          icon.classList.remove('hidden');
        } else {
          btn.classList.add('opacity-40');
        }
      });

      // Show Feedback Card
      const panel = document.getElementById('quiz-feedback-panel');
      const icon = document.getElementById('quiz-feedback-icon');
      const title = document.getElementById('quiz-feedback-title');
      const exp = document.getElementById('quiz-feedback-explanation');

      panel.classList.remove('hidden', 'bg-emerald-950/30', 'border-emerald-500/40', 'bg-red-950/30', 'border-red-500/40');

      if (isCorrect) {
        panel.classList.add('bg-emerald-950/30', 'border-emerald-500/40');
        icon.className = 'w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
        icon.innerHTML = '&#10003;';
        title.className = 'text-sm font-bold text-emerald-300';
        title.textContent = 'Correct!';
      } else {
        panel.classList.add('bg-red-950/30', 'border-red-500/40');
        icon.className = 'w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs bg-red-500/20 text-red-400 border border-red-500/40';
        icon.innerHTML = '&#10005;';
        title.className = 'text-sm font-bold text-red-300';
        title.textContent = `Incorrect. Correct answer was ${q.correctLetter}: ${q.correctText}`;
      }

      exp.textContent = `Tip: ${q.explanation}`;

      const nextLabel = document.getElementById('quiz-next-label');
      if (currentQuestionIdx + 1 >= quizQuestions.length) {
        nextLabel.textContent = 'View Final Score';
      } else {
        nextLabel.textContent = 'Next Question';
      }
    }

    function nextQuestion() {
      if (currentQuestionIdx + 1 < quizQuestions.length) {
        currentQuestionIdx++;
        renderQuestion();
      } else {
        showResults();
      }
    }

    // Results Screen
    function showResults() {
      setView('results');
      const total = quizQuestions.length;
      const percent = Math.round((currentScore / total) * 100);

      document.getElementById('results-score-fraction').textContent = `${currentScore}/${total}`;
      document.getElementById('results-percentage').textContent = `${percent}%`;
      document.getElementById('results-max-streak').textContent = maxStreak;

      const headline = document.getElementById('results-headline');
      const subtext = document.getElementById('results-subtext');

      if (percent === 100) {
        headline.textContent = 'Flawless Victory!';
        subtext.textContent = 'You answered every question correctly. Outstanding technical mastery!';
      } else if (percent >= 80) {
        headline.textContent = 'Excellent Performance!';
        subtext.textContent = 'Strong grasp of core technical topics and architectural paradigms.';
      } else if (percent >= 60) {
        headline.textContent = 'Solid Effort!';
        subtext.textContent = 'Good foundation. Review the missed concepts below to close knowledge gaps.';
      } else {
        headline.textContent = 'Keep Practicing!';
        subtext.textContent = 'Technical mastery comes through repetition. Review the tips below and try again!';
      }

      // Review Section
      const reviewSection = document.getElementById('results-review-section');
      const reviewList = document.getElementById('results-review-list');
      const retryMissedBtn = document.getElementById('results-retry-missed-btn');

      if (missedQuestions.length > 0) {
        reviewSection.classList.remove('hidden');
        retryMissedBtn.classList.remove('hidden');
        document.getElementById('results-missed-count').textContent = missedQuestions.length;

        reviewList.innerHTML = '';
        missedQuestions.forEach(q => {
          const item = document.createElement('div');
          item.className = 'p-4 rounded-xl bg-slate-850 border border-slate-800 space-y-2';
          item.innerHTML = `
            <div class="flex items-center gap-2 text-xs text-slate-400">
              <span class="font-semibold text-slate-200">${q.category}</span>
              <span aria-hidden="true">&middot;</span>
              <span class="text-emerald-400 font-mono">Answer: ${q.correctText}</span>
            </div>
            <div class="text-sm font-semibold text-white">${q.question}</div>
            <div class="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
              <span class="font-semibold text-slate-400">Tip:</span> ${q.explanation}
            </div>
          `;
          reviewList.appendChild(item);
        });
      } else {
        reviewSection.classList.add('hidden');
        retryMissedBtn.classList.add('hidden');
      }

      recordRoundComplete();
    }

    function retryMissedQuestions() {
      if (!missedQuestions.length) return;
      const retryList = missedQuestions.map(q => {
        const letters = ['A', 'B', 'C', 'D'];
        const options = shuffle([...q.options]);
        return {
          category: q.category,
          question: q.question,
          options: options,
          correctLetter: letters[options.indexOf(q.correctText)],
          correctText: q.correctText,
          explanation: q.explanation
        };
      });
      startQuiz(retryList);
    }

    function restartRound() {
      startQuiz();
    }

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      const activeQuiz = !document.getElementById('view-quiz').classList.contains('hidden');
      if (!activeQuiz) return;

      const key = e.key.toUpperCase();
      if (['A', 'B', 'C', 'D'].includes(key) && !answeredCurrent) {
        selectAnswer(key);
      } else if ((e.key === 'Enter' || e.key === ' ') && answeredCurrent) {
        e.preventDefault();
        nextQuestion();
      }
    });

    // Browse Question Bank
    let currentBrowseCategory = 'All';

    function setBrowseCategory(cat) {
      currentBrowseCategory = cat;
      document.querySelectorAll('.bcat-btn').forEach(btn => {
        if (btn.getAttribute('data-bcat') === cat) {
          btn.classList.add('bg-emerald-500/15', 'border-emerald-500/50', 'text-emerald-300', 'font-semibold');
          btn.classList.remove('bg-slate-900', 'border-slate-800', 'text-slate-300');
        } else {
          btn.classList.remove('bg-emerald-500/15', 'border-emerald-500/50', 'text-emerald-300', 'font-semibold');
          btn.classList.add('bg-slate-900', 'border-slate-800', 'text-slate-300');
        }
      });
      renderBrowseList();
    }

    function filterBrowseQuestions() {
      renderBrowseList();
    }

    function renderBrowseList() {
      const query = (document.getElementById('browse-search').value || '').toLowerCase();
      const container = document.getElementById('browse-list');
      container.innerHTML = '';

      let filtered = RAW_QUESTION_BANK;
      if (currentBrowseCategory !== 'All') {
        filtered = filtered.filter(q => q[0] === currentBrowseCategory);
      }
      if (query) {
        filtered = filtered.filter(q => 
          q[1].toLowerCase().includes(query) || 
          q[2].toLowerCase().includes(query) || 
          q[4].toLowerCase().includes(query)
        );
      }

      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-slate-400 text-sm">No questions matched your query.</div>`;
        return;
      }

      filtered.forEach((q, idx) => {
        const [cat, text, correct, wrong, exp] = q;
        const card = document.createElement('div');
        card.className = 'bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3';
        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-400">
            <span class="font-semibold text-slate-200">${cat}</span>
            <span class="font-mono text-slate-400">#${idx + 1}</span>
          </div>
          <h4 class="text-base font-semibold text-white">${text}</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <div class="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-500/40 text-emerald-300">
              <span class="font-bold text-emerald-400">&#10003; Answer:</span> ${correct}
            </div>
            ${wrong.map(w => `
              <div class="p-2.5 rounded-lg bg-slate-850 border border-slate-800 text-slate-400">
                <span class="text-slate-400">&bull;</span> ${w}
              </div>
            `).join('')}
          </div>
          <div class="text-xs text-slate-300 bg-slate-950 p-3 rounded-lg border border-slate-800/80">
            <span class="font-semibold text-slate-400">Explanation:</span> ${exp}
          </div>
        `;
        container.appendChild(card);
      });
    }

    // LocalStorage Statistics Tracking
    function getStoredStats() {
      try {
        const data = localStorage.getItem('tech_quiz_stats');
        return data ? JSON.parse(data) : { rounds: 0, answered: 0, correct: 0 };
      } catch (e) {
        return { rounds: 0, answered: 0, correct: 0 };
      }
    }

    function recordAnswer(isCorrect) {
      const stats = getStoredStats();
      stats.answered++;
      if (isCorrect) stats.correct++;
      try {
        localStorage.setItem('tech_quiz_stats', JSON.stringify(stats));
      } catch (e) {}
    }

    function recordRoundComplete() {
      const stats = getStoredStats();
      stats.rounds++;
      try {
        localStorage.setItem('tech_quiz_stats', JSON.stringify(stats));
      } catch (e) {}
    }

    function renderStats() {
      const stats = getStoredStats();
      document.getElementById('stat-rounds').textContent = stats.rounds;
      document.getElementById('stat-answered').textContent = stats.answered;
      document.getElementById('stat-correct').textContent = stats.correct;
      const acc = stats.answered > 0 ? Math.round((stats.correct / stats.answered) * 100) : 0;
      document.getElementById('stat-accuracy').textContent = `${acc}%`;
    }

    function clearStats() {
      if (confirm('Reset your quiz statistics?')) {
        localStorage.removeItem('tech_quiz_stats');
        renderStats();
      }
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    # Category counts
    cat_counts = {}
    for entry in QUESTION_BANK:
        cat = entry[0]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    import json
    return render_template_string(
        HTML_TEMPLATE,
        total_questions=len(QUESTION_BANK),
        categories=CATEGORIES,
        category_counts=cat_counts,
        question_bank_json=json.dumps(QUESTION_BANK),
        categories_json=json.dumps(CATEGORIES)
    )

@app.route("/api/categories")
def api_categories():
    counts = {}
    for entry in QUESTION_BANK:
        cat = entry[0]
        counts[cat] = counts.get(cat, 0) + 1
    return jsonify({
        "categories": CATEGORIES,
        "counts": counts,
        "total": len(QUESTION_BANK)
    })

@app.route("/api/quiz")
def api_quiz():
    category = request.args.get("category", "All")
    count_param = request.args.get("count", "10")

    pool = QUESTION_BANK
    if category != "All" and category in CATEGORIES:
        pool = [q for q in pool if q[0] == category]

    try:
        count = min(int(count_param), len(pool))
    except ValueError:
        count = min(10, len(pool))

    selected = random.sample(pool, count)
    questions = [build_question(entry) for entry in selected]
    return jsonify({
        "category": category,
        "count": len(questions),
        "questions": questions
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    # Werkzeug development server bound to 0.0.0.0
    app.run(host="0.0.0.0", port=port, debug=False)
