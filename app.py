import os
import random
import json
from flask import Flask, jsonify, request, render_template_string

from quiz_game import QUESTION_BANK, build_question, LETTERS

app = Flask(__name__)

# Real categories from the verified question bank
CATEGORIES = sorted(list({entry[0] for entry in QUESTION_BANK}))

# Category metadata mapping for enhanced developer UI
CATEGORY_DETAILS = {
    "Python": {
        "title": "Python Programming",
        "description": "Language syntax, data types, generators, decorators & OOP",
        "icon": "python",
        "color": "cyan",
    },
    "DSA": {
        "title": "Data Structures & Algorithms",
        "description": "Big-O complexity, stacks, queues, trees, graphs & sorting",
        "icon": "tree",
        "color": "violet",
    },
    "Web": {
        "title": "Web & Networking",
        "description": "HTTP status codes, DNS, REST APIs, JSON & security protocols",
        "icon": "globe",
        "color": "blue",
    },
    "Databases": {
        "title": "Databases & SQL",
        "description": "Relational schemas, SQL queries, ACID transactions & NoSQL",
        "icon": "database",
        "color": "amber",
    },
    "Git & DevOps": {
        "title": "Git & DevOps",
        "description": "Version control, branching, CI/CD pipelines & deployment",
        "icon": "git",
        "color": "emerald",
    },
    "CS Basics": {
        "title": "CS Fundamentals",
        "description": "Binary logic, compiler mechanics, RAM & architecture",
        "icon": "cpu",
        "color": "rose",
    },
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="h-full scroll-smooth">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TechNova — The Technical Challenge Arena</title>
  <meta name="description" content="Ignite your logic. Explore technology. Test your skills across Python, DSA, Web Architecture, Databases, Git, and Computer Science fundamentals in an interactive developer arena.">
  <meta property="og:title" content="TechNova — The Technical Challenge Arena">
  <meta property="og:description" content="Ignite your logic. Explore technology in a futuristic technical quiz platform.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
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
            arena: {
              bg: '#070a13',
              card: '#0c1322',
              hover: '#111a30',
              border: '#18243c',
              borderGlow: '#0ea5e9',
              cyan: '#06b6d4',
              cyanGlow: 'rgba(6, 182, 212, 0.25)',
              violet: '#8b5cf6',
              violetGlow: 'rgba(139, 92, 246, 0.25)',
            }
          },
          backgroundImage: {
            'grid-pattern': "radial-gradient(circle at 1px 1px, rgba(14, 165, 233, 0.08) 1px, transparent 0)",
            'cyber-gradient': 'linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)',
          }
        }
      }
    }
  </script>
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #070a13;
      background-size: 24px 24px;
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

    /* Subtle glow utilities */
    .glow-cyan {
      box-shadow: 0 0 25px -5px rgba(6, 182, 212, 0.25);
    }
    .glow-violet {
      box-shadow: 0 0 25px -5px rgba(139, 92, 246, 0.25);
    }
    .glow-border {
      border-color: rgba(6, 182, 212, 0.5);
      box-shadow: 0 0 15px -3px rgba(6, 182, 212, 0.2);
    }

    /* Accessibility: Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }

    /* Option card transitions */
    .option-card {
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #070a13;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #0ea5e9;
    }

    /* Pulse circuit animation */
    @keyframes pulseCircuit {
      0%, 100% { opacity: 0.35; transform: scale(1); }
      50% { opacity: 0.75; transform: scale(1.02); }
    }
    .circuit-pulse {
      animation: pulseCircuit 4s ease-in-out infinite;
    }

    /* Technical Scanline Animation */
    @keyframes techScanline {
      0% { top: -10%; opacity: 0; }
      15% { opacity: 0.85; }
      85% { opacity: 0.85; }
      100% { top: 110%; opacity: 0; }
    }
    .tech-scanline {
      position: absolute;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent 0%, rgba(6, 182, 212, 0.95) 50%, transparent 100%);
      box-shadow: 0 0 12px 1px rgba(6, 182, 212, 0.8);
      animation: techScanline 3.2s ease-in-out infinite;
      pointer-events: none;
      z-index: 20;
    }

    /* Technical Data Stream Flow on SVG circuit traces */
    @keyframes dataStreamFlow {
      0% { stroke-dashoffset: 40; }
      100% { stroke-dashoffset: 0; }
    }
    .circuit-stream {
      stroke-dasharray: 6 4;
      animation: dataStreamFlow 1.6s linear infinite;
    }

    /* Glowing Node Pulse */
    @keyframes nodePulseGlow {
      0%, 100% { opacity: 0.75; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.35); filter: drop-shadow(0 0 6px rgba(6, 182, 212, 0.9)); }
    }
    .node-pulse {
      transform-box: fill-box;
      transform-origin: center;
      animation: nodePulseGlow 2s ease-in-out infinite;
    }

    /* Blinking Terminal Cursor */
    @keyframes cursorBlink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    .terminal-cursor {
      display: inline-block;
      width: 7px;
      height: 13px;
      background-color: #06b6d4;
      vertical-align: middle;
      margin-left: 4px;
      box-shadow: 0 0 6px #06b6d4;
      animation: cursorBlink 0.9s infinite;
    }

    /* Radar Ping Indicator on HUD */
    @keyframes radarPing {
      0% { transform: scale(0.9); opacity: 0.85; }
      70% { transform: scale(2.3); opacity: 0; }
      100% { transform: scale(2.5); opacity: 0; }
    }
    .radar-beacon {
      position: relative;
    }
    .radar-beacon::after {
      content: '';
      position: absolute;
      inset: -2px;
      border-radius: 9999px;
      border: 1.5px solid #06b6d4;
      animation: radarPing 2s cubic-bezier(0, 0, 0.2, 1) infinite;
    }
  </style>
</head>
<body class="bg-arena-bg bg-grid-pattern text-slate-100 min-h-full flex flex-col antialiased selection:bg-cyan-500/30 selection:text-cyan-200">

  <!-- ================= TOP NAVIGATION BAR ================= -->
  <!-- Strict Top Bar Contract: 3 zones, gap-8, single line -->
  <header class="border-b border-slate-800/80 bg-arena-bg/85 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-8">
      
      <!-- Zone 1: Brand Wordmark -->
      <a href="/" onclick="handleBrandClick(event)" class="flex items-center gap-2.5 text-lg font-bold tracking-tight text-white font-display whitespace-nowrap shrink-0 group">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500/20 to-violet-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 group-hover:border-cyan-400 group-hover:shadow-[0_0_12px_rgba(6,182,212,0.4)] transition-all">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
          </svg>
        </div>
        <div class="flex items-baseline gap-1.5">
          <span class="bg-gradient-to-r from-white via-cyan-100 to-cyan-400 bg-clip-text text-transparent font-extrabold text-xl">TechNova</span>
          <span class="text-[11px] font-mono text-cyan-400/80 tracking-wider hidden sm:inline">ARENA</span>
        </div>
      </a>

      <!-- Zone 2: Navigation Links -->
      <nav class="hidden md:flex items-center gap-6 text-xs font-semibold uppercase tracking-wider text-slate-400">
        <button onclick="requestView('landing')" id="nav-landing" class="nav-item hover:text-cyan-300 transition-colors whitespace-nowrap shrink-0 text-cyan-400 font-bold">Arena Home</button>
        <button onclick="requestView('stats')" id="nav-stats" class="nav-item hover:text-cyan-300 transition-colors whitespace-nowrap shrink-0">Telemetry Stats</button>
      </nav>

      <!-- Zone 3: Primary Action -->
      <div class="flex items-center gap-3 shrink-0">
        <button onclick="scrollToSetup()" class="px-4 py-2 text-xs font-bold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 rounded-lg transition-all whitespace-nowrap shrink-0 shadow-md shadow-cyan-500/20 active:scale-95 flex items-center gap-1.5">
          <span>Start Challenge</span>
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    </div>
  </header>

  <!-- ================= MAIN CONTENT ================= -->
  <main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-8 flex flex-col">

    <!-- ================= VIEW 1: LANDING & SETUP ================= -->
    <div id="view-landing" class="space-y-12">
      
      <!-- HERO SECTION -->
      <section class="relative rounded-3xl border border-slate-800/80 bg-gradient-to-b from-slate-900/70 via-arena-card/60 to-arena-bg/90 p-8 sm:p-12 overflow-hidden shadow-2xl">
        <!-- Background Circuit Decor -->
        <div class="absolute -right-16 -top-16 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none circuit-pulse"></div>
        <div class="absolute -left-16 -bottom-16 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl pointer-events-none circuit-pulse" style="animation-delay: -2s;"></div>
        
        <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <!-- Left Column: Copy & Value Proposition -->
          <div class="lg:col-span-7 space-y-6">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-xs font-mono text-cyan-300">
              <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
              <span>DEV CHALLENGE SYSTEM &middot; v2.4</span>
            </div>

            <div class="space-y-2">
              <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold font-display tracking-tight text-white leading-[1.1]">
                TechNova
              </h1>
              <p class="text-lg sm:text-xl font-semibold bg-gradient-to-r from-cyan-300 via-sky-200 to-violet-300 bg-clip-text text-transparent">
                Ignite your logic. Explore technology.
              </p>
            </div>

            <p class="text-sm sm:text-base text-slate-300 leading-relaxed max-w-xl">
              Enter the competitive developer proving ground. Test your technical knowledge across core computer science paradigms, data structure performance, system protocols, and modern development stacks with instant architectural feedback.
            </p>

            <div class="flex flex-wrap items-center gap-4 pt-2">
              <button onclick="scrollToSetup()" class="px-6 py-3.5 text-sm font-bold text-slate-950 bg-gradient-to-r from-cyan-400 via-cyan-300 to-emerald-300 hover:from-cyan-300 hover:to-emerald-200 rounded-xl transition-all shadow-lg shadow-cyan-500/25 active:scale-95 flex items-center gap-2">
                <span>Start Challenge</span>
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </button>

              <button onclick="scrollToSetup()" class="px-5 py-3.5 text-sm font-semibold text-slate-300 bg-slate-800/80 hover:bg-slate-700/80 hover:text-white rounded-xl transition-all border border-slate-700/80 flex items-center gap-2">
                <svg class="w-4 h-4 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="7" height="7"></rect>
                  <rect x="14" y="3" width="7" height="7"></rect>
                  <rect x="14" y="14" width="7" height="7"></rect>
                  <rect x="3" y="14" width="7" height="7"></rect>
                </svg>
                <span>Choose Discipline</span>
              </button>
            </div>
          </div>

          <!-- Right Column: Animated Technical Illustration / Circuit HUD -->
          <div class="lg:col-span-5 flex justify-center">
            <div class="w-full max-w-sm rounded-2xl border border-slate-800 bg-slate-950/80 p-5 shadow-2xl relative backdrop-blur overflow-hidden">
              <div class="tech-scanline"></div>
              <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4 text-xs font-mono text-slate-400">
                <div class="flex items-center gap-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 radar-beacon"></span>
                  <span class="text-cyan-300 font-semibold tracking-wide">ARENA_KERNEL<span class="terminal-cursor"></span></span>
                </div>
                <span class="text-slate-400 font-mono text-[11px]">ACTIVE &middot; READY</span>
              </div>

              <!-- Circuit SVG Matrix with animated data stream and node pulses -->
              <div class="space-y-3">
                <div class="h-28 rounded-xl bg-gradient-to-br from-slate-900 to-arena-card border border-slate-800 flex items-center justify-center relative overflow-hidden">
                  <svg class="w-full h-full text-cyan-500/30" viewBox="0 0 300 120" fill="none">
                    <line x1="20" y1="60" x2="80" y2="60" stroke="#0ea5e9" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <circle cx="80" cy="60" r="5" fill="#06b6d4" class="node-pulse" />
                    <line x1="80" y1="60" x2="140" y2="25" stroke="#8b5cf6" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <circle cx="140" cy="25" r="5" fill="#8b5cf6" class="node-pulse" />
                    <line x1="80" y1="60" x2="140" y2="95" stroke="#3b82f6" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <circle cx="140" cy="95" r="5" fill="#3b82f6" class="node-pulse" />
                    <line x1="140" y1="25" x2="220" y2="25" stroke="#10b981" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <circle cx="220" cy="25" r="5" fill="#10b981" class="node-pulse" />
                    <line x1="140" y1="95" x2="220" y2="95" stroke="#f59e0b" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <circle cx="220" cy="95" r="5" fill="#f59e0b" class="node-pulse" />
                    <line x1="220" y1="25" x2="270" y2="60" stroke="#0ea5e9" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <line x1="220" y1="95" x2="270" y2="60" stroke="#0ea5e9" stroke-width="2" stroke-opacity="0.8" class="circuit-stream"/>
                    <circle cx="270" cy="60" r="6" fill="#06b6d4" class="node-pulse" />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <span class="font-mono text-xs font-bold text-cyan-300 bg-slate-950/85 px-2.5 py-1 rounded border border-cyan-500/40 shadow-lg shadow-cyan-950/50">
                      7 ARENA DOMAINS
                    </span>
                  </div>
                </div>

                <!-- HUD Quick Stats -->
                <div class="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div class="bg-slate-900/90 border border-slate-800 rounded-lg p-2.5">
                    <span class="text-slate-400 block text-[10px] uppercase">Bank Capacity</span>
                    <span class="text-base font-bold text-cyan-400 tabular-nums">{{ total_questions }} Challenges</span>
                  </div>
                  <div class="bg-slate-900/90 border border-slate-800 rounded-lg p-2.5">
                    <span class="text-slate-400 block text-[10px] uppercase">Disciplines</span>
                    <span class="text-base font-bold text-violet-400 tabular-nums">7 Selectable</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COMPACT STATISTICS SECTION -->
        <!-- Requirement: Displaying 42 questions and 7 technical categories matching existing application data -->
        <div class="mt-8 pt-6 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div class="space-y-1">
            <span class="text-xs text-slate-400">Total Questions</span>
            <div class="text-2xl font-bold font-mono text-white tabular-nums flex items-baseline gap-1">
              <span>{{ total_questions }}</span>
              <span class="text-xs text-cyan-400 font-sans font-normal">curated</span>
            </div>
          </div>
          <div class="space-y-1">
            <span class="text-xs text-slate-400">Technical Categories</span>
            <div class="text-2xl font-bold font-mono text-cyan-400 tabular-nums flex items-baseline gap-1">
              <span>7</span>
              <span class="text-xs text-slate-400 font-sans font-normal">(6 + All)</span>
            </div>
          </div>
          <div class="space-y-1">
            <span class="text-xs text-slate-400">Verification</span>
            <div class="text-2xl font-bold font-mono text-emerald-400 tabular-nums flex items-baseline gap-1">
              <span>100%</span>
              <span class="text-xs text-slate-400 font-sans font-normal">explained</span>
            </div>
          </div>
          <div class="space-y-1">
            <span class="text-xs text-slate-400">Audio Feedback</span>
            <div class="text-2xl font-bold font-mono text-violet-400 tabular-nums flex items-baseline gap-1">
              <span>WebAudio</span>
              <span class="text-xs text-slate-400 font-sans font-normal">synthesized</span>
            </div>
          </div>
        </div>
      </section>

      <!-- SETUP CONTAINER ANCHOR -->
      <div id="setup-anchor" class="pt-2"></div>

      <!-- INTERACTIVE CATEGORY SELECTION -->
      <section class="space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
          <div>
            <h2 class="text-2xl font-bold font-display text-white">Select Your Challenge Discipline</h2>
            <p class="text-xs sm:text-sm text-slate-400">Choose a focused domain or test across all engineering fundamentals.</p>
          </div>
          <span id="selected-category-summary" class="text-xs font-mono text-cyan-400">All Topics &middot; {{ total_questions }} questions available</span>
        </div>

        <!-- Category Cards Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3.5" id="category-cards-grid">
          
          <!-- Card: All Topics -->
          <div onclick="selectCategory('All')" 
               onkeydown="handleCardKeydown(event, 'All')"
               tabindex="0"
               data-cat="All" 
               class="category-card active group relative rounded-2xl border p-4 cursor-pointer transition-all bg-gradient-to-br from-cyan-950/40 to-slate-900 border-cyan-500/70 shadow-[0_0_20px_rgba(6,182,212,0.18)] focus:outline-none focus:ring-2 focus:ring-cyan-400">
            <div class="flex items-start justify-between">
              <div class="w-10 h-10 rounded-xl bg-cyan-500/20 border border-cyan-500/40 text-cyan-300 flex items-center justify-center shrink-0">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                  <polyline points="2 17 12 22 22 17"></polyline>
                  <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
              </div>
              <span class="text-xs font-mono font-bold text-cyan-300 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-500/30">
                {{ total_questions }} Qs
              </span>
            </div>
            <div class="mt-3 space-y-1">
              <h3 class="text-base font-bold text-white group-hover:text-cyan-200 transition-colors">All Topics</h3>
              <p class="text-xs text-slate-400 leading-snug">Full-spectrum arena across all 6 core technical domains.</p>
            </div>
            <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-cyan-400">
              <span class="card-indicator font-semibold">&#10003; SELECTED</span>
              <span class="text-slate-400">Multi-Domain</span>
            </div>
          </div>

          <!-- Dynamic Category Cards from existing data -->
          {% for cat in categories %}
          {% set info = category_details.get(cat, {}) %}
          {% set count = category_counts.get(cat, 0) %}
          <div onclick="selectCategory('{{ cat }}')" 
               onkeydown="handleCardKeydown(event, '{{ cat }}')"
               tabindex="0"
               data-cat="{{ cat }}" 
               class="category-card group relative rounded-2xl border p-4 cursor-pointer transition-all bg-slate-900/80 border-slate-800 hover:border-slate-700 hover:bg-slate-850/80 focus:outline-none focus:ring-2 focus:ring-cyan-400">
            <div class="flex items-start justify-between">
              <div class="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 flex items-center justify-center shrink-0 group-hover:border-slate-600 transition-colors">
                {% if info.icon == 'python' %}
                <svg class="w-5 h-5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
                {% elif info.icon == 'tree' %}
                <svg class="w-5 h-5 text-violet-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="5" r="3"></circle>
                  <circle cx="6" cy="19" r="3"></circle>
                  <circle cx="18" cy="19" r="3"></circle>
                  <path d="M12 8v4M6 16l4.5-4M18 16l-4.5-4"></path>
                </svg>
                {% elif info.icon == 'globe' %}
                <svg class="w-5 h-5 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="2" y1="12" x2="22" y2="12"></line>
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
                {% elif info.icon == 'database' %}
                <svg class="w-5 h-5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                  <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
                  <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                </svg>
                {% elif info.icon == 'git' %}
                <svg class="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="18" cy="18" r="3"></circle>
                  <circle cx="6" cy="6" r="3"></circle>
                  <path d="M6 9v12"></path>
                  <path d="M18 9a9 9 0 0 1-9 9"></path>
                </svg>
                {% elif info.icon == 'cpu' %}
                <svg class="w-5 h-5 text-rose-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="4" y="4" width="16" height="16" rx="2"></rect>
                  <rect x="9" y="9" width="6" height="6"></rect>
                  <path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"></path>
                </svg>
                {% else %}
                <svg class="w-5 h-5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="9"></circle>
                  <polyline points="12 6 12 12 14 14"></polyline>
                </svg>
                {% endif %}
              </div>
              <span class="text-xs font-mono font-semibold text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                {{ count }} Qs
              </span>
            </div>
            <div class="mt-3 space-y-1">
              <h3 class="text-base font-bold text-white group-hover:text-cyan-200 transition-colors">{{ info.get('title', cat) }}</h3>
              <p class="text-xs text-slate-400 leading-snug line-clamp-2">{{ info.get('description', 'Verified technical challenge set.') }}</p>
            </div>
            <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span class="card-indicator">Select</span>
              <span>Domain Focus</span>
            </div>
          </div>
          {% endfor %}

        </div>
      </section>

      <!-- QUIZ CONFIGURATION PANEL -->
      <section class="rounded-2xl border border-slate-800 bg-slate-900/90 p-6 sm:p-8 space-y-6 shadow-xl relative backdrop-blur">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h3 class="text-lg font-bold font-display text-white">Challenge Parameters</h3>
            <p class="text-xs text-slate-400">Configure round size, timing, and sensory feedback.</p>
          </div>
          <span class="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2.5 py-1 rounded border border-cyan-500/30">
            CONFIG PROTOCOL
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Question Count Selector -->
          <!-- Requirement: Interactive question-count selectors for 5, 10, 20, and All. Do not allow selected count to exceed available questions. -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-xs font-bold uppercase tracking-wider text-slate-300">Question Capacity</label>
              <span id="count-feedback-hint" class="text-xs font-mono text-cyan-300 font-semibold">10 Questions Selected</span>
            </div>
            <div class="grid grid-cols-4 gap-2" id="count-selector-group">
              <button onclick="selectCount(5)" data-count="5" id="btn-count-5" class="count-btn py-2.5 text-xs font-bold font-mono rounded-xl border border-slate-800 bg-slate-950 text-slate-300 hover:border-slate-700 transition-all">5</button>
              <button onclick="selectCount(10)" data-count="10" id="btn-count-10" class="count-btn active py-2.5 text-xs font-bold font-mono rounded-xl border border-cyan-500/80 bg-cyan-950/40 text-cyan-300 shadow-[0_0_12px_rgba(6,182,212,0.2)] transition-all">10</button>
              <button onclick="selectCount(20)" data-count="20" id="btn-count-20" class="count-btn py-2.5 text-xs font-bold font-mono rounded-xl border border-slate-800 bg-slate-950 text-slate-300 hover:border-slate-700 transition-all">20</button>
              <button onclick="selectCount('max')" data-count="max" id="btn-count-max" class="count-btn py-2.5 text-xs font-bold font-mono rounded-xl border border-slate-800 bg-slate-950 text-slate-300 hover:border-slate-700 transition-all">All</button>
            </div>
            <p id="count-clamping-msg" class="text-[11px] text-slate-400">Pick how many questions you want to tackle this round.</p>
          </div>

          <!-- Modifiers: Timer & Audio -->
          <div class="space-y-3">
            <label class="text-xs font-bold uppercase tracking-wider text-slate-300">Arena Modifiers</label>
            <div class="space-y-2.5">
              
              <!-- Timer Mode Toggle -->
              <label class="flex items-center justify-between p-3 rounded-xl border border-slate-800 bg-slate-950 hover:border-slate-700 cursor-pointer transition-colors">
                <div class="flex items-center gap-2.5">
                  <div class="w-7 h-7 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xs">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                  </div>
                  <div>
                    <span class="text-xs font-bold text-white block">Speed Timer (30s per question)</span>
                    <span class="text-[11px] text-slate-400">Adds countdown pressure for bonus focus</span>
                  </div>
                </div>
                <input type="checkbox" id="timer-toggle" class="w-4 h-4 rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-500">
              </label>

              <!-- Sound Effects Toggle -->
              <label class="flex items-center justify-between p-3 rounded-xl border border-slate-800 bg-slate-950 hover:border-slate-700 cursor-pointer transition-colors">
                <div class="flex items-center gap-2.5">
                  <div class="w-7 h-7 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-xs">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                      <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                    </svg>
                  </div>
                  <div>
                    <span class="text-xs font-bold text-white block">WebAudio Sound Chimes</span>
                    <span class="text-[11px] text-slate-400">Audio feedback for answers & streaks</span>
                  </div>
                </div>
                <input type="checkbox" id="sound-toggle" checked onchange="handleAudioToggleChange()" class="w-4 h-4 rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-500">
              </label>

            </div>
          </div>
        </div>

        <!-- Configuration Summary Strip -->
        <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div class="flex items-center gap-2 text-slate-300">
            <span class="text-slate-400">Summary:</span>
            <span id="summary-category-pill" class="font-bold text-white font-mono">All Topics</span>
            <span aria-hidden="true">&middot;</span>
            <span id="summary-count-pill" class="font-bold text-cyan-300 font-mono">10 Questions</span>
            <span aria-hidden="true">&middot;</span>
            <span id="summary-timer-pill" class="text-slate-400 font-mono">Untimed</span>
          </div>

          <div class="text-[11px] text-slate-400 font-mono">
            SHORTCUTS: <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">A</kbd> <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">B</kbd> <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">C</kbd> <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">D</kbd>
          </div>
        </div>

        <!-- Prominent Launch Button -->
        <button onclick="startQuiz()" class="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-cyan-400 via-cyan-300 to-violet-400 hover:from-cyan-300 hover:to-violet-300 text-slate-950 font-extrabold text-sm tracking-wider uppercase transition-all shadow-xl shadow-cyan-500/20 active:scale-[0.99] flex items-center justify-center gap-2 group">
          <span>Initialize Challenge</span>
          <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </section>

    </div>

    <!-- ================= VIEW 2: ACTIVE QUIZ SCREEN ================= -->
    <section id="view-quiz" class="hidden max-w-3xl w-full mx-auto space-y-5 my-auto">
      
      <!-- Top HUD Header -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/90 p-4 sm:p-5 space-y-3 shadow-xl backdrop-blur">
        <div class="flex items-center justify-between text-xs text-slate-400">
          <!-- Category & Question Counter -->
          <div class="flex items-center gap-2">
            <span id="quiz-cat-badge" class="font-bold text-cyan-300 font-mono uppercase tracking-wider">Python</span>
            <span aria-hidden="true">&middot;</span>
            <span class="text-slate-300 font-medium">Question <span id="quiz-current-num" class="font-mono text-white font-bold">1</span> of <span id="quiz-total-num" class="font-mono">10</span></span>
          </div>

          <!-- Score, Streak, Timer & Quit Button -->
          <div class="flex items-center gap-3 sm:gap-4">
            <!-- Timer Display (if enabled) -->
            <div id="quiz-timer-container" class="hidden flex items-center gap-1 font-mono text-xs font-bold text-amber-400 bg-amber-950/40 border border-amber-500/30 px-2 py-0.5 rounded">
              <svg class="w-3 h-3 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor"></path>
              </svg>
              <span id="quiz-timer-seconds">30</span>s
            </div>

            <!-- Score -->
            <div class="flex items-center gap-1 text-xs">
              <span class="text-slate-400">Score:</span>
              <span id="quiz-live-score" class="font-mono font-bold text-cyan-400 tabular-nums">0</span>
            </div>

            <!-- Streak -->
            <div class="flex items-center gap-1 text-xs">
              <span class="text-slate-400">Streak:</span>
              <span id="quiz-live-streak" class="font-mono font-bold text-amber-400 tabular-nums">0</span>
            </div>

            <!-- Quit Button with Confirmation -->
            <button onclick="promptQuitQuiz()" title="Quit current round" class="text-xs text-slate-400 hover:text-rose-400 p-1 rounded hover:bg-slate-800 transition-colors">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800/80 p-0.5">
          <div id="quiz-progress-bar" class="bg-gradient-to-r from-cyan-500 via-sky-400 to-violet-500 h-full rounded-full transition-all duration-300 shadow-[0_0_10px_rgba(6,182,212,0.5)]" style="width: 10%;"></div>
        </div>
      </div>

      <!-- Question Card -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/90 p-6 sm:p-8 space-y-6 shadow-2xl backdrop-blur relative">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-mono uppercase tracking-widest text-cyan-400 font-bold bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30">
              MULTIPLE CHOICE QUERY
            </span>
            <span class="text-xs font-mono text-slate-400">Press A, B, C, or D</span>
          </div>

          <!-- Question Text with high contrast -->
          <h2 id="quiz-question-text" class="text-xl sm:text-2xl font-bold font-display text-white leading-snug">
            Question loading...
          </h2>
        </div>

        <!-- Four Well-Spaced Answer Option Cards -->
        <div id="quiz-options-container" class="space-y-3">
          <!-- Populated by JS -->
        </div>

        <!-- Detailed Feedback & Explanation Card (Smoothly revealed upon answering) -->
        <div id="quiz-feedback-panel" class="hidden rounded-xl p-4 sm:p-5 border transition-all space-y-3 shadow-lg">
          <div class="flex items-start gap-3">
            <div id="quiz-feedback-icon" class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-bold text-xs"></div>
            <div class="space-y-1 flex-1">
              <div id="quiz-feedback-title" class="text-sm font-bold font-display"></div>
              <div id="quiz-feedback-explanation" class="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans"></div>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-800/60 flex items-center justify-between">
            <span class="text-[11px] text-slate-400 font-mono">Press <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">ENTER</kbd> or <kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300">SPACE</kbd></span>
            <button id="quiz-next-btn" onclick="nextQuestion()" class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 text-slate-950 font-bold text-xs uppercase tracking-wider transition-all shadow-md shadow-cyan-500/20 active:scale-95 flex items-center gap-1.5">
              <span id="quiz-next-label">Next Challenge</span>
              <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= VIEW 3: RESULTS SCREEN ================= -->
    <section id="view-results" class="hidden max-w-3xl w-full mx-auto space-y-6 my-auto">
      <div class="rounded-3xl border border-slate-800 bg-slate-900/90 p-6 sm:p-10 space-y-8 shadow-2xl backdrop-blur relative overflow-hidden text-center">
        <!-- Glow accents -->
        <div class="absolute -top-24 left-1/2 -translate-x-1/2 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="relative z-10 space-y-2">
          <span class="text-xs font-mono uppercase tracking-widest text-cyan-400 font-bold bg-cyan-950/80 px-3 py-1 rounded-full border border-cyan-500/30">
            CHALLENGE EVALUATION COMPLETE
          </span>
          <h2 id="results-headline" class="text-3xl sm:text-4xl font-extrabold font-display text-white">
            Architecture Mastery
          </h2>
          <p id="results-subtext" class="text-xs sm:text-sm text-slate-300 max-w-lg mx-auto leading-relaxed"></p>
        </div>

        <!-- Circular Score Progress Visualization -->
        <div class="relative z-10 flex flex-col items-center justify-center">
          <div class="relative w-40 h-40 flex items-center justify-center">
            <!-- SVG Progress Ring -->
            <svg class="w-full h-full -rotate-90" viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="50" fill="none" stroke="#1e293b" stroke-width="8"></circle>
              <circle id="results-ring-progress" cx="60" cy="60" r="50" fill="none" stroke="url(#ring-gradient)" stroke-width="8" stroke-dasharray="314.16" stroke-dashoffset="314.16" stroke-linecap="round" class="transition-all duration-1000 ease-out"></circle>
              <defs>
                <linearGradient id="ring-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#06b6d4" />
                  <stop offset="100%" stop-color="#8b5cf6" />
                </linearGradient>
              </defs>
            </svg>
            <!-- Center percentage & fraction -->
            <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
              <span id="results-percentage" class="text-3xl font-extrabold font-mono text-white tabular-nums">0%</span>
              <span id="results-score-fraction" class="text-xs font-mono text-cyan-300 tabular-nums">0/0</span>
            </div>
          </div>
        </div>

        <!-- Quantitative Metric Grid (Real Verified Data Only) -->
        <div class="relative z-10 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-xl mx-auto">
          <div class="rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-center">
            <span class="text-[11px] text-slate-400 block">Correct</span>
            <span id="results-stat-correct" class="text-xl font-bold font-mono text-emerald-400 tabular-nums">0</span>
          </div>
          <div class="rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-center">
            <span class="text-[11px] text-slate-400 block">Incorrect</span>
            <span id="results-stat-incorrect" class="text-xl font-bold font-mono text-rose-400 tabular-nums">0</span>
          </div>
          <div class="rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-center">
            <span class="text-[11px] text-slate-400 block">Max Streak</span>
            <span id="results-stat-streak" class="text-xl font-bold font-mono text-amber-400 tabular-nums">0</span>
          </div>
          <div class="rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-center">
            <span class="text-[11px] text-slate-400 block">Discipline</span>
            <span id="results-stat-cat" class="text-sm font-bold font-mono text-cyan-300 truncate block mt-0.5">All</span>
          </div>
        </div>

        <!-- Primary Action CTAs -->
        <div class="relative z-10 flex flex-wrap items-center justify-center gap-3 pt-2">
          <button onclick="restartRound()" class="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 text-slate-950 font-bold text-xs uppercase tracking-wider transition-all shadow-lg shadow-cyan-500/20 active:scale-95 flex items-center gap-2">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 4 23 10 17 10"></polyline>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
            <span>Play Another Round</span>
          </button>

          <button id="results-retry-missed-btn" onclick="retryMissedQuestions()" class="hidden px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs uppercase tracking-wider transition-all border border-slate-700 flex items-center gap-2">
            <svg class="w-4 h-4 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>Practice Missed (<span id="results-missed-count">0</span>)</span>
          </button>

          <button onclick="requestView('landing')" class="px-5 py-3 rounded-xl bg-slate-950 hover:bg-slate-850 text-slate-300 font-semibold text-xs tracking-wider transition-all border border-slate-800">
            Choose Another Category
          </button>
        </div>
      </div>

      <!-- Question Review Panel -->
      <div id="results-review-section" class="rounded-2xl border border-slate-800 bg-slate-900/90 p-6 sm:p-8 space-y-4 shadow-xl backdrop-blur">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <svg class="w-4 h-4 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
            </svg>
            <h3 class="text-base font-bold font-display text-white">Review Round Challenges</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">Targeted Feedback & Tips</span>
        </div>

        <div id="results-review-list" class="space-y-3">
          <!-- Populated by JS -->
        </div>
      </div>
    </section>

    <!-- ================= VIEW 4: TELEMETRY STATS ================= -->
    <section id="view-stats" class="hidden space-y-6 max-w-4xl w-full mx-auto">
      <div class="rounded-2xl border border-slate-800 bg-slate-900/90 p-6 sm:p-8 space-y-6 shadow-xl backdrop-blur">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h2 class="text-2xl font-bold font-display text-white">Lifetime Arena Telemetry</h2>
            <p class="text-xs sm:text-sm text-slate-400">Real-time statistics recorded on your browser storage.</p>
          </div>
          <span class="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2.5 py-1 rounded border border-cyan-500/30">
            SYSTEM PERFORMANCE
          </span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <span class="text-xs text-slate-400">Total Rounds</span>
            <div id="stat-rounds" class="text-2xl sm:text-3xl font-extrabold font-mono text-white mt-1 tabular-nums">0</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <span class="text-xs text-slate-400">Questions Answered</span>
            <div id="stat-answered" class="text-2xl sm:text-3xl font-extrabold font-mono text-white mt-1 tabular-nums">0</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <span class="text-xs text-slate-400">Correct Answers</span>
            <div id="stat-correct" class="text-2xl sm:text-3xl font-extrabold font-mono text-emerald-400 mt-1 tabular-nums">0</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <span class="text-xs text-slate-400">Overall Accuracy</span>
            <div id="stat-accuracy" class="text-2xl sm:text-3xl font-extrabold font-mono text-cyan-400 mt-1 tabular-nums">0%</div>
          </div>
        </div>

        <div class="pt-4 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400">
          <span>Telemetry is preserved across browser sessions.</span>
          <button onclick="clearStats()" class="text-rose-400 hover:text-rose-300 transition-colors font-mono">Reset Telemetry</button>
        </div>
      </div>
    </section>

  </main>

  <!-- ================= MODAL: QUIT CONFIRMATION ================= -->
  <div id="modal-quit" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
    <div class="max-w-md w-full rounded-2xl border border-slate-800 bg-slate-900 p-6 space-y-4 shadow-2xl">
      <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-400 flex items-center justify-center">
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <div class="space-y-1">
        <h3 class="text-lg font-bold font-display text-white">Quit Active Challenge?</h3>
        <p class="text-xs text-slate-300 leading-relaxed">
          You have an active round in progress. If you exit now, your current score, streak, and answers will be lost.
        </p>
      </div>
      <div class="flex items-center justify-end gap-3 pt-2">
        <button onclick="dismissQuitModal()" class="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors">
          Continue Quiz
        </button>
        <button onclick="confirmQuitQuiz()" class="px-4 py-2 text-xs font-bold rounded-lg bg-rose-600 hover:bg-rose-500 text-white transition-colors">
          Quit Challenge
        </button>
      </div>
    </div>
  </div>

  <!-- ================= FOOTER ================= -->
  <footer class="border-t border-slate-800/80 bg-arena-bg py-5 text-xs text-slate-400">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="font-bold text-slate-300 font-display">TechNova</span>
        <span>&middot;</span>
        <span>The Technical Challenge Arena</span>
      </div>
      <div class="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
        <span>{{ total_questions }} Verified Challenges</span>
        <span>&middot;</span>
        <span>Python &middot; DSA &middot; Web &middot; DB &middot; DevOps &middot; CS</span>
      </div>
    </div>
  </footer>

  <!-- ================= CLIENT APPLICATION LOGIC ================= -->
  <script>
    // Injected Backend State
    const RAW_QUESTION_BANK = {{ question_bank_json | safe }};
    const CATEGORIES = {{ categories_json | safe }};
    const CATEGORY_COUNTS = {{ category_counts_json | safe }};
    const TOTAL_QUESTIONS = {{ total_questions }};

    // Client Runtime State
    let selectedCategory = 'All';
    let selectedCount = 10;
    let quizQuestions = [];
    let currentQuestionIdx = 0;
    let currentScore = 0;
    let currentStreak = 0;
    let maxStreak = 0;
    let roundAnswers = []; // History of answers in current round
    let answeredCurrent = false;
    let missedQuestions = [];
    let isQuizActive = false;
    let pendingNavView = null;

    // Timer State
    let timerInterval = null;
    let timerSecondsRemaining = 30;

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
          // Futuristic dual-tone chime
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(523.25, now); // C5
          osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.08); // E5
          osc.frequency.exponentialRampToValueAtTime(783.99, now + 0.16); // G5
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc.start(now);
          osc.stop(now + 0.35);
        } else {
          // Low dampened chime
          osc.type = 'sine';
          osc.frequency.setValueAtTime(240, now);
          osc.frequency.exponentialRampToValueAtTime(160, now + 0.18);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
          osc.start(now);
          osc.stop(now + 0.28);
        }
      } catch (e) {
        // Fallback gracefully if blocked
      }
    }

    function handleAudioToggleChange() {
      if (document.getElementById('sound-toggle').checked) {
        playChime(true);
      }
    }

    // Scroll Helper
    function scrollToSetup() {
      if (isQuizActive) {
        promptQuitQuiz('landing');
        return;
      }
      setView('landing');
      const el = document.getElementById('setup-anchor');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }

    function handleBrandClick(e) {
      e.preventDefault();
      requestView('landing');
    }

    // Navigation and Quit Guard
    function requestView(viewName) {
      if (isQuizActive) {
        promptQuitQuiz(viewName);
        return;
      }
      setView(viewName);
    }

    function promptQuitQuiz(targetView = 'landing') {
      pendingNavView = targetView;
      document.getElementById('modal-quit').classList.remove('hidden');
    }

    function dismissQuitModal() {
      pendingNavView = null;
      document.getElementById('modal-quit').classList.add('hidden');
    }

    function confirmQuitQuiz() {
      clearInterval(timerInterval);
      isQuizActive = false;
      document.getElementById('modal-quit').classList.add('hidden');
      const target = pendingNavView || 'landing';
      pendingNavView = null;
      setView(target);
    }

    function setView(viewName) {
      ['landing', 'quiz', 'results', 'stats'].forEach(v => {
        const el = document.getElementById('view-' + v);
        if (el) el.classList.add('hidden');
      });

      const activeEl = document.getElementById('view-' + viewName);
      if (activeEl) activeEl.classList.remove('hidden');

      // Update Nav active classes
      ['landing', 'stats'].forEach(n => {
        const navEl = document.getElementById('nav-' + n);
        if (navEl) {
          navEl.classList.remove('text-cyan-400', 'font-bold');
          navEl.classList.add('text-slate-400');
        }
      });
      const currentNav = document.getElementById('nav-' + (viewName === 'landing' || viewName === 'quiz' || viewName === 'results' ? 'landing' : viewName));
      if (currentNav) {
        currentNav.classList.add('text-cyan-400', 'font-bold');
        currentNav.classList.remove('text-slate-400');
      }

      if (viewName === 'stats') {
        renderStats();
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Keyboard navigation helper on category cards
    function handleCardKeydown(e, cat) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        selectCategory(cat);
      }
    }

    // Category Selection Logic
    function selectCategory(cat) {
      selectedCategory = cat;
      const available = getAvailableCountForCategory(cat);

      // Visual updates on cards
      document.querySelectorAll('.category-card').forEach(card => {
        const c = card.getAttribute('data-cat');
        const indicator = card.querySelector('.card-indicator');
        if (c === cat) {
          card.classList.add('active', 'border-cyan-500/70', 'bg-gradient-to-br', 'from-cyan-950/40', 'to-slate-900', 'shadow-[0_0_20px_rgba(6,182,212,0.18)]');
          card.classList.remove('border-slate-800', 'bg-slate-900/80');
          if (indicator) {
            indicator.textContent = '✓ SELECTED';
            indicator.className = 'card-indicator font-semibold text-cyan-400';
          }
        } else {
          card.classList.remove('active', 'border-cyan-500/70', 'bg-gradient-to-br', 'from-cyan-950/40', 'to-slate-900', 'shadow-[0_0_20px_rgba(6,182,212,0.18)]');
          card.classList.add('border-slate-800', 'bg-slate-900/80');
          if (indicator) {
            indicator.textContent = 'Select';
            indicator.className = 'card-indicator text-slate-400';
          }
        }
      });

      // Update text summaries
      const catDisplayName = cat === 'All' ? 'All Topics' : cat;
      document.getElementById('selected-category-summary').textContent = `${catDisplayName} · ${available} questions available`;
      document.getElementById('summary-category-pill').textContent = catDisplayName;

      // Update and clamp count selectors
      updateCountSelectorsForCategory(available);
    }

    function getAvailableCountForCategory(cat) {
      if (cat === 'All') return TOTAL_QUESTIONS;
      return CATEGORY_COUNTS[cat] || 0;
    }

    // Question Count Clamping & Configuration
    // Requirement: Do not allow selected question count to exceed available questions in chosen category.
    function updateCountSelectorsForCategory(available) {
      const counts = [5, 10, 20];
      counts.forEach(num => {
        const btn = document.getElementById(`btn-count-5`.replace('5', num));
        if (!btn) return;

        if (num > available) {
          // Disable button
          btn.disabled = true;
          btn.classList.add('opacity-30', 'cursor-not-allowed', 'border-slate-850');
          btn.classList.remove('hover:border-slate-700', 'active', 'border-cyan-500/80', 'text-cyan-300', 'bg-cyan-950/40');
          btn.title = `Exceeds ${available} available questions in this category`;
        } else {
          btn.disabled = false;
          btn.classList.remove('opacity-30', 'cursor-not-allowed', 'border-slate-850');
          btn.classList.add('hover:border-slate-700');
          btn.title = `Choose ${num} questions`;
        }
      });

      // Max/All button is always allowed
      const maxBtn = document.getElementById('btn-count-max');
      if (maxBtn) {
        maxBtn.disabled = false;
        maxBtn.textContent = `All (${available})`;
      }

      // Check if current selectedCount is still valid
      if (selectedCount !== 'max' && parseInt(selectedCount) > available) {
        // Clamp to either largest valid count or 'max'
        if (available >= 10) {
          selectCount(10);
        } else if (available >= 5) {
          selectCount(5);
        } else {
          selectCount('max');
        }
        document.getElementById('count-clamping-msg').textContent = `Adjusted round count to match ${available} available questions in ${selectedCategory}.`;
      } else {
        document.getElementById('count-clamping-msg').textContent = `Select how many challenges to tackle from this discipline.`;
        refreshCountButtonsVisual();
      }
    }

    function selectCount(count) {
      const available = getAvailableCountForCategory(selectedCategory);
      if (count !== 'max' && parseInt(count) > available) {
        count = 'max';
      }

      selectedCount = count;
      refreshCountButtonsVisual();

      const displayCount = count === 'max' ? available : count;
      document.getElementById('count-feedback-hint').textContent = `${displayCount} Questions Selected`;
      document.getElementById('summary-count-pill').textContent = `${displayCount} Questions`;
    }

    function refreshCountButtonsVisual() {
      document.querySelectorAll('.count-btn').forEach(btn => {
        const c = btn.getAttribute('data-count');
        const isActive = (c === 'max' && selectedCount === 'max') || (c == selectedCount);
        if (isActive && !btn.disabled) {
          btn.classList.add('active', 'border-cyan-500/80', 'bg-cyan-950/40', 'text-cyan-300', 'shadow-[0_0_12px_rgba(6,182,212,0.2)]');
          btn.classList.remove('border-slate-800', 'bg-slate-950', 'text-slate-300');
        } else if (!btn.disabled) {
          btn.classList.remove('active', 'border-cyan-500/80', 'bg-cyan-950/40', 'text-cyan-300', 'shadow-[0_0_12px_rgba(6,182,212,0.2)]');
          btn.classList.add('border-slate-800', 'bg-slate-950', 'text-slate-300');
        }
      });
    }

    // Helper: Shuffle array
    function shuffle(arr) {
      const copy = [...arr];
      for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }
      return copy;
    }

    // Start Quiz Routine
    function startQuiz(customQuestionList = null) {
      const timerEnabled = document.getElementById('timer-toggle').checked;
      document.getElementById('summary-timer-pill').textContent = timerEnabled ? '30s Timer' : 'Untimed';

      if (customQuestionList) {
        quizQuestions = customQuestionList;
      } else {
        let pool = RAW_QUESTION_BANK;
        if (selectedCategory !== 'All') {
          pool = pool.filter(q => q[0] === selectedCategory);
        }
        const available = pool.length;
        const count = selectedCount === 'max' ? available : Math.min(parseInt(selectedCount), available);
        const shuffled = shuffle(pool).slice(0, count);

        // Build question items with shuffled A-D options
        quizQuestions = shuffled.map((item, index) => {
          const [cat, text, correct, wrong, explanation] = item;
          const options = shuffle([...wrong, correct]);
          const letters = ['A', 'B', 'C', 'D'];
          const correctIdx = options.indexOf(correct);
          return {
            id: index + 1,
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
      roundAnswers = [];
      answeredCurrent = false;
      isQuizActive = true;

      // Timer UI visibility
      const timerContainer = document.getElementById('quiz-timer-container');
      if (timerEnabled) {
        timerContainer.classList.remove('hidden');
      } else {
        timerContainer.classList.add('hidden');
      }

      setView('quiz');
      renderQuestion();
    }

    // Question Rendering
    function renderQuestion() {
      answeredCurrent = false;
      clearInterval(timerInterval);

      const q = quizQuestions[currentQuestionIdx];
      const total = quizQuestions.length;

      document.getElementById('quiz-cat-badge').textContent = q.category;
      document.getElementById('quiz-current-num').textContent = currentQuestionIdx + 1;
      document.getElementById('quiz-total-num').textContent = total;
      document.getElementById('quiz-live-score').textContent = currentScore;
      document.getElementById('quiz-live-streak').textContent = currentStreak;

      // Progress calculation
      const progressPercent = ((currentQuestionIdx) / total) * 100;
      document.getElementById('quiz-progress-bar').style.width = `${progressPercent}%`;

      // Question Title
      document.getElementById('quiz-question-text').textContent = q.question;
      document.getElementById('quiz-feedback-panel').classList.add('hidden');

      // Populate 4 Options
      const container = document.getElementById('quiz-options-container');
      container.innerHTML = '';

      const letters = ['A', 'B', 'C', 'D'];
      q.options.forEach((optText, idx) => {
        const letter = letters[idx];
        const btn = document.createElement('button');
        btn.className = `option-card w-full text-left p-4 sm:p-4.5 rounded-xl border border-slate-800 bg-slate-950/80 hover:border-cyan-500/50 hover:bg-slate-900/90 flex items-center justify-between text-sm sm:text-base font-medium text-slate-200 cursor-pointer focus:outline-none focus:ring-2 focus:ring-cyan-400`;
        btn.setAttribute('data-letter', letter);
        btn.onclick = () => selectAnswer(letter);

        btn.innerHTML = `
          <div class="flex items-center gap-3.5 flex-1 min-w-0 pr-3">
            <span class="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700 font-mono text-xs font-bold text-cyan-300 flex items-center justify-center shrink-0">
              ${letter}
            </span>
            <span class="text-slate-200 leading-snug break-words">${optText}</span>
          </div>
          <span class="option-status-badge hidden text-xs font-bold font-mono px-2 py-0.5 rounded shrink-0"></span>
        `;
        container.appendChild(btn);
      });

      // Start countdown timer if enabled
      const timerEnabled = document.getElementById('timer-toggle').checked;
      if (timerEnabled) {
        startQuestionTimer();
      }
    }

    // Timer Implementation
    function startQuestionTimer() {
      timerSecondsRemaining = 30;
      const timerEl = document.getElementById('quiz-timer-seconds');
      const timerContainer = document.getElementById('quiz-timer-container');
      timerEl.textContent = timerSecondsRemaining;
      timerContainer.classList.remove('text-rose-400', 'border-rose-500/50');
      timerContainer.classList.add('text-amber-400', 'border-amber-500/30');

      timerInterval = setInterval(() => {
        timerSecondsRemaining--;
        timerEl.textContent = timerSecondsRemaining;

        if (timerSecondsRemaining <= 5) {
          timerContainer.classList.remove('text-amber-400', 'border-amber-500/30');
          timerContainer.classList.add('text-rose-400', 'border-rose-500/50');
        }

        if (timerSecondsRemaining <= 0) {
          clearInterval(timerInterval);
          if (!answeredCurrent) {
            handleTimeExpired();
          }
        }
      }, 1000);
    }

    function handleTimeExpired() {
      selectAnswer(null, true);
    }

    // Answer Selection
    function selectAnswer(chosenLetter, isTimeout = false) {
      if (answeredCurrent) return;
      answeredCurrent = true;
      clearInterval(timerInterval);

      const q = quizQuestions[currentQuestionIdx];
      const isCorrect = chosenLetter === q.correctLetter && !isTimeout;

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

      // Record to lifetime telemetry
      recordAnswer(isCorrect);

      // Save round answer details
      roundAnswers.push({
        question: q,
        chosenLetter: chosenLetter,
        isCorrect: isCorrect,
        isTimeout: isTimeout
      });

      // Update live score display
      document.getElementById('quiz-live-score').textContent = currentScore;
      document.getElementById('quiz-live-streak').textContent = currentStreak;

      // Option Buttons Styling
      const buttons = document.querySelectorAll('#quiz-options-container .option-card');
      buttons.forEach(btn => {
        const letter = btn.getAttribute('data-letter');
        btn.classList.remove('hover:border-cyan-500/50', 'hover:bg-slate-900/90', 'cursor-pointer');
        btn.classList.add('cursor-default');

        const badge = btn.querySelector('.option-status-badge');

        if (letter === q.correctLetter) {
          // Highlight correct answer in emerald/cyan
          btn.classList.add('bg-emerald-950/40', 'border-emerald-500', 'text-emerald-200', 'shadow-[0_0_15px_rgba(16,185,129,0.25)]');
          badge.innerHTML = `&#10003; CORRECT`;
          badge.className = 'option-status-badge text-xs font-bold font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
          badge.classList.remove('hidden');
        } else if (letter === chosenLetter && !isCorrect) {
          // Highlight user's incorrect choice in rose/red
          btn.classList.add('bg-rose-950/40', 'border-rose-500', 'text-rose-200', 'shadow-[0_0_15px_rgba(244,63,94,0.2)]');
          badge.innerHTML = `&#10005; YOUR CHOICE`;
          badge.className = 'option-status-badge text-xs font-bold font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40';
          badge.classList.remove('hidden');
        } else {
          btn.classList.add('opacity-40');
        }
      });

      // Expand Explanation Panel
      const panel = document.getElementById('quiz-feedback-panel');
      const icon = document.getElementById('quiz-feedback-icon');
      const title = document.getElementById('quiz-feedback-title');
      const exp = document.getElementById('quiz-feedback-explanation');

      panel.classList.remove('hidden', 'bg-emerald-950/30', 'border-emerald-500/40', 'bg-rose-950/30', 'border-rose-500/40', 'bg-amber-950/30', 'border-amber-500/40');

      if (isCorrect) {
        panel.classList.add('bg-emerald-950/30', 'border-emerald-500/40');
        icon.className = 'w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-bold text-xs bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
        icon.innerHTML = '&#10003;';
        title.className = 'text-sm font-bold font-display text-emerald-300';
        title.textContent = 'Correct Answer Verified';
      } else if (isTimeout) {
        panel.classList.add('bg-amber-950/30', 'border-amber-500/40');
        icon.className = 'w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-bold text-xs bg-amber-500/20 text-amber-400 border border-amber-500/40';
        icon.innerHTML = '!';
        title.className = 'text-sm font-bold font-display text-amber-300';
        title.textContent = `Time Expired &middot; Correct Answer was Option ${q.correctLetter}: ${q.correctText}`;
      } else {
        panel.classList.add('bg-rose-950/30', 'border-rose-500/40');
        icon.className = 'w-7 h-7 rounded-lg flex items-center justify-center shrink-0 font-bold text-xs bg-rose-500/20 text-rose-400 border border-rose-500/40';
        icon.innerHTML = '&#10005;';
        title.className = 'text-sm font-bold font-display text-rose-300';
        title.textContent = `Incorrect &middot; Correct Answer is Option ${q.correctLetter}: ${q.correctText}`;
      }

      exp.innerHTML = `<span class="font-bold text-slate-400 font-mono">TECHNICAL INSIGHT:</span> ${q.explanation}`;

      const nextLabel = document.getElementById('quiz-next-label');
      if (currentQuestionIdx + 1 >= quizQuestions.length) {
        nextLabel.textContent = 'Finalize & View Scorecard';
      } else {
        nextLabel.textContent = 'Next Challenge';
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

    // Results Screen Routine
    function showResults() {
      clearInterval(timerInterval);
      isQuizActive = false;
      setView('results');

      const total = quizQuestions.length;
      const percent = Math.round((currentScore / total) * 100);
      const incorrectCount = total - currentScore;

      // Update KPI figures
      document.getElementById('results-score-fraction').textContent = `${currentScore} / ${total}`;
      document.getElementById('results-percentage').textContent = `${percent}%`;
      document.getElementById('results-stat-correct').textContent = currentScore;
      document.getElementById('results-stat-incorrect').textContent = incorrectCount;
      document.getElementById('results-stat-streak').textContent = maxStreak;
      document.getElementById('results-stat-cat').textContent = selectedCategory === 'All' ? 'All Topics' : selectedCategory;

      // Animated Circular Ring (circumference = 2 * PI * 50 = 314.16)
      const ring = document.getElementById('results-ring-progress');
      const circumference = 314.16;
      const offset = circumference - (percent / 100) * circumference;
      setTimeout(() => {
        ring.style.strokeDashoffset = offset;
      }, 100);

      // Headline and Tier Assessment
      const headline = document.getElementById('results-headline');
      const subtext = document.getElementById('results-subtext');

      if (percent === 100) {
        headline.textContent = 'Principal Architect Level';
        subtext.textContent = 'Flawless execution! You demonstrated immaculate conceptual mastery across all challenged systems.';
      } else if (percent >= 80) {
        headline.textContent = 'Senior Systems Engineer';
        subtext.textContent = 'Exceptional performance. Strong engineering fundamentals and algorithmic reasoning across the board.';
      } else if (percent >= 60) {
        headline.textContent = 'Core Developer Proficiency';
        subtext.textContent = 'Solid technical foundation. Review the specific architectural gaps below to reach senior-level mastery.';
      } else {
        headline.textContent = 'Foundational Developer';
        subtext.textContent = 'Great effort. Technical mastery develops with repeated exposure. Review the targeted insights below and tackle the arena again!';
      }

      // Review Section Population
      const reviewSection = document.getElementById('results-review-section');
      const reviewList = document.getElementById('results-review-list');
      const retryMissedBtn = document.getElementById('results-retry-missed-btn');

      reviewList.innerHTML = '';

      if (roundAnswers.length > 0) {
        roundAnswers.forEach((ans, idx) => {
          const item = document.createElement('div');
          const isCorrect = ans.isCorrect;
          item.className = `p-4 rounded-xl border ${isCorrect ? 'bg-slate-950/60 border-slate-800' : 'bg-rose-950/20 border-rose-900/50'} space-y-2.5`;
          
          item.innerHTML = `
            <div class="flex items-center justify-between text-xs font-mono">
              <div class="flex items-center gap-2">
                <span class="${isCorrect ? 'text-emerald-400' : 'text-rose-400'} font-bold">
                  ${isCorrect ? '✓ CORRECT' : (ans.isTimeout ? '! TIMEOUT' : '✕ INCORRECT')}
                </span>
                <span class="text-slate-500">&middot;</span>
                <span class="text-slate-400 font-semibold">${ans.question.category}</span>
              </div>
              <span class="text-slate-500">Q${idx + 1}</span>
            </div>
            
            <div class="text-sm font-bold text-white leading-snug">
              ${ans.question.question}
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
              <div class="p-2 rounded-lg bg-emerald-950/40 border border-emerald-500/40 text-emerald-300">
                <span class="text-emerald-400 font-bold">Correct:</span> ${ans.question.correctLetter}. ${ans.question.correctText}
              </div>
              ${!isCorrect ? `
              <div class="p-2 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-300">
                <span class="text-rose-400 font-bold">You Picked:</span> ${ans.chosenLetter ? ans.chosenLetter : 'None (Timeout)'}
              </div>` : ''}
            </div>

            <div class="text-xs text-slate-300 bg-slate-900/80 p-3 rounded-lg border border-slate-800 leading-relaxed font-sans">
              <span class="font-bold text-cyan-400 font-mono text-[11px] block mb-1">ARCHITECTURAL TIP:</span>
              ${ans.question.explanation}
            </div>
          `;
          reviewList.appendChild(item);
        });
      }

      if (missedQuestions.length > 0) {
        retryMissedBtn.classList.remove('hidden');
        document.getElementById('results-missed-count').textContent = missedQuestions.length;
      } else {
        retryMissedBtn.classList.add('hidden');
      }

      recordRoundComplete();
    }

    // Practice Missed Questions Flow
    function retryMissedQuestions() {
      if (!missedQuestions.length) return;
      const retryList = missedQuestions.map((q, idx) => {
        const letters = ['A', 'B', 'C', 'D'];
        const options = shuffle([...q.options]);
        return {
          id: idx + 1,
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

    // Keyboard Shortcuts Handler
    window.addEventListener('keydown', (e) => {
      // Don't trigger if focus is in search input
      if (e.target && e.target.tagName === 'INPUT') return;

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

    // Telemetry LocalStorage Functions
    function getStoredStats() {
      try {
        const data = localStorage.getItem('technova_telemetry');
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
        localStorage.setItem('technova_telemetry', JSON.stringify(stats));
      } catch (e) {}
    }

    function recordRoundComplete() {
      const stats = getStoredStats();
      stats.rounds++;
      try {
        localStorage.setItem('technova_telemetry', JSON.stringify(stats));
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
      if (confirm('Clear all stored TechNova telemetry data?')) {
        localStorage.removeItem('technova_telemetry');
        renderStats();
      }
    }

    // Initialize Default States on page load
    document.addEventListener('DOMContentLoaded', () => {
      selectCategory('All');
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    cat_counts = {}
    for entry in QUESTION_BANK:
        cat = entry[0]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    return render_template_string(
        HTML_TEMPLATE,
        total_questions=len(QUESTION_BANK),
        categories=CATEGORIES,
        category_counts=cat_counts,
        category_details=CATEGORY_DETAILS,
        question_bank_json=json.dumps(QUESTION_BANK),
        categories_json=json.dumps(CATEGORIES),
        category_counts_json=json.dumps(cat_counts)
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
    app.run(host="0.0.0.0", port=port, debug=False)
