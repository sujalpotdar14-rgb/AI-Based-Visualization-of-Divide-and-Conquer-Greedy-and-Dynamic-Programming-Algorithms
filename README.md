# AI-Based Visualization of Divide and Conquer, Greedy and Dynamic Programming Algorithms

An interactive web application designed to help students understand algorithm design techniques through visualizations, algorithm execution, and AI-assisted explanations where implemented.

## 📌 Project Overview

Understanding algorithms can be difficult when students only read theoretical explanations or source code. This project aims to make algorithm learning easier by combining an interactive web interface, a Python backend, and algorithm visualization.

The project focuses on three major algorithmic approaches:

- **Divide and Conquer:** Divide a problem into smaller subproblems, solve them, and combine their results.
- **Greedy Algorithms:** Make locally optimal choices at each step to solve a problem.
- **Dynamic Programming:** Solve overlapping subproblems and reuse stored results to reduce repeated computation.

## 🎯 Objectives

- Make complex algorithms easier to understand.
- Demonstrate algorithm execution through visual representations.
- Help students understand algorithm logic and problem-solving techniques.
- Explore AI-assisted explanations for algorithm learning.
- Provide a practical learning tool for Design and Analysis of Algorithms (DAA).

## ✨ Key Features

- Interactive web-based interface.
- Python backend powered by FastAPI.
- Support for organizing and implementing different algorithm categories.
- Static frontend assets served by the backend.
- Potential integration with Google's Generative AI SDK for AI-based functionality.
- Modular application structure for easier maintenance and future development.

*Note: The availability of individual algorithms, animations, complexity comparisons, and AI-generated explanations depends on their implementation in the source code.*

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development and algorithm implementation |
| FastAPI | Web server and API development |
| HTML | Frontend structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions |
| Google GenAI SDK | Generative AI integration, where configured |
| Git and GitHub | Version control and project hosting |

## 🏗️ Project Structure

```text
AI-Based-Visualization-of-Divide-and-Conquer-
Greedy-and-Dynamic-Programming-Algorithms/
│
├── app/
│   └── Application modules and API routers
│
├── static/
│   ├── index.html
│   └── Frontend assets
│
├── Images/
│   └── Project images and visual assets
│
├── main.py
│   └── FastAPI application entry point
│
├── requirements.txt
│   └── Python dependencies
│
├── run.bat
│   └── Windows startup script
│
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version for the project's dependencies.
- pip, the Python package installer.
- Git (optional, for cloning the repository).
- A modern web browser.

### Step 1: Clone the repository

```bash
git clone https://github.com/sujalpotdar14-rgb/AI-Based-Visualization-of-Divide-and-Conquer-Greedy-and-Dynamic-Programming-Algorithms.git
```

### Step 2: Open the project directory

```bash
cd AI-Based-Visualization-of-Divide-and-Conquer-Greedy-and-Dynamic-Programming-Algorithms
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure environment variables

If the implemented AI functionality requires a Google GenAI API key, configure the appropriate environment variable using the name expected by your source code.

For example, if the application reads `GEMINI_API_KEY`, set it in your terminal:

```cmd
set GEMINI_API_KEY=your_api_key_here
```

Never commit API keys, passwords, or other secrets to GitHub.

### Step 6: Run the application

Start the FastAPI server from the project directory:

```bash
uvicorn main:app --reload
```

If Uvicorn is not installed directly, install it with:

```bash
python -m pip install uvicorn
```

If the repository's `run.bat` script is configured for startup, you can also use that script.

### Step 7: Open the application

Visit the following address in your browser:

- Application: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs

These addresses assume the server is running on the default Uvicorn port and that the application exposes the corresponding routes.

## 🧠 Algorithm Categories

### 1. Divide and Conquer

This technique divides a large problem into smaller subproblems, solves them, and combines their results.

Examples include:
- Merge Sort
- Quick Sort
- Binary Search

### 2. Greedy Algorithms

Greedy algorithms choose the best available local option at each step according to a defined strategy.

Common examples include:
- Activity Selection
- Fractional Knapsack
- Huffman Coding
- Minimum Spanning Tree algorithms

### 3. Dynamic Programming

Dynamic programming stores and reuses solutions to smaller subproblems to avoid unnecessary repeated calculations.

Examples include:
- Fibonacci Sequence
- 0/1 Knapsack
- Longest Common Subsequence
- Matrix Chain Multiplication

*These are representative examples of the three categories, not a verified inventory of the algorithms currently implemented in this repository.*

## 🔄 System Workflow

1. The user opens the web application.
2. The user interacts with the available interface and selects an available operation.
3. The frontend sends requests to the backend when required.
4. The backend processes requests through the relevant application modules.
5. The frontend presents the returned results or visualizations.
6. If AI functionality is implemented and configured, the application can use the relevant AI service for supported tasks.

## 📈 Future Enhancements

- Add step-by-step algorithm animations.
- Display time and space complexity.
- Compare the performance of different algorithms.
- Add input validation and example datasets.
- Provide AI-generated explanations and code walkthroughs.
- Include execution statistics and progress controls.
- Add more algorithms and interactive learning exercises.
- Improve accessibility and responsive design.
- Add automated testing and deployment.

## 🎓 Applications

- Design and Analysis of Algorithms coursework.
- Computer science laboratory demonstrations.
- Algorithm practice and revision.
- Self-paced learning.
- Educational demonstrations of algorithmic problem-solving techniques.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit your changes with a clear message.
5. Open a pull request describing your improvements.

## 👨‍💻 Author

**Sujal Potdar**
**Pratham Gunjal**
**Ashish Sagare**

GitHub: [@sujalpotdar14-rgb](https://github.com/sujalpotdar14-rgb)

## 📄 License

No license has been specified here. If you want others to reuse, modify, or distribute the project, add an appropriate open-source license to the repository.

## ⭐ Support

If you find this project useful for learning algorithms, consider starring the repository on GitHub.

---

**Project:** AI-Based Visualization of Divide and Conquer, Greedy and Dynamic Programming Algorithms

**Purpose:** To make algorithm learning more interactive, visual, and accessible.
