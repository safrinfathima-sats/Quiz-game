questions = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A. Mars", "B. Venus", "C. Jupiter", "D. Saturn"],
        "answer": "A"
    },
    {
        "question": "Which language is used to create this program?",
        "options": ["A. C++", "B. Python", "C. Java", "D. Ruby"],
        "answer": "B"
    },
    {
        "question": "What is the boiling point of water (in °C)?",
        "options": ["A. 90", "B. 100", "C. 110", "D. 120"],
        "answer": "B"
    },
    {
        "question": "Which animal is known as the 'King of the Jungle'?",
        "options": ["A. Tiger", "B. Lion", "C. Elephant", "D. Bear"],
        "answer": "B"
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
        "answer": "C"
    }
]

score = 0
for q in questions:
    print(q["question"])
    for opt in q["options"]:
        print(opt)
    user_ans = input("Enter your answer (A/B/C/D): ").upper()
    if user_ans == q["answer"]:
        print("Correct!\n")
        score += 1
    else:
        print(f"Wrong! Correct answer is {q['answer']}\n")

print(f"Your final score is {score}/{len(questions)}")