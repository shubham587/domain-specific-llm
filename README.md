# 🧮 Math Tutor CLI - EdTech Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LM Studio](https://img.shields.io/badge/LM%20Studio-Compatible-green.svg)](https://lmstudio.ai)

**Domain-Specific LLM Agent for Class 6-10 Mathematics Education**

A sophisticated Math Tutor CLI application that demonstrates advanced prompt engineering strategies using local LLMs via LM Studio. This project implements and evaluates four different prompting approaches for educational AI applications.

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation & Setup](#-installation--setup)
- [🎬 Demo](#-demo)
- [🔧 Core Features](#-core-features)
- [💻 Usage Examples](#-usage-examples)
- [📊 Evaluation Results](#-evaluation-results)
- [🏗️ Repository Structure](#️-repository-structure)
- [🎯 Assignment Deliverables Mapping](#-assignment-deliverables-mapping)
- [🔧 Troubleshooting](#-troubleshooting)
- [📖 Additional Documentation](#-additional-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

- 🎯 **Four Prompt Engineering Strategies**: Zero-shot, Few-shot, Chain-of-Thought, and Self-ask
- 📊 **Comprehensive Evaluation Framework**: Multi-metric scoring system with accuracy, reasoning, hallucination detection, and consistency testing
- 🛡️ **Intelligent Fallback Mechanism**: Handles ambiguous inputs with clarification prompts
- 🧮 **Educational Focus**: Designed specifically for Class 6-10 mathematics curriculum
- 💻 **CLI Interface**: Beautiful, user-friendly command-line interface with colored output
- 📈 **Batch Evaluation**: Automated testing across all strategies and problems
- 🔄 **Interactive Mode**: Conversational interface for continuous problem-solving
- 📋 **Detailed Reporting**: CSV exports with timestamps and comprehensive analysis

## 📋 Assignment Context

**Domain**: EdTech Math Tutor for Class 6-10 curriculum  
**Technology**: LM Studio + meta-llama-3.1-8b-instruct  
**Focus**: Prompt engineering, evaluation, and comparison of different strategies

### 🎯 Three Representative User Tasks

1. **Step-by-step Problem Solving**: "Solve for x: 2x + 5 = 15"
2. **Concept Explanation**: "Explain how to find the area of a circle"  
3. **Student Work Verification**: "Check if this solution is correct: [student work]"

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows
- 8GB+ RAM recommended for local LLM inference

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd math-tutor-cli
```

### 2. LM Studio Setup
- Download [LM Studio](https://lmstudio.ai) for your operating system
- Install and launch LM Studio
- Download the `meta-llama-3.1-8b-instruct` model (recommended)
- Start the local server on `http://localhost:1234`

### 3. Python Environment Setup
   ```bash
   # Create and activate virtual environment
   python -m venv math_tutor_env
   source math_tutor_env/bin/activate  # On macOS/Linux
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

### 4. Quick Start

```bash
# Activate virtual environment first
source math_tutor_env/bin/activate

# Test the connection and see examples
python main.py --help-examples

# Solve a single problem
python main.py --problem "Solve: 2x + 5 = 15" --strategy cot

# Run evaluation on all strategies
python main.py --evaluate

# Interactive mode
python main.py --interactive
```

## 🎬 Demo

### Single Problem Solving
```bash
python main.py --problem "Find the area of a circle with radius 5 cm" --strategy cot
```

**Output:**
```
🔍 Analyzing Problem...
Problem: Find the area of a circle with radius 5 cm
Strategy: cot

🤔 Thinking with Chain-of-Thought approach...

✅ SOLUTION:
============================================================
Let me solve this step by step:

1. First, I need to identify what we're looking for: the area of a circle
2. The formula for the area of a circle is: A = πr²
3. Given information: radius (r) = 5 cm
4. Substituting into the formula: A = π × (5)²
5. Calculating: A = π × 25 = 25π cm²
6. Using π ≈ 3.14159: A ≈ 78.54 cm²

Therefore, the area of the circle is 25π cm² or approximately 78.54 cm².
============================================================
```

### Batch Evaluation Results
```
🏆 STRATEGY RANKINGS (Overall Score)
========================================
1. Chain-of-Thought: 0.847
2. Few-shot: 0.823  
3. Self-ask: 0.791
4. Zero-shot: 0.765
```

## 🔧 Core Features

### 🎯 **4 Prompt Engineering Strategies**

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Zero-shot** | Direct problem solving without examples | Quick, straightforward problems |
| **Few-shot** | Learning from 2-3 examples before solving | Complex problems needing context |
| **Chain-of-Thought** | Step-by-step reasoning process | Problems requiring detailed explanation |
| **Self-ask** | Agent asks clarifying questions first | Ambiguous or multi-part problems |

### 📊 **Evaluation Framework**

**Metrics Measured**:
- **Accuracy** (0-1): Correctness of final answer
- **Reasoning Clarity** (1-5): Quality of step-by-step explanation  
- **Hallucination Score** (0-3): Mathematical errors or false statements
- **Consistency** (0-1): Same answer for repeated queries

### 🛡️ **Fallback Mechanism**

Handles ambiguous inputs like:
- "help with math"
- "solve this problem" 
- "I need help"

Provides clarification prompts to guide users toward specific problems.

## 📚 Test Dataset

**8 Curated Problems** covering Class 6-10 curriculum:

| Problem | Category | Grade | Difficulty |
|---------|----------|-------|------------|
| Linear equations | Algebra | 8-9 | Medium |
| Circle area | Geometry | 7-8 | Medium |
| Percentage calculation | Arithmetic | 6-7 | Easy |
| Quadratic equations | Algebra | 10 | Hard |
| Speed-distance-time | Physics-Math | 7-8 | Easy |
| Trigonometry | Advanced | 10 | Medium |
| Algebraic expressions | Algebra | 8 | Easy |
| Rectangle perimeter | Geometry | 6-7 | Medium |

## 💻 Usage Examples

### Interactive Problem Solving

```bash
# Activate environment first
source math_tutor_env/bin/activate

# Zero-shot approach
python main.py --problem "What is 15% of 240?" --strategy zero-shot

# Few-shot with examples
python main.py --problem "Solve: x² - 5x + 6 = 0" --strategy few-shot

# Chain-of-thought reasoning
python main.py --problem "Find area of circle with radius 7 cm" --strategy cot

# Self-questioning approach
python main.py --problem "A train travels 120 km in 2 hours. What is its speed?" --strategy self-ask
```

### Batch Evaluation

```bash
# Activate environment first
source math_tutor_env/bin/activate

# Test all strategies on all problems (32 total tests)
python main.py --evaluate

# Test only Chain-of-Thought strategy
python main.py --evaluate --strategy cot

# Results saved to results/ directory with timestamps
```

### Interactive Mode

```bash
# Activate environment first
source math_tutor_env/bin/activate

python main.py --interactive
# Provides conversational interface for continuous problem solving
```

## 📊 Evaluation Results

After running evaluation, you'll get:

1. **Strategy Comparison Report**: Performance metrics for each prompt strategy
2. **Strategy Rankings**: Overall scores with weighted metrics displayed in terminal
3. **Detailed CSV Reports**: Timestamped results in `results/` folder
   - `detailed_results_[timestamp].csv` - Individual test results
   - `strategy_comparison_[timestamp].csv` - Summary comparison

### Sample Output
```
🏆 STRATEGY RANKINGS (Overall Score)
========================================
1. Chain-of-Thought: 0.847
2. Few-shot: 0.823  
3. Self-ask: 0.791
4. Zero-shot: 0.765
```

## 🏗️ Repository Structure

```
math-tutor-cli/
├── main.py                        # CLI interface & LM Studio integration
├── prompt_strategies.py           # 4 prompt strategies + fallback handler
├── evaluator.py                   # Testing framework & scoring system
├── test_queries.py               # 8 curated test problems dataset
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── ASSIGNMENT_METHODOLOGY.md     # Technical methodology & analysis
├── math_tutor_env/              # Virtual environment (created after setup)
└── results/                     # Generated evaluation reports (created after runs)
    ├── detailed_results_[timestamp].csv
    └── strategy_comparison_[timestamp].csv
```

## 🎯 Assignment Deliverables Mapping

### **Part 1**: Domain Understanding ✅
- **Domain**: EdTech Math Tutor (Class 6-10)
- **User Tasks**: Problem solving, concept explanation, work verification
- **Implementation**: `test_queries.py` + documentation

### **Part 2**: Prompt Engineering ✅  
- **4 Strategies**: Zero-shot, Few-shot, CoT, Self-ask in `prompt_strategies.py`
- **Fallback Mechanism**: Ambiguity detection and clarification
- **Automation**: Batch testing framework in `evaluator.py`
- **Hallucination Logging**: Automatic detection and reporting

### **Part 3**: Evaluation & Analysis ✅
- **Accuracy**: Correct answer matching
- **Reasoning**: Step-by-step clarity scoring  
- **Hallucination**: Mathematical error detection
- **Consistency**: Repeated query testing
- **Comparison**: Strategy performance analysis

## 🔧 Troubleshooting

### Common Issues

1. **LM Studio Connection Failed**:
   ```bash
   # Ensure LM Studio is running with server started
   # Check http://localhost:1234 is accessible
   ```

2. **Model Not Found**:
   ```bash
   # Download meta-llama-3.1-8b-instruct in LM Studio
   # Ensure model is loaded before starting server
   ```

3. **Virtual Environment Issues**:
   ```bash
   # Make sure to activate the virtual environment
   source math_tutor_env/bin/activate
   
   # If modules are missing, reinstall dependencies
   pip install -r requirements.txt
   ```

4. **Memory Issues on M1 Mac**:
   ```bash
   # Use Phi-3-Mini or Mistral-7B if Llama is too large
   # Adjust model in main.py LMStudioClient initialization
   ```

## 📖 Additional Documentation

For comprehensive technical details, methodology, and implementation insights, see:
- **`ASSIGNMENT_METHODOLOGY.md`** - Complete technical documentation explaining:
  - Detailed workflow and architecture
  - In-depth prompt strategy analysis
  - Evaluation methodology and scoring systems
  - Strategy effectiveness analysis
  - Implementation details and rationale

