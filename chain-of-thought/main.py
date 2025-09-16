#!/usr/bin/env python3
"""
Chain-of-Thought (CoT) Prompting Implementation

This module demonstrates Chain-of-Thought prompting technique which guides AI
to break down complex problems into sequential reasoning steps.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
)  # if you have not set the env variable


def cot_prompt_template(problem: str) -> str:
    """
    Creates a Chain-of-Thought prompt template for problem solving.

    Args:
        problem: The problem to solve using CoT reasoning

    Returns:
        Formatted CoT prompt
    """
    return f"""
I need to solve this problem step by step using clear reasoning.

Problem: {problem}

Let me think through this step by step:

Step 1: First, I'll identify what the problem is asking for.
Step 2: Then, I'll break down the problem into smaller components.
Step 3: I'll work through each component systematically.
Step 4: Finally, I'll combine my findings to reach the final answer.

Let me work through this:
"""


def solve_with_cot(problem: str, model: str = "gpt-4") -> str:
    """
    Solves a problem using Chain-of-Thought prompting.

    Args:
        problem: The problem to solve
        model: The OpenAI model to use

    Returns:
        The AI's step-by-step reasoning and solution
    """
    prompt = cot_prompt_template(problem)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert problem solver who thinks step by step. Always show your reasoning clearly and explicitly.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,  # Lower temperature for more consistent reasoning
            max_tokens=1000,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def demonstrate_math_problem():
    """Demonstrates CoT on a mathematical problem."""
    problem = """
    A bakery sells cupcakes for $3 each and cookies for $1.50 each. 
    Sarah bought some cupcakes and cookies, spending exactly $24. 
    If she bought twice as many cookies as cupcakes, how many of each did she buy?
    """

    console.print(Panel("🧮 Mathematical Problem Solving with CoT", style="bold blue"))
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")
    console.print("\n[bold yellow]Chain-of-Thought Reasoning:[/bold yellow]\n")

    solution = solve_with_cot(problem)
    console.print(Markdown(solution))


def demonstrate_logical_reasoning():
    """Demonstrates CoT on a logical reasoning problem."""
    problem = """
    In a classroom, there are 30 students. 18 students play basketball, 
    12 students play soccer, and 8 students play both basketball and soccer. 
    How many students play neither basketball nor soccer?
    """

    console.print(Panel("🤔 Logical Reasoning with CoT", style="bold green"))
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")
    console.print("\n[bold yellow]Chain-of-Thought Reasoning:[/bold yellow]\n")

    solution = solve_with_cot(problem)
    console.print(Markdown(solution))


def demonstrate_complex_analysis():
    """Demonstrates CoT on a complex analysis problem."""
    problem = """
    A company's quarterly revenue has been: Q1: $100K, Q2: $120K, Q3: $135K, Q4: $150K.
    Analyze the growth pattern and predict the revenue for the next two quarters.
    Consider potential factors that might affect growth and provide a reasoned prediction.
    """

    console.print(Panel("📊 Business Analysis with CoT", style="bold magenta"))
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")
    console.print("\n[bold yellow]Chain-of-Thought Reasoning:[/bold yellow]\n")

    solution = solve_with_cot(problem)
    console.print(Markdown(solution))


def interactive_mode():
    """Allows users to input their own problems for CoT solving."""
    console.print(Panel("🎯 Interactive Chain-of-Thought Mode", style="bold cyan"))
    console.print("Enter your own problem to solve with Chain-of-Thought reasoning!")
    console.print("Type 'quit' to exit.\n")

    while True:
        try:
            problem = input("Your problem: ").strip()

            if problem.lower() in ["quit", "exit", "q"]:
                console.print("👋 Goodbye!")
                break

            if not problem:
                console.print("Please enter a problem to solve.")
                continue

            console.print("\n[bold yellow]Chain-of-Thought Reasoning:[/bold yellow]\n")
            solution = solve_with_cot(problem)
            console.print(Markdown(solution))
            console.print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main function to run Chain-of-Thought demonstrations."""
    console.print(
        Panel.fit(
            "🔗 Chain-of-Thought (CoT) Prompting Demonstration",
            style="bold white on blue",
        )
    )

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set![/red]")
        console.print("Please set your OpenAI API key in the .env file.")
        sys.exit(1)

    console.print("\n[bold]What is Chain-of-Thought (CoT) Prompting?[/bold]")
    console.print(
        """
Chain-of-Thought prompting is a technique that guides AI models to break down 
complex problems into sequential reasoning steps. This approach makes the AI's 
thinking process transparent and often leads to more accurate results.
    """
    )

    # Run demonstrations
    console.print("\n" + "=" * 60)
    demonstrate_math_problem()

    console.print("\n" + "=" * 60)
    demonstrate_logical_reasoning()

    console.print("\n" + "=" * 60)
    demonstrate_complex_analysis()

    console.print("\n" + "=" * 60)

    # Ask if user wants interactive mode
    console.print(
        "\n[bold]Would you like to try solving your own problems? (y/n)[/bold]"
    )
    choice = input().strip().lower()

    if choice in ["y", "yes"]:
        interactive_mode()
    else:
        console.print("🎯 Chain-of-Thought demonstration complete!")


if __name__ == "__main__":
    main()
