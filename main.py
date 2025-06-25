"""
Math Tutor CLI - Main Interface
EdTech Math Tutor for Class 6-10 using LM Studio with Llama-3.1-8B-Instruct
"""

import argparse
import requests
import json
import sys
from colorama import init, Fore, Style
from prompt_strategies import get_strategy, get_all_strategies, FallbackHandler
from evaluator import MathTutorEvaluator
from test_queries import get_test_problems

# Initialize colorama for colored output
init()

class LMStudioClient:
    """Client for LM Studio API integration"""
    
    def __init__(self, base_url="http://localhost:1234", model_name="meta-llama-3.1-8b-instruct"):
        self.base_url = base_url
        self.model_name = model_name
        self.headers = {"Content-Type": "application/json"}
    
    def test_connection(self):
        """Test if LM Studio is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json().get("data", [])
                print(f"✅ Connected to LM Studio. Available models: {len(models)}")
                return True
            else:
                print(f"❌ LM Studio responded with status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to LM Studio: {e}")
            print("💡 Make sure LM Studio is running on http://localhost:1234")
            return False
    
    def get_completion(self, prompt_dict, max_tokens=1000, temperature=0.1):
        """Get completion from LM Studio"""
        try:
            # Format prompt for LM Studio API
            messages = [
                {"role": "system", "content": prompt_dict["system"]},
                {"role": "user", "content": prompt_dict["user"]}
            ]
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=120  # Increased to 2 minutes for model loading
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: API returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return f"Error: Connection failed - {e}"
        except Exception as e:
            return f"Error: {e}"

class MathTutorCLI:
    """Main CLI application"""
    
    def __init__(self):
        self.client = LMStudioClient()
        self.fallback_handler = FallbackHandler()
        
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                    🧮 MATH TUTOR CLI                         ║
║              EdTech Assistant for Class 6-10                 ║
║                  Powered by Llama-3.1-8B                     ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def print_help(self):
        """Print usage help"""
        help_text = f"""
{Fore.YELLOW}📚 USAGE EXAMPLES:{Style.RESET_ALL}

{Fore.GREEN}Interactive Problem Solving:{Style.RESET_ALL}
  python main.py --problem "Solve for x: 2x + 5 = 15" --strategy cot
  python main.py --problem "Find area of circle with radius 7 cm" --strategy few-shot
  python main.py --problem "What is 15% of 240?" --strategy zero-shot

{Fore.GREEN}Batch Evaluation:{Style.RESET_ALL}
  python main.py --evaluate                    # Test all strategies
  python main.py --evaluate --strategy cot     # Test only Chain-of-Thought

{Fore.GREEN}Available Strategies:{Style.RESET_ALL}
  • zero-shot      - Direct problem solving
  • few-shot       - Learning from examples  
  • cot            - Chain-of-thought reasoning
  • self-ask       - Self-questioning approach

{Fore.GREEN}Domain Coverage:{Style.RESET_ALL}
  Class 6-10 Mathematics: Algebra, Geometry, Arithmetic, Trigonometry, 
  Percentages, Speed-Distance-Time, Area-Perimeter, etc.
"""
        print(help_text)
    
    def solve_single_problem(self, problem_text, strategy_name):
        """Solve a single math problem interactively"""
        print(f"\n{Fore.BLUE}🔍 Analyzing Problem...{Style.RESET_ALL}")
        print(f"Problem: {problem_text}")
        print(f"Strategy: {strategy_name}")
        
        # Check if input is ambiguous
        if self.fallback_handler.is_ambiguous(problem_text):
            print(f"\n{Fore.YELLOW}⚠️  Input seems ambiguous. Let me help clarify...{Style.RESET_ALL}")
            clarification = self.fallback_handler.generate_clarification_prompt(problem_text)
            print(clarification)
            return
        
        # Get strategy
        strategy = get_strategy(strategy_name)
        if not strategy:
            print(f"{Fore.RED}❌ Unknown strategy: {strategy_name}{Style.RESET_ALL}")
            print("Available strategies: zero-shot, few-shot, cot, self-ask")
            return
        
        # Generate prompt and get response
        print(f"\n{Fore.BLUE}🤔 Thinking with {strategy.strategy_name} approach...{Style.RESET_ALL}")
        prompt = strategy.generate_prompt(problem_text)
        
        try:
            response = self.client.get_completion(prompt)
            
            print(f"\n{Fore.GREEN}✅ SOLUTION:{Style.RESET_ALL}")
            print("=" * 60)
            print(response)
            print("=" * 60)
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting response: {e}{Style.RESET_ALL}")
    
    def run_evaluation(self, specific_strategy=None):
        """Run batch evaluation of all strategies"""
        print(f"\n{Fore.BLUE}🧪 Starting Evaluation Mode...{Style.RESET_ALL}")
        
        evaluator = MathTutorEvaluator(self.client)
        
        if specific_strategy:
            # Test only specific strategy
            strategy = get_strategy(specific_strategy)
            if not strategy:
                print(f"{Fore.RED}❌ Unknown strategy: {specific_strategy}{Style.RESET_ALL}")
                return
            
            print(f"Testing only: {strategy.strategy_name}")
            evaluator.strategies = [strategy]
        
        # Run evaluation
        results = evaluator.run_full_evaluation()
        
        # Generate and display report
        print(f"\n{Fore.CYAN}📊 GENERATING EVALUATION REPORT...{Style.RESET_ALL}")
        report = evaluator.generate_comparison_report()
        
        # Show rankings
        evaluator.get_strategy_rankings()
        
        print(f"\n{Fore.GREEN}✅ Evaluation complete! Check 'results/' folder for detailed reports.{Style.RESET_ALL}")
    
    def interactive_mode(self):
        """Interactive conversation mode"""
        print(f"\n{Fore.CYAN}💬 Interactive Mode - Type 'quit' to exit{Style.RESET_ALL}")
        
        while True:
            try:
                problem = input(f"\n{Fore.YELLOW}🧮 Enter your math problem: {Style.RESET_ALL}")
                
                if problem.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.CYAN}👋 Goodbye! Happy learning!{Style.RESET_ALL}")
                    break
                
                strategy = input(f"{Fore.YELLOW}📝 Choose strategy (zero-shot/few-shot/cot/self-ask): {Style.RESET_ALL}")
                
                if not strategy:
                    strategy = "cot"  # Default to chain-of-thought
                
                self.solve_single_problem(problem, strategy)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}👋 Goodbye! Happy learning!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    
    def run(self, args):
        """Main application runner"""
        self.print_banner()
        
        # Test LM Studio connection
        if not self.client.test_connection():
            print(f"\n{Fore.RED}❌ Cannot proceed without LM Studio connection{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Setup Instructions:{Style.RESET_ALL}")
            print("1. Download and install LM Studio")
            print("2. Load the meta-llama-3.1-8b-instruct model")
            print("3. Start the local server on http://localhost:1234")
            print("4. Try running this script again")
            return
        
        # Handle different modes
        if args.help_examples:
            self.print_help()
            
        elif args.evaluate:
            self.run_evaluation(args.strategy)
            
        elif args.problem:
            if not args.strategy:
                print(f"{Fore.YELLOW}⚠️  No strategy specified, using Chain-of-Thought (cot){Style.RESET_ALL}")
                args.strategy = "cot"
            
            self.solve_single_problem(args.problem, args.strategy)
            
        elif args.interactive:
            self.interactive_mode()
            
        else:
            print(f"{Fore.YELLOW}ℹ️  No specific action requested. Use --help for options or --interactive for chat mode.{Style.RESET_ALL}")
            self.print_help()

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="🧮 Math Tutor CLI - EdTech Assistant for Class 6-10",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main action arguments
    parser.add_argument("--problem", "-p", type=str, help="Math problem to solve")
    parser.add_argument("--strategy", "-s", type=str, 
                       choices=["zero-shot", "few-shot", "cot", "chain-of-thought", "self-ask"],
                       help="Prompt strategy to use")
    parser.add_argument("--evaluate", "-e", action="store_true", 
                       help="Run batch evaluation on test problems")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Start interactive conversation mode")
    parser.add_argument("--help-examples", action="store_true",
                       help="Show detailed usage examples")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run application
    app = MathTutorCLI()
    app.run(args)

if __name__ == "__main__":
    main() 