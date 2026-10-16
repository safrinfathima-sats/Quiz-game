# Technical & General Quiz Game

A modern interactive web quiz application rewritten in React, TypeScript, and Tailwind CSS from the original Python console quiz games (`QUIZ GAME.py` and `quiz_game.py`).

## Features Ported & Enhanced

- **Comprehensive Question Bank**: 47 curated questions across 7 core computer science & general knowledge categories:
  - Python (syntax, decorators, PEP 8, generators, data structures)
  - Data Structures & Algorithms (time complexities, LIFO/FIFO, tree traversal, hashing)
  - Web & Networking (HTTP status codes, ports, DNS, JSON, REST APIs, SSH)
  - Databases (SQL queries, primary keys, JOINs, ACID properties, NoSQL)
  - Git & DevOps (clone, commit, pull mechanics, CI/CD)
  - Computer Science Fundamentals (binary, memory volatility, compilers, DRY, OOP encapsulation)
  - General Trivia (planets, language history, science trivia)
- **Randomized Options**: Questions shuffle choices (A, B, C, D) dynamically each round with immediate correctness validation.
- **Instant Explanations & Tips**: Educational feedback tips displayed after answering every question.
- **Customizable Rounds**: Select category filters and customize question count (from 1 to 47 questions).
- **Keyboard Shortcuts**: Swift gameplay with keyboard keys `A`, `B`, `C`, `D` (or `1`, `2`, `3`, `4`) and `Enter` / `Space` to advance.
- **Performance Evaluation**: Preserves original score brackets and feedback messages:
  - 100%: *"Perfect! You really know your stuff."*
  - ≥ 70%: *"Great job! Keep it up."*
  - ≥ 40%: *"Not bad - review the tips and try again."*
  - < 40%: *"Keep practicing - every attempt makes you better!"*
- **Missed Questions & Practice Retry**: Review missed topics and launch a focused practice session on questions you missed.
- **Retro CLI Mode**: Full in-browser Python terminal emulator reproducing the authentic terminal CLI experience.

## Tech Stack

- **Framework**: React 19 + TypeScript
- **Bundler**: Vite 6
- **Styling**: Tailwind CSS v4
- **Icons**: Lucide React
- **Celebration Effects**: Canvas Confetti

## Getting Started

```bash
npm install
npm run dev
```

The application runs on port 3000 at `http://localhost:3000`.
