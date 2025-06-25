"""
Prompt Engineering Strategies for Math Tutor
Contains Zero-shot, Few-shot, Chain-of-Thought, and Self-ask strategies
"""

import json
from abc import ABC, abstractmethod

class PromptStrategy(ABC):
    """Base class for all prompt strategies"""
    
    def __init__(self, strategy_name):
        self.strategy_name = strategy_name
    
    @abstractmethod
    def generate_prompt(self, problem, context=None):
        """Generate prompt for the given problem"""
        pass
    
    def format_system_prompt(self):
        """Common system prompt for all strategies"""
        return """You are an expert mathematics tutor for students in Class 6-10. 
You are patient, encouraging, and always provide clear step-by-step explanations.
Your goal is to help students understand mathematical concepts, not just get answers.
Always show your working and explain each step clearly."""

class ZeroShotStrategy(PromptStrategy):
    """Direct problem solving without examples"""
    
    def __init__(self):
        super().__init__("Zero-shot")
    
    def generate_prompt(self, problem, context=None):
        system_prompt = self.format_system_prompt()
        
        user_prompt = f"""
Solve this math problem step by step:

Problem: {problem}

Please provide:
1. The solution steps
2. The final answer
3. A brief explanation of the concept used

"""
        return {
            "system": system_prompt,
            "user": user_prompt
        }

class FewShotStrategy(PromptStrategy):
    """Learning from examples before solving"""
    
    def __init__(self):
        super().__init__("Few-shot")
    
    def generate_prompt(self, problem, context=None):
        system_prompt = self.format_system_prompt()
        
        examples = """
Here are some examples of how to solve math problems:

Example 1:
Problem: Solve for x: 3x + 7 = 16
Solution:
Step 1: Subtract 7 from both sides
3x + 7 - 7 = 16 - 7
3x = 9

Step 2: Divide both sides by 3
3x ÷ 3 = 9 ÷ 3
x = 3

Answer: x = 3

Example 2:
Problem: Find the area of a rectangle with length 6 cm and width 4 cm
Solution:
Step 1: Use the area formula for rectangle
Area = length × width

Step 2: Substitute the values
Area = 6 cm × 4 cm = 24 cm²

Answer: 24 cm²

Now solve this problem following the same format:
"""
        
        user_prompt = f"""
{examples}

Problem: {problem}

Please provide:
1. The solution steps (like in the examples)
2. The final answer
3. A brief explanation of the concept used

"""
        return {
            "system": system_prompt,
            "user": user_prompt
        }

class ChainOfThoughtStrategy(PromptStrategy):
    """Step-by-step reasoning approach"""
    
    def __init__(self):
        super().__init__("Chain-of-Thought")
    
    def generate_prompt(self, problem, context=None):
        system_prompt = self.format_system_prompt()
        
        user_prompt = f"""
Let's solve this math problem step by step, thinking through each part carefully:

Problem: {problem}

Let's think step by step:

1. First, let me identify what type of problem this is and what I need to find
2. Then, I'll determine which mathematical concept or formula applies
3. Next, I'll work through the solution step by step
4. Finally, I'll verify my answer makes sense

Please solve this problem following this thinking process, showing all your reasoning and calculations.

"""
        return {
            "system": system_prompt,
            "user": user_prompt
        }

class SelfAskStrategy(PromptStrategy):
    """Agent asks clarifying questions and self-guides"""
    
    def __init__(self):
        super().__init__("Self-ask")
    
    def generate_prompt(self, problem, context=None):
        system_prompt = self.format_system_prompt()
        
        user_prompt = f"""
I need to solve this math problem, but first let me ask myself some important questions to understand it better:

Problem: {problem}

Let me ask myself:
- What exactly is this problem asking me to find?
- What information has been given to me?
- What mathematical concept or formula should I use?
- Are there any special conditions or constraints?
- What would be a reasonable answer range?

Now let me answer these questions and then solve the problem step by step.

"""
        return {
            "system": system_prompt,
            "user": user_prompt
        }

class FallbackHandler:
    """Handles ambiguous or unclear user inputs"""
    
    def __init__(self):
        self.clarification_prompts = {
            "topic": "What specific math topic do you need help with? (e.g., algebra, geometry, arithmetic)",
            "grade": "What grade level is this for? (Class 6, 7, 8, 9, or 10)",
            "problem_type": "What type of problem is this? (e.g., solve equation, find area, calculate percentage)",
            "specific_problem": "Can you provide the exact math problem you want me to solve?"
        }
    
    def is_ambiguous(self, user_input):
        """Check if user input is too vague or ambiguous"""
        ambiguous_keywords = [
            "help", "teach", "explain", "what is", "how to",
            "math", "mathematics", "problem", "solve this"
        ]
        
        # Check if input is very short or contains only ambiguous keywords
        words = user_input.lower().split()
        if len(words) <= 3:
            return any(keyword in user_input.lower() for keyword in ambiguous_keywords)
        
        # Check if it doesn't contain specific math content
        math_indicators = [
            "=", "+", "-", "*", "/", "x", "solve", "find", "calculate",
            "area", "perimeter", "volume", "angle", "triangle", "circle",
            "equation", "algebra", "geometry", "%", "percent"
        ]
        
        has_math_content = any(indicator in user_input.lower() for indicator in math_indicators)
        return not has_math_content
    
    def generate_clarification_prompt(self, user_input):
        """Generate a prompt to ask for clarification"""
        return f"""
I'd like to help you with math, but I need more specific information.

Your input: "{user_input}"

To provide the best help, could you please:

1. **Provide a specific math problem** - For example:
   - "Solve for x: 2x + 5 = 15"
   - "Find the area of a circle with radius 7 cm"
   - "What is 15% of 240?"

2. **Specify the topic** if you want a general explanation:
   - Algebra (equations, expressions)
   - Geometry (area, perimeter, angles)
   - Arithmetic (basic operations, percentages)
   - Trigonometry (sin, cos, tan)

3. **Mention the grade level** (Class 6-10) if relevant

Example formats:
- "Solve: x² - 5x + 6 = 0"
- "Explain how to find the area of a triangle"
- "Help with Class 8 algebra problems"

Please provide your specific math problem or question!
"""

def get_strategy(strategy_name):
    """Factory function to get strategy by name"""
    strategies = {
        "zero-shot": ZeroShotStrategy(),
        "few-shot": FewShotStrategy(), 
        "cot": ChainOfThoughtStrategy(),
        "chain-of-thought": ChainOfThoughtStrategy(),
        "self-ask": SelfAskStrategy()
    }
    
    return strategies.get(strategy_name.lower())

def get_all_strategies():
    """Get all available strategies"""
    return [
        ZeroShotStrategy(),
        FewShotStrategy(),
        ChainOfThoughtStrategy(),
        SelfAskStrategy()
    ] 