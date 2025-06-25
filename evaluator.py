"""
Evaluation Framework for Math Tutor
Tests strategies and scores responses on multiple metrics
"""

import json
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from test_queries import get_test_problems
from prompt_strategies import get_all_strategies

class MathTutorEvaluator:
    """Main evaluation class for testing prompt strategies"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        self.results = []
        self.test_problems = get_test_problems()
        self.strategies = get_all_strategies()
    
    def extract_final_answer(self, response_text):
        """Extract the final numerical answer from response"""
        # Look for common answer patterns
        patterns = [
            r"(?:Answer|Final Answer|Result):\s*(.+?)(?:\n|$)",
            r"(?:x\s*=\s*|=\s*)([0-9.+-]+)",
            r"([0-9.]+\s*(?:cm²|cm|km/hr|°|degrees)?)",
            r"(\d+/\d+)",  # fractions
            r"(x\s*=\s*[0-9]+(?:\s*or\s*x\s*=\s*[0-9]+)?)"  # multiple solutions
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # If no pattern found, return last line that contains numbers
        lines = response_text.strip().split('\n')
        for line in reversed(lines):
            if re.search(r'[0-9]', line):
                return line.strip()
        
        return "No answer found"
    
    def score_accuracy(self, expected, actual):
        """Score accuracy (0 or 1)"""
        # Normalize both answers for comparison
        expected_clean = re.sub(r'[^\w\d./=\s]', '', str(expected).lower())
        actual_clean = re.sub(r'[^\w\d./=\s]', '', str(actual).lower())
        
        # Check for exact match or key components
        if expected_clean in actual_clean or actual_clean in expected_clean:
            return 1.0
        
        # Check for numerical equality
        try:
            expected_nums = re.findall(r'[0-9.]+', expected_clean)
            actual_nums = re.findall(r'[0-9.]+', actual_clean)
            
            if expected_nums and actual_nums:
                if expected_nums[0] == actual_nums[0]:
                    return 1.0
        except:
            pass
        
        return 0.0
    
    def score_reasoning_clarity(self, response_text):
        """Score reasoning clarity (1-5 scale)"""
        score = 1  # Base score
        
        # Check for step-by-step structure
        if re.search(r'step\s*\d+|first|second|third|next|then|finally', response_text, re.IGNORECASE):
            score += 1
        
        # Check for mathematical explanations
        if re.search(r'because|since|therefore|thus|so|reason|explanation', response_text, re.IGNORECASE):
            score += 1
        
        # Check for formula mentions
        if re.search(r'formula|equation|method|approach|technique', response_text, re.IGNORECASE):
            score += 1
        
        # Check for clear structure (multiple lines, organized)
        lines = response_text.strip().split('\n')
        if len(lines) >= 3:
            score += 1
        
        return min(score, 5)
    
    def score_hallucination(self, response_text, problem_context):
        """Score hallucination (0-3, where 0 is good, 3 is bad)"""
        hallucination_score = 0
        
        # Check for mathematical errors (basic patterns)
        incorrect_facts = [
            r'π\s*=\s*[^2][^2]',  # π not equal to 22/7 or 3.14...
            r'sin\s*30°?\s*=\s*(?!0\.5|1/2)',  # sin 30° should be 0.5
            r'cos\s*90°?\s*=\s*(?!0)',  # cos 90° should be 0
        ]
        
        for pattern in incorrect_facts:
            if re.search(pattern, response_text, re.IGNORECASE):
                hallucination_score += 1
        
        # Check for impossible mathematical statements
        if re.search(r'divide\s+by\s+zero|infinity\s*=|negative\s+square\s+root', response_text, re.IGNORECASE):
            hallucination_score += 1
        
        # Check for contradictory statements
        if re.search(r'always\s+never|never\s+always|impossible\s+possible', response_text, re.IGNORECASE):
            hallucination_score += 1
        
        return min(hallucination_score, 3)
    
    def test_single_problem(self, problem, strategy):
        """Test a single problem with a specific strategy"""
        try:
            prompt = strategy.generate_prompt(problem["problem"])
            response = self.api_client.get_completion(prompt)
            
            # Extract metrics
            final_answer = self.extract_final_answer(response)
            accuracy = self.score_accuracy(problem["expected_answer"], final_answer)
            reasoning = self.score_reasoning_clarity(response)
            hallucination = self.score_hallucination(response, problem)
            
            result = {
                "problem_id": problem["id"],
                "problem_text": problem["problem"],
                "expected_answer": problem["expected_answer"],
                "strategy": strategy.strategy_name,
                "response": response,
                "extracted_answer": final_answer,
                "accuracy_score": accuracy,
                "reasoning_score": reasoning,
                "hallucination_score": hallucination,
                "category": problem["category"],
                "difficulty": problem["difficulty"],
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                "problem_id": problem["id"],
                "strategy": strategy.strategy_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def test_consistency(self, problem, strategy, num_runs=3):
        """Test consistency by running same problem multiple times"""
        responses = []
        for i in range(num_runs):
            result = self.test_single_problem(problem, strategy)
            if "error" not in result:
                responses.append(result["extracted_answer"])
        
        if len(responses) < 2:
            return 0.0
        
        # Check if all responses are the same
        unique_responses = set(responses)
        consistency_score = 1.0 - (len(unique_responses) - 1) / len(responses)
        return consistency_score
    
    def run_full_evaluation(self):
        """Run complete evaluation on all problems and strategies"""
        print("🚀 Starting Math Tutor Evaluation...")
        print(f"Testing {len(self.test_problems)} problems with {len(self.strategies)} strategies")
        
        total_tests = len(self.test_problems) * len(self.strategies)
        current_test = 0
        
        for problem in self.test_problems:
            print(f"\n📝 Testing Problem {problem['id']}: {problem['problem'][:50]}...")
            
            for strategy in self.strategies:
                current_test += 1
                print(f"  [{current_test}/{total_tests}] {strategy.strategy_name}...")
                
                # Run single test
                result = self.test_single_problem(problem, strategy)
                
                # Test consistency
                if "error" not in result:
                    consistency = self.test_consistency(problem, strategy, num_runs=2)
                    result["consistency_score"] = consistency
                
                self.results.append(result)
        
        print("\n✅ Evaluation Complete!")
        return self.results
    
    def generate_comparison_report(self):
        """Generate comprehensive comparison report"""
        if not self.results:
            print("No results to analyze. Run evaluation first.")
            return
        
        # Filter out error results
        valid_results = [r for r in self.results if "error" not in r]
        
        if not valid_results:
            print("No valid results found.")
            return
        
        df = pd.DataFrame(valid_results)
        
        # Strategy comparison
        strategy_stats = df.groupby('strategy').agg({
            'accuracy_score': ['mean', 'std'],
            'reasoning_score': ['mean', 'std'],
            'hallucination_score': ['mean', 'std'],
            'consistency_score': ['mean', 'std']
        }).round(3)
        
        print("\n📊 STRATEGY COMPARISON REPORT")
        print("=" * 50)
        print(strategy_stats)
        
        # Category performance
        print("\n📚 PERFORMANCE BY CATEGORY")
        print("=" * 30)
        category_stats = df.groupby(['category', 'strategy'])['accuracy_score'].mean().unstack()
        print(category_stats.round(3))
        
        # Save detailed results
        self.save_results(df, strategy_stats)
        
        return {
            "strategy_comparison": strategy_stats,
            "category_performance": category_stats,
            "detailed_results": df
        }
    
    def save_results(self, df, summary_stats):
        """Save results to files"""
        # Create results directory
        os.makedirs("results", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        df.to_csv(f"results/detailed_results_{timestamp}.csv", index=False)
        
        # Save summary
        summary_stats.to_csv(f"results/strategy_comparison_{timestamp}.csv")
        
        # Save hallucination log
        hallucination_cases = df[df['hallucination_score'] > 0]
        if not hallucination_cases.empty:
            hallucination_cases[['problem_text', 'strategy', 'response', 'hallucination_score']].to_csv(
                f"results/hallucination_log_{timestamp}.csv", index=False
            )
        
        print(f"\n💾 Results saved to results/ directory with timestamp {timestamp}")
    
    def get_strategy_rankings(self):
        """Get overall strategy rankings"""
        if not self.results:
            return None
        
        valid_results = [r for r in self.results if "error" not in r]
        df = pd.DataFrame(valid_results)
        
        # Calculate overall score (weighted combination)
        df['overall_score'] = (
            df['accuracy_score'] * 0.4 +  # 40% weight on accuracy
            (df['reasoning_score'] / 5.0) * 0.3 +  # 30% weight on reasoning
            (1 - df['hallucination_score'] / 3.0) * 0.2 +  # 20% weight on low hallucination
            df['consistency_score'] * 0.1  # 10% weight on consistency
        )
        
        rankings = df.groupby('strategy')['overall_score'].mean().sort_values(ascending=False)
        
        print("\n🏆 STRATEGY RANKINGS (Overall Score)")
        print("=" * 40)
        for i, (strategy, score) in enumerate(rankings.items(), 1):
            print(f"{i}. {strategy}: {score:.3f}")
        
        return rankings 