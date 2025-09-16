#!/usr/bin/env python3
"""
Tree-of-Thoughts (ToT) Prompting Implementation

This module demonstrates Tree-of-Thoughts prompting technique which explores
multiple reasoning paths simultaneously and allows backtracking when needed.
"""

import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
)  # if you have not set the env variable


class TreeOfThoughts:
    """
    Implementation of Tree-of-Thoughts reasoning pattern.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.thoughts = []
        self.evaluations = []

    def generate_thoughts(self, problem: str, num_thoughts: int = 3) -> List[str]:
        """
        Generate multiple initial thought paths for a problem.

        Args:
            problem: The problem to solve
            num_thoughts: Number of different thought paths to generate

        Returns:
            List of different reasoning approaches
        """
        prompt = f"""
        I need to solve this problem by exploring multiple different approaches simultaneously.
        
        Problem: {problem}
        
        Generate {num_thoughts} different reasoning approaches or thought paths to solve this problem.
        Each approach should be distinct and explore different angles.
        
        Format your response as:
        Approach 1: [reasoning approach]
        Approach 2: [reasoning approach]
        Approach 3: [reasoning approach]
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert problem solver who can think from multiple perspectives simultaneously.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=800,
            )

            content = response.choices[0].message.content

            # Parse the approaches
            approaches = []
            lines = content.split("\n")
            current_approach = ""

            for line in lines:
                if line.strip().startswith("Approach"):
                    if current_approach:
                        approaches.append(current_approach.strip())
                    current_approach = line.strip()
                elif current_approach and line.strip():
                    current_approach += " " + line.strip()

            if current_approach:
                approaches.append(current_approach.strip())

            self.thoughts = approaches
            return approaches

        except Exception as e:
            return [f"Error generating thoughts: {str(e)}"]

    def evaluate_thoughts(self, thoughts: List[str]) -> List[Dict[str, Any]]:
        """
        Evaluate the quality and feasibility of each thought path.

        Args:
            thoughts: List of thought paths to evaluate

        Returns:
            List of evaluations with scores and reasoning
        """
        evaluations = []

        for i, thought in enumerate(thoughts):
            prompt = f"""
            Evaluate this reasoning approach for solving the problem:
            
            Approach: {thought}
            
            Rate this approach on:
            1. Feasibility (1-10): How practical is this approach?
            2. Completeness (1-10): How well does it address the full problem?
            3. Clarity (1-10): How clear and understandable is the reasoning?
            
            Provide scores and brief explanations for each criterion.
            Also give an overall recommendation: PURSUE, MODIFY, or ABANDON.
            """

            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert evaluator of reasoning approaches.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=400,
                )

                evaluation = {
                    "thought_id": i,
                    "thought": thought,
                    "evaluation": response.choices[0].message.content,
                }
                evaluations.append(evaluation)

            except Exception as e:
                evaluation = {
                    "thought_id": i,
                    "thought": thought,
                    "evaluation": f"Error evaluating: {str(e)}",
                }
                evaluations.append(evaluation)

        self.evaluations = evaluations
        return evaluations

    def expand_best_thought(self, best_thought: str) -> str:
        """
        Expand the best thought path with detailed steps.

        Args:
            best_thought: The selected best reasoning approach

        Returns:
            Detailed step-by-step solution
        """
        prompt = f"""
        Now take this promising reasoning approach and expand it into a complete,
        step-by-step solution:
        
        Selected Approach: {best_thought}
        
        Provide a detailed, step-by-step solution following this approach.
        If you encounter any issues or dead ends, explain them and suggest
        alternative sub-paths within this approach.
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert problem solver who provides detailed step-by-step solutions.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=1000,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error expanding thought: {str(e)}"

    def solve_problem(self, problem: str) -> Dict[str, Any]:
        """
        Solve a problem using Tree-of-Thoughts methodology.

        Args:
            problem: The problem to solve

        Returns:
            Complete ToT solution with all steps
        """
        console.print(f"[bold blue]🌳 Generating multiple thought paths...[/bold blue]")
        thoughts = self.generate_thoughts(problem, 3)

        console.print(f"[bold yellow]🔍 Evaluating thought paths...[/bold yellow]")
        evaluations = self.evaluate_thoughts(thoughts)

        # For demo purposes, select the first thought as "best"
        # In practice, you'd analyze evaluations to pick the best
        best_thought = thoughts[0] if thoughts else ""

        console.print(f"[bold green]🚀 Expanding best thought path...[/bold green]")
        solution = self.expand_best_thought(best_thought)

        return {
            "problem": problem,
            "thoughts": thoughts,
            "evaluations": evaluations,
            "best_thought": best_thought,
            "solution": solution,
        }


def demonstrate_creative_problem():
    """Demonstrates ToT on a creative problem-solving task."""
    problem = """
    Design a public park that serves a diverse urban community with limited space (2 acres)
    and a budget of $500,000. The park should meet the needs of children, elderly residents,
    dog owners, and people who want quiet spaces for reading or meditation.
    """

    console.print(
        Panel("🎨 Creative Problem Solving with Tree-of-Thoughts", style="bold blue")
    )
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")

    tot = TreeOfThoughts()
    result = tot.solve_problem(problem)

    # Display the tree structure
    tree = Tree("🌳 Tree-of-Thoughts Analysis")

    for i, thought in enumerate(result["thoughts"]):
        branch = tree.add(f"💡 Approach {i+1}")
        branch.add(thought[:100] + "..." if len(thought) > 100 else thought)

    console.print(tree)

    console.print("\n[bold yellow]📊 Evaluations:[/bold yellow]")
    for eval_item in result["evaluations"]:
        console.print(
            Panel(
                eval_item["evaluation"], title=f"Approach {eval_item['thought_id']+1}"
            )
        )

    console.print("\n[bold green]🎯 Final Solution:[/bold green]")
    console.print(Markdown(result["solution"]))


def demonstrate_strategic_planning():
    """Demonstrates ToT on a strategic planning problem."""
    problem = """
    A small tech startup has $100K funding and 6 months to achieve product-market fit.
    They have a team of 4 developers and an idea for a productivity app. What strategy
    should they follow to maximize their chances of success?
    """

    console.print(
        Panel("📈 Strategic Planning with Tree-of-Thoughts", style="bold magenta")
    )
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")

    tot = TreeOfThoughts()
    result = tot.solve_problem(problem)

    # Display results in a structured way
    console.print("\n[bold cyan]🧠 Generated Thought Paths:[/bold cyan]")
    for i, thought in enumerate(result["thoughts"]):
        console.print(f"\n[bold]Path {i+1}:[/bold] {thought}")

    console.print("\n[bold green]🏆 Recommended Strategy:[/bold green]")
    console.print(Markdown(result["solution"]))


def demonstrate_complex_decision():
    """Demonstrates ToT on a complex decision-making problem."""
    problem = """
    A family of four needs to decide whether to relocate from a small town to a big city.
    Consider factors like: career opportunities, children's education, cost of living,
    quality of life, proximity to extended family, and long-term financial goals.
    The parents are both teachers, children are 8 and 12 years old.
    """

    console.print(
        Panel("🤔 Complex Decision Making with Tree-of-Thoughts", style="bold green")
    )
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")

    tot = TreeOfThoughts()
    result = tot.solve_problem(problem)

    console.print("\n[bold yellow]🔄 Multi-Path Analysis:[/bold yellow]")

    # Create a visual tree for the analysis
    decision_tree = Tree("🏠 Relocation Decision Analysis")

    for i, thought in enumerate(result["thoughts"]):
        path_branch = decision_tree.add(f"📋 Analysis Path {i+1}")
        # Add evaluation summary
        eval_text = (
            result["evaluations"][i]["evaluation"][:150] + "..."
            if len(result["evaluations"][i]["evaluation"]) > 150
            else result["evaluations"][i]["evaluation"]
        )
        path_branch.add(eval_text)

    console.print(decision_tree)

    console.print("\n[bold green]💡 Decision Recommendation:[/bold green]")
    console.print(Markdown(result["solution"]))


def interactive_tot_mode():
    """Interactive mode for Tree-of-Thoughts problem solving."""
    console.print(Panel("🌳 Interactive Tree-of-Thoughts Mode", style="bold cyan"))
    console.print(
        "Enter complex problems that benefit from exploring multiple approaches!"
    )
    console.print("Type 'quit' to exit.\n")

    tot = TreeOfThoughts()

    while True:
        try:
            problem = input("Your complex problem: ").strip()

            if problem.lower() in ["quit", "exit", "q"]:
                console.print("👋 Goodbye!")
                break

            if not problem:
                console.print("Please enter a problem to analyze.")
                continue

            console.print(
                "\n[bold blue]🌳 Analyzing with Tree-of-Thoughts...[/bold blue]"
            )
            result = tot.solve_problem(problem)

            console.print(
                f"\n[bold yellow]Generated {len(result['thoughts'])} different approaches:[/bold yellow]"
            )
            for i, thought in enumerate(result["thoughts"]):
                console.print(f"\n{i+1}. {thought}")

            console.print("\n[bold green]🎯 Recommended Solution:[/bold green]")
            console.print(Markdown(result["solution"]))
            console.print("\n" + "=" * 60 + "\n")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main function to run Tree-of-Thoughts demonstrations."""
    console.print(
        Panel.fit(
            "🌳 Tree-of-Thoughts (ToT) Prompting Demonstration",
            style="bold white on green",
        )
    )

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set![/red]")
        console.print("Please set your OpenAI API key in the .env file.")
        sys.exit(1)

    console.print("\n[bold]What is Tree-of-Thoughts (ToT) Prompting?[/bold]")
    console.print(
        """
Tree-of-Thoughts prompting explores multiple reasoning paths simultaneously,
allowing AI to consider different approaches and backtrack when needed. This is
especially useful for creative problems, strategic planning, and complex decisions.
    """
    )

    # Run demonstrations
    console.print("\n" + "=" * 70)
    demonstrate_creative_problem()

    console.print("\n" + "=" * 70)
    demonstrate_strategic_planning()

    console.print("\n" + "=" * 70)
    demonstrate_complex_decision()

    console.print("\n" + "=" * 70)

    # Ask if user wants interactive mode
    console.print(
        "\n[bold]Would you like to try Tree-of-Thoughts on your own problems? (y/n)[/bold]"
    )
    choice = input().strip().lower()

    if choice in ["y", "yes"]:
        interactive_tot_mode()
    else:
        console.print("🌳 Tree-of-Thoughts demonstration complete!")


if __name__ == "__main__":
    main()
