#!/usr/bin/env python3
"""
Recursive Self-Improvement Prompting (RSIP) Implementation

This module demonstrates RSIP technique which implements recursive self-reflection
and improvement, allowing AI to iteratively refine its own outputs.
"""

import os
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
)  # if you have not set the env variable


@dataclass
class RSIPIteration:
    """Represents one iteration in the RSIP process."""

    iteration: int
    content: str
    self_critique: str
    improvement_plan: str
    quality_score: float
    refined_content: str
    improvements_made: List[str]


class RSIPProcessor:
    """
    Recursive Self-Improvement Prompting processor that enables AI to
    iteratively critique and improve its own outputs.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.iterations = []
        self.improvement_history = []

    def generate_initial_content(self, task: str, requirements: str = "") -> str:
        """Generate initial content for the given task."""

        prompt = f"""
        Task: {task}
        
        {f"Requirements: {requirements}" if requirements else ""}
        
        Please create high-quality content that addresses this task thoroughly.
        Focus on creating something that is well-structured, comprehensive, and valuable.
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a skilled content creator who produces high-quality, thoughtful work.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1200,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating initial content: {str(e)}"

    def self_critique(self, content: str, task: str, iteration: int) -> Dict[str, Any]:
        """Generate self-critique of the current content."""

        critique_prompt = f"""
        You are now acting as a critical reviewer of your own work. Analyze the following content objectively and thoroughly.
        
        ORIGINAL TASK: {task}
        
        CONTENT TO REVIEW (Iteration {iteration}):
        {content}
        
        Please provide a comprehensive critique that includes:
        
        1. STRENGTHS: What aspects of this content are well done?
        2. WEAKNESSES: What specific areas need improvement?
        3. MISSING ELEMENTS: What important aspects are missing or underrepresented?
        4. STRUCTURAL ISSUES: Are there problems with organization or flow?
        5. QUALITY ASSESSMENT: Rate the overall quality (1-10) and explain why.
        6. IMPROVEMENT OPPORTUNITIES: Specific suggestions for enhancement.
        
        Be honest, constructive, and detailed in your analysis.
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a meticulous critic who provides honest, detailed feedback on creative and analytical work.",
                    },
                    {"role": "user", "content": critique_prompt},
                ],
                temperature=0.3,
                max_tokens=800,
            )

            critique_content = response.choices[0].message.content

            # Extract quality score
            quality_score = 5.0  # default
            lines = critique_content.split("\n")
            for line in lines:
                if "quality" in line.lower() and any(char.isdigit() for char in line):
                    try:
                        # Extract number from the line
                        import re

                        numbers = re.findall(r"\b\d+(?:\.\d+)?\b", line)
                        if numbers:
                            score = float(numbers[0])
                            if 1 <= score <= 10:
                                quality_score = score
                                break
                    except:
                        pass

            return {"critique": critique_content, "quality_score": quality_score}

        except Exception as e:
            return {
                "critique": f"Error generating critique: {str(e)}",
                "quality_score": 0.0,
            }

    def generate_improvement_plan(self, content: str, critique: str, task: str) -> str:
        """Generate specific improvement plan based on critique."""

        plan_prompt = f"""
        Based on the self-critique below, create a specific, actionable improvement plan.
        
        ORIGINAL TASK: {task}
        CURRENT CONTENT: {content}
        SELF-CRITIQUE: {critique}
        
        Create a detailed improvement plan that includes:
        
        1. PRIORITY IMPROVEMENTS: List the top 3-5 most important changes needed
        2. SPECIFIC ACTIONS: For each improvement, describe exactly what should be done
        3. ENHANCEMENT STRATEGIES: Techniques to make the content better
        4. STRUCTURAL CHANGES: Any reorganization or reformatting needed
        5. CONTENT ADDITIONS: What new information or sections should be added
        6. QUALITY UPGRADES: How to elevate the overall standard
        
        Be specific and actionable in your recommendations.
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert improvement strategist who creates detailed, actionable plans for content enhancement.",
                    },
                    {"role": "user", "content": plan_prompt},
                ],
                temperature=0.4,
                max_tokens=600,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating improvement plan: {str(e)}"

    def apply_improvements(
        self, content: str, critique: str, improvement_plan: str, task: str
    ) -> str:
        """Apply the improvement plan to create refined content."""

        improvement_prompt = f"""
        Now implement the improvement plan to create a significantly enhanced version of the content.
        
        ORIGINAL TASK: {task}
        CURRENT CONTENT: {content}
        CRITIQUE RECEIVED: {critique}
        IMPROVEMENT PLAN: {improvement_plan}
        
        Create an improved version that:
        - Addresses all the weaknesses identified in the critique
        - Implements the specific improvements outlined in the plan
        - Maintains the strengths of the original while fixing the problems
        - Results in higher quality, more comprehensive content
        - Is better organized and more engaging
        
        Produce the complete, improved version:
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a skilled editor and content improver who implements feedback to create superior versions of content.",
                    },
                    {"role": "user", "content": improvement_prompt},
                ],
                temperature=0.6,
                max_tokens=1500,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error applying improvements: {str(e)}"

    def extract_improvements_made(self, original: str, improved: str) -> List[str]:
        """Identify what specific improvements were made."""

        analysis_prompt = f"""
        Compare the original and improved versions of content and identify the specific improvements that were made.
        
        ORIGINAL VERSION:
        {original[:500]}...
        
        IMPROVED VERSION:
        {improved[:500]}...
        
        List the specific improvements that were made, such as:
        - Added sections or information
        - Improved structure or organization
        - Enhanced clarity or readability
        - Better examples or explanations
        - Fixed issues or weaknesses
        
        Format as a simple bullet list of improvements.
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an analytical reviewer who identifies specific changes and improvements between versions of content.",
                    },
                    {"role": "user", "content": analysis_prompt},
                ],
                temperature=0.3,
                max_tokens=400,
            )

            improvements_text = response.choices[0].message.content

            # Extract bullet points
            improvements = []
            lines = improvements_text.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith(("-", "•", "*")) or line.startswith(
                    tuple(f"{i}." for i in range(1, 10))
                ):
                    # Clean up the bullet point
                    cleaned = line.lstrip("-•*0123456789. ").strip()
                    if cleaned:
                        improvements.append(cleaned)

            return improvements[:5]  # Return top 5 improvements

        except Exception as e:
            return [f"Error analyzing improvements: {str(e)}"]

    def rsip_process(
        self,
        task: str,
        requirements: str = "",
        max_iterations: int = 3,
        quality_threshold: float = 8.0,
    ) -> Dict[str, Any]:
        """
        Execute the complete RSIP process.

        Args:
            task: The task to work on
            requirements: Additional requirements or constraints
            max_iterations: Maximum number of improvement iterations
            quality_threshold: Stop when quality reaches this score

        Returns:
            Complete RSIP results with all iterations
        """

        console.print(f"[bold blue]🔄 Starting RSIP process for: {task}[/bold blue]")

        # Generate initial content
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:

            init_task = progress.add_task("Generating initial content...", total=1)
            current_content = self.generate_initial_content(task, requirements)
            progress.advance(init_task, 1)

            iteration_count = 0

            while iteration_count < max_iterations:
                iteration_count += 1

                # Self-critique
                critique_task = progress.add_task(
                    f"Iteration {iteration_count}: Self-critiquing...", total=1
                )
                critique_result = self.self_critique(
                    current_content, task, iteration_count
                )
                progress.advance(critique_task, 1)

                critique = critique_result["critique"]
                quality_score = critique_result["quality_score"]

                console.print(f"[yellow]Quality Score: {quality_score}/10[/yellow]")

                # Check if quality threshold reached
                if quality_score >= quality_threshold:
                    console.print(
                        f"[green]Quality threshold ({quality_threshold}) reached! Stopping early.[/green]"
                    )
                    break

                # Generate improvement plan
                plan_task = progress.add_task(
                    f"Iteration {iteration_count}: Planning improvements...", total=1
                )
                improvement_plan = self.generate_improvement_plan(
                    current_content, critique, task
                )
                progress.advance(plan_task, 1)

                # Apply improvements
                improve_task = progress.add_task(
                    f"Iteration {iteration_count}: Applying improvements...", total=1
                )
                original_content = current_content
                current_content = self.apply_improvements(
                    current_content, critique, improvement_plan, task
                )
                progress.advance(improve_task, 1)

                # Analyze improvements made
                improvements_made = self.extract_improvements_made(
                    original_content, current_content
                )

                # Store iteration
                iteration_obj = RSIPIteration(
                    iteration=iteration_count,
                    content=original_content,
                    self_critique=critique,
                    improvement_plan=improvement_plan,
                    quality_score=quality_score,
                    refined_content=current_content,
                    improvements_made=improvements_made,
                )

                self.iterations.append(iteration_obj)

        # Final quality check
        final_critique = self.self_critique(current_content, task, iteration_count + 1)
        final_quality = final_critique["quality_score"]

        return {
            "task": task,
            "initial_content": self.iterations[0].content if self.iterations else "",
            "final_content": current_content,
            "iterations": self.iterations,
            "final_quality_score": final_quality,
            "total_iterations": iteration_count,
            "quality_improvement": final_quality
            - (self.iterations[0].quality_score if self.iterations else 0),
            "convergence_achieved": final_quality >= quality_threshold,
        }


def demonstrate_creative_writing():
    """Demonstrate RSIP for creative writing improvement."""
    console.print(Panel("📝 Creative Writing Enhancement with RSIP", style="bold blue"))

    processor = RSIPProcessor()

    task = "Write a compelling short story about a time traveler who accidentally changes a small detail in the past and discovers how it creates unexpected ripple effects in the present."
    requirements = "The story should be engaging, have well-developed characters, include dialogue, and be approximately 300-400 words long."

    result = processor.rsip_process(
        task, requirements, max_iterations=3, quality_threshold=8.5
    )

    # Display iteration progress
    console.print("\n[bold yellow]📈 RSIP Improvement Journey:[/bold yellow]")

    progress_table = Table(title="Quality Improvement Over Iterations")
    progress_table.add_column("Iteration", style="cyan")
    progress_table.add_column("Quality Score", style="green")
    progress_table.add_column("Key Improvements", style="yellow")

    for iteration in result["iterations"]:
        improvements_preview = ", ".join(iteration.improvements_made[:2])
        if len(iteration.improvements_made) > 2:
            improvements_preview += f" (+{len(iteration.improvements_made)-2} more)"

        progress_table.add_row(
            str(iteration.iteration),
            f"{iteration.quality_score:.1f}/10",
            (
                improvements_preview[:50] + "..."
                if len(improvements_preview) > 50
                else improvements_preview
            ),
        )

    # Add final score
    progress_table.add_row(
        "Final",
        f"{result['final_quality_score']:.1f}/10",
        "Complete",
        style="bold green",
    )

    console.print(progress_table)

    console.print(f"\n[bold green]📊 Improvement Summary:[/bold green]")
    console.print(f"Quality improvement: +{result['quality_improvement']:.1f} points")
    console.print(f"Total iterations: {result['total_iterations']}")
    console.print(
        f"Convergence achieved: {'Yes' if result['convergence_achieved'] else 'No'}"
    )

    console.print(f"\n[bold green]✨ Final Story:[/bold green]")
    console.print(Panel(result["final_content"], title="RSIP Enhanced Story"))


def demonstrate_business_proposal():
    """Demonstrate RSIP for business document improvement."""
    console.print(
        Panel("💼 Business Proposal Enhancement with RSIP", style="bold magenta")
    )

    processor = RSIPProcessor()

    task = "Create a compelling business proposal for a mobile app that helps people reduce food waste by connecting them with local restaurants and grocery stores offering discounted surplus food."
    requirements = "Include market opportunity, solution description, revenue model, competitive analysis, and implementation timeline. Make it persuasive for potential investors."

    result = processor.rsip_process(
        task, requirements, max_iterations=2, quality_threshold=8.0
    )

    console.print("\n[bold yellow]🔄 Self-Improvement Process:[/bold yellow]")

    for i, iteration in enumerate(result["iterations"]):
        console.print(f"\n[cyan]Iteration {iteration.iteration}:[/cyan]")
        console.print(f"[green]Quality Score: {iteration.quality_score}/10[/green]")

        # Show critique summary
        critique_lines = iteration.self_critique.split("\n")[:3]
        critique_preview = " ".join(critique_lines)[:200] + "..."
        console.print(f"[yellow]Self-Critique:[/yellow] {critique_preview}")

        # Show improvements made
        if iteration.improvements_made:
            console.print("[blue]Improvements Made:[/blue]")
            for improvement in iteration.improvements_made[:3]:
                console.print(f"  • {improvement}")

    console.print(f"\n[bold green]📋 Final Business Proposal:[/bold green]")
    console.print(
        Panel(
            result["final_content"][:500] + "...",
            title=f"Enhanced Proposal (Score: {result['final_quality_score']}/10)",
        )
    )


def demonstrate_technical_explanation():
    """Demonstrate RSIP for technical content improvement."""
    console.print(
        Panel("🔬 Technical Explanation Enhancement with RSIP", style="bold green")
    )

    processor = RSIPProcessor()

    task = "Explain how blockchain technology works to someone with no technical background, covering key concepts like decentralization, consensus mechanisms, and cryptographic hashing."
    requirements = "Use simple language, practical analogies, avoid jargon, and include real-world examples. Should be comprehensive yet accessible."

    result = processor.rsip_process(
        task, requirements, max_iterations=3, quality_threshold=8.5
    )

    console.print("\n[bold yellow]🧠 Iterative Refinement Process:[/bold yellow]")

    refinement_data = []

    for iteration in result["iterations"]:
        refinement_data.append(
            {
                "iteration": iteration.iteration,
                "score": iteration.quality_score,
                "improvements": len(iteration.improvements_made),
                "content_length": len(iteration.refined_content),
            }
        )

    # Show progression chart
    console.print("[cyan]Quality Score Progression:[/cyan]")
    for data in refinement_data:
        bar_length = int(data["score"])
        bar = "█" * bar_length + "░" * (10 - bar_length)
        console.print(
            f"Iteration {data['iteration']}: {bar} {data['score']:.1f}/10 ({data['improvements']} improvements)"
        )

    # Show final explanation
    console.print(f"\n[bold green]🎓 Final Technical Explanation:[/bold green]")
    final_preview = (
        result["final_content"][:400] + "..."
        if len(result["final_content"]) > 400
        else result["final_content"]
    )
    console.print(
        Panel(
            final_preview,
            title=f"Refined Explanation (Quality: {result['final_quality_score']:.1f}/10)",
        )
    )


def interactive_rsip_mode():
    """Interactive mode for RSIP experimentation."""
    console.print(Panel("🔄 Interactive RSIP Laboratory", style="bold cyan"))
    console.print("Experience recursive self-improvement in action!")
    console.print("The AI will critique and improve its own work iteratively.\n")

    processor = RSIPProcessor()

    while True:
        try:
            console.print("[bold]Configuration:[/bold]")

            task = input("Describe your task: ").strip()
            if not task:
                console.print("Task is required.")
                continue

            if task.lower() in ["quit", "exit", "q"]:
                console.print("👋 Goodbye!")
                break

            requirements = input("Additional requirements (optional): ").strip()

            try:
                max_iter = int(input("Maximum iterations (1-5, default 3): ") or "3")
                max_iter = max(1, min(5, max_iter))
            except ValueError:
                max_iter = 3

            try:
                threshold = float(
                    input("Quality threshold to stop early (1-10, default 8.0): ")
                    or "8.0"
                )
                threshold = max(1.0, min(10.0, threshold))
            except ValueError:
                threshold = 8.0

            console.print(f"\n[blue]🚀 Starting RSIP process...[/blue]")
            console.print(f"Task: {task}")
            console.print(f"Max iterations: {max_iter}")
            console.print(f"Quality threshold: {threshold}")

            # Run RSIP process
            result = processor.rsip_process(task, requirements, max_iter, threshold)

            # Show detailed results
            console.print(f"\n[bold yellow]📊 RSIP Results:[/bold yellow]")
            console.print(f"Total iterations: {result['total_iterations']}")
            console.print(
                f"Quality improvement: +{result['quality_improvement']:.1f} points"
            )
            console.print(f"Final score: {result['final_quality_score']:.1f}/10")
            console.print(
                f"Threshold reached: {'Yes' if result['convergence_achieved'] else 'No'}"
            )

            # Show iteration details
            if result["iterations"]:
                console.print(f"\n[cyan]Improvement Journey:[/cyan]")
                for iteration in result["iterations"]:
                    console.print(
                        f"\nIteration {iteration.iteration}: {iteration.quality_score:.1f}/10"
                    )
                    if iteration.improvements_made:
                        console.print("Key improvements:")
                        for imp in iteration.improvements_made[:2]:
                            console.print(f"  • {imp}")

            # Show final content
            console.print(f"\n[bold green]🎯 Final Result:[/bold green]")
            console.print(Panel(result["final_content"], title="RSIP Enhanced Content"))

            console.print("\n" + "=" * 60 + "\n")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main function to run RSIP demonstrations."""
    console.print(
        Panel.fit(
            "🔄 Recursive Self-Improvement Prompting (RSIP) Demonstration",
            style="bold white on purple",
        )
    )

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set![/red]")
        console.print("Please set your OpenAI API key in the .env file.")
        sys.exit(1)

    console.print("\n[bold]What is Recursive Self-Improvement Prompting (RSIP)?[/bold]")
    console.print(
        """
RSIP enables AI to iteratively critique and improve its own outputs through
recursive self-reflection. The AI generates content, critiques it objectively,
plans improvements, and applies them in cycles until quality thresholds are met.
    """
    )

    # Run demonstrations
    console.print("\n" + "=" * 70)
    demonstrate_creative_writing()

    console.print("\n" + "=" * 70)
    demonstrate_business_proposal()

    console.print("\n" + "=" * 70)
    demonstrate_technical_explanation()

    console.print("\n" + "=" * 70)

    # Ask if user wants interactive mode
    console.print("\n[bold]Would you like to try interactive RSIP? (y/n)[/bold]")
    choice = input().strip().lower()

    if choice in ["y", "yes"]:
        interactive_rsip_mode()
    else:
        console.print("🔄 RSIP demonstration complete!")


if __name__ == "__main__":
    main()
