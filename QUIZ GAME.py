import random

# Each entry: (category, question, correct answer, [3 wrong answers], explanation)
# To add a new question, just append another tuple to this list.
QUESTION_BANK = [
    # ---------------- Python ----------------
    ("Python", "Which keyword is used to define a function in Python?",
     "def", ["func", "function", "define"],
     "Functions in Python are defined with the 'def' keyword."),
    ("Python", "Which of these data types is immutable?",
     "tuple", ["list", "dict", "set"],
     "Tuples cannot be changed after creation; lists, dicts and sets can."),
    ("Python", "What does the // operator do?",
     "Floor division", ["Exponentiation", "Modulus", "Regular division"],
     "7 // 2 gives 3 - the result is rounded down to the nearest whole number."),
    ("Python", "What is the output of print(2 ** 3)?",
     "8", ["6", "9", "5"],
     "** is the exponent operator, so 2 ** 3 = 2 x 2 x 2 = 8."),
    ("Python", "Which list method adds an item to the end of a list?",
     "append()", ["add()", "push()", "insert_end()"],
     "list.append(x) adds x to the end of the list."),
    ("Python", "What is a decorator in Python?",
     "A function that modifies the behavior of another function",
     ["A way to style output", "A type of loop", "A built-in data type"],
     "Decorators wrap a function to extend its behavior, e.g. @staticmethod."),
    ("Python", "Which block is used to handle exceptions in Python?",
     "try / except", ["do / catch", "begin / rescue", "check / error"],
     "Python uses try/except (and optionally else/finally)."),
    ("Python", "What does PEP 8 describe?",
     "The Python style guide", ["Python's package manager", "Python's memory model", "The Python license"],
     "PEP 8 is the official style guide for writing readable Python code."),
    ("Python", "What is the output of print(bool([]))?",
     "False", ["True", "None", "Error"],
     "Empty collections are 'falsy' in Python."),
    ("Python", "Which keyword creates a generator function?",
     "yield", ["return", "generate", "async"],
     "'yield' pauses the function and produces a value lazily."),

    # ---------------- Data Structures & Algorithms ----------------
    ("DSA", "What is the time complexity of binary search?",
     "O(log n)", ["O(n)", "O(n log n)", "O(1)"],
     "Binary search halves the search space each step."),
    ("DSA", "Which data structure follows the LIFO principle?",
     "Stack", ["Queue", "Linked list", "Heap"],
     "Last In, First Out - the last item pushed is the first popped."),
    ("DSA", "Which data structure follows the FIFO principle?",
     "Queue", ["Stack", "Tree", "Graph"],
     "First In, First Out - like a line of people waiting."),
    ("DSA", "What is the average time complexity of a hash table lookup?",
     "O(1)", ["O(n)", "O(log n)", "O(n^2)"],
     "Hashing lets you jump straight to the bucket, so lookups are constant time on average."),
    ("DSA", "Which sorting algorithm guarantees O(n log n) even in the worst case?",
     "Merge sort", ["Quick sort", "Bubble sort", "Insertion sort"],
     "Quick sort can degrade to O(n^2); merge sort is always O(n log n)."),
    ("DSA", "Which graph traversal algorithm uses a queue?",
     "Breadth-First Search (BFS)", ["Depth-First Search (DFS)", "Dijkstra with a stack", "Binary search"],
     "BFS explores level by level using a queue; DFS uses a stack/recursion."),
    ("DSA", "How many children can a node in a binary tree have at most?",
     "2", ["1", "3", "Unlimited"],
     "'Binary' means each node has at most two children (left and right)."),
    ("DSA", "What data structure does the system use to track function calls?",
     "Call stack", ["Heap", "Queue", "Hash table"],
     "Each function call is pushed onto the call stack and popped on return."),

    # ---------------- Web & Networking ----------------
    ("Web", "Which HTTP status code means 'Not Found'?",
     "404", ["200", "403", "500"],
     "404 means the server can't find the requested resource."),
    ("Web", "Which HTTP status code means 'Internal Server Error'?",
     "500", ["401", "404", "301"],
     "5xx codes indicate a server-side problem."),
    ("Web", "What is the default port for HTTPS?",
     "443", ["80", "21", "8080"],
     "HTTP uses 80, HTTPS uses 443."),
    ("Web", "What does DNS do?",
     "Translates domain names into IP addresses", ["Encrypts web traffic", "Stores website files", "Assigns MAC addresses"],
     "DNS is the internet's phone book for domain names."),
    ("Web", "Which HTTP method is normally used to retrieve data without changing it?",
     "GET", ["POST", "DELETE", "PUT"],
     "GET is safe and idempotent - it only reads data."),
    ("Web", "What does API stand for?",
     "Application Programming Interface", ["Applied Program Integration", "Automated Process Interface", "Application Protocol Index"],
     "An API defines how software components talk to each other."),
    ("Web", "What does JSON stand for?",
     "JavaScript Object Notation", ["Java Standard Output Network", "JavaScript Online Node", "Joint Syntax Object Name"],
     "JSON is a lightweight text format for exchanging data."),
    ("Web", "Which protocol is commonly used to securely log into a remote machine?",
     "SSH", ["FTP", "Telnet", "SMTP"],
     "SSH (Secure Shell) encrypts the connection, unlike Telnet."),

    # ---------------- Databases ----------------
    ("Databases", "Which SQL command is used to retrieve data from a table?",
     "SELECT", ["GET", "FETCH", "EXTRACT"],
     "SELECT is the core SQL query command."),
    ("Databases", "What is a primary key?",
     "A column that uniquely identifies each row", ["A column that stores passwords", "The first column in a table", "An index that allows duplicates"],
     "Primary keys must be unique and not NULL."),
    ("Databases", "Which JOIN returns only the rows that have matches in both tables?",
     "INNER JOIN", ["LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"],
     "INNER JOIN keeps only matching rows."),
    ("Databases", "In ACID, what does the 'A' stand for?",
     "Atomicity", ["Availability", "Accuracy", "Authorization"],
     "Atomicity means a transaction either fully completes or not at all."),
    ("Databases", "Which of these is a NoSQL database?",
     "MongoDB", ["MySQL", "PostgreSQL", "SQLite"],
     "MongoDB is a document-oriented NoSQL database."),

    # ---------------- Git & DevOps ----------------
    ("Git & DevOps", "Which command creates a local copy of a remote repository?",
     "git clone", ["git copy", "git pull", "git fork"],
     "git clone downloads the full repository and its history."),
    ("Git & DevOps", "What does 'git commit' do?",
     "Saves staged changes to the local repository", ["Uploads changes to GitHub", "Creates a new branch", "Downloads remote changes"],
     "Committing records a snapshot locally; 'git push' sends it to the remote."),
    ("Git & DevOps", "'git pull' is a combination of which two commands?",
     "git fetch + git merge", ["git add + git commit", "git clone + git push", "git stash + git apply"],
     "Pull fetches remote changes and merges them into your branch."),
    ("Git & DevOps", "What does CI/CD stand for?",
     "Continuous Integration / Continuous Delivery", ["Code Inspection / Code Debugging", "Central Integration / Central Deployment", "Compiled Instructions / Compiled Data"],
     "CI/CD automates building, testing and releasing software."),

    # ---------------- CS Fundamentals ----------------
    ("CS Basics", "What is the binary representation of decimal 10?",
     "1010", ["1001", "1100", "1110"],
     "8 + 2 = 10, so the bits are 1010."),
    ("CS Basics", "How many bits are in one byte?",
     "8", ["4", "16", "10"],
     "1 byte = 8 bits."),
    ("CS Basics", "What does a compiler do?",
     "Translates source code into machine code", ["Runs code line by line", "Fixes bugs automatically", "Stores variables in memory"],
     "A compiler converts the whole program before it runs; an interpreter runs it line by line."),
    ("CS Basics", "What does the DRY principle stand for?",
     "Don't Repeat Yourself", ["Debug, Run, Yield", "Data Reduction Yield", "Do Recursion Yearly"],
     "DRY encourages reusing code instead of duplicating logic."),
    ("CS Basics", "What does 'encapsulation' mean in OOP?",
     "Bundling data and methods together and restricting direct access",
     ["Creating a new class from an existing one", "Using one interface for many types", "Converting objects to text"],
     "Encapsulation hides internal state behind a class's methods."),
    ("CS Basics", "RAM is best described as which type of memory?",
     "Volatile, temporary memory", ["Permanent storage", "Read-only memory", "Cloud memory"],
     "RAM loses its contents when the power is turned off."),
    ("CS Basics", "Which of these is an operating system kernel?",
     "Linux", ["Python", "Oracle", "Chrome"],
     "Linux is a kernel; Python is a language, Oracle a database, Chrome a browser."),
]

LETTERS = "ABCD"


def build_question(entry):
    """Turn a bank entry into a question with shuffled A-D options."""
    category, text, correct, wrong, explanation = entry
    options = wrong + [correct]
    random.shuffle(options)
    return {
        "category": category,
        "question": text,
        "options": options,
        "answer": LETTERS[options.index(correct)],
        "correct_text": correct,
        "explanation": explanation,
    }


def ask_number_of_questions():
    total = len(QUESTION_BANK)
    while True:
        raw = input(f"How many questions would you like? (1-{total}, default 10): ").strip()
        if raw == "":
            return min(10, total)
        if raw.isdigit() and 1 <= int(raw) <= total:
            return int(raw)
        print(f"Please enter a number between 1 and {total}.")


def ask_question(number, total, q):
    print(f"\nQuestion {number}/{total}  [{q['category']}]")
    print(q["question"])
    for letter, option in zip(LETTERS, q["options"]):
        print(f"  {letter}. {option}")

    while True:
        user_ans = input("Enter your answer (A/B/C/D): ").strip().upper()
        if user_ans in LETTERS:
            break
        print("Invalid input. Please enter A, B, C or D.")

    if user_ans == q["answer"]:
        print("Correct!")
        correct = True
    else:
        print(f"Wrong! The correct answer is {q['answer']}. {q['correct_text']}")
        correct = False
    print(f"Tip: {q['explanation']}")
    return correct


def play_round():
    count = ask_number_of_questions()
    # random.sample picks unique questions, so nothing repeats within a round
    selected = random.sample(QUESTION_BANK, count)

    score = 0
    missed = []
    for i, entry in enumerate(selected, start=1):
        q = build_question(entry)
        if ask_question(i, count, q):
            score += 1
        else:
            missed.append(q)

    percent = score / count * 100
    print("\n" + "=" * 40)
    print(f"Your final score is {score}/{count} ({percent:.0f}%)")
    if percent == 100:
        print("Perfect! You really know your stuff.")
    elif percent >= 70:
        print("Great job! Keep it up.")
    elif percent >= 40:
        print("Not bad - review the tips and try again.")
    else:
        print("Keep practicing - every attempt makes you better!")

    if missed:
        print("\nTopics to review:")
        for q in missed:
            print(f"  - [{q['category']}] {q['question']} -> {q['correct_text']}")


def main():
    print("=== Technical Quiz Game ===")
    print(f"Question bank size: {len(QUESTION_BANK)} questions\n")
    while True:
        play_round()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
