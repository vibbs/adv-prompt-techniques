#!/usr/bin/env python3
"""
Meta Prompting Implementation

This module demonstrates meta prompting technique where AI is used to optimize
and generate better prompts, creating a self-improving prompting system.
"""

import os
import sys
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import track

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
)  # if you have not set the env variable


@dataclass
class PromptEvaluation:
    """Represents an evaluation of a prompt's performance."""

    prompt: str
    score: float
    criteria_scores: Dict[str, float]
    feedback: str
    test_case: str
    response: str


class MetaPrompter:
    """
    Meta prompting system that uses AI to optimize and generate prompts.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.prompt_history = []
        self.evaluation_history = []

    def generate_initial_prompts(
        self, task_description: str, num_prompts: int = 3
    ) -> List[str]:
        """Generate multiple initial prompt variations for a task."""

        meta_prompt = f"""
        You are an expert prompt engineer. Generate {num_prompts} different high-quality prompts for this task:
        
        Task: {task_description}
        
        Each prompt should:
        - Be clear and specific
        - Include relevant context and constraints
        - Use effective prompting techniques
        - Be optimized for the intended outcome
        
        Format your response as:
        PROMPT 1:
        [prompt text]
        
        PROMPT 2:
        [prompt text]
        
        PROMPT 3:
        [prompt text]
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master prompt engineer with expertise in crafting effective AI prompts.",
                    },
                    {"role": "user", "content": meta_prompt},
                ],
                temperature=0.8,
                max_tokens=1200,
            )

            content = response.choices[0].message.content

            # Parse the prompts
            prompts = []
            lines = content.split("\n")
            current_prompt = ""
            capturing = False

            for line in lines:
                if line.strip().startswith("PROMPT"):
                    if current_prompt.strip() and capturing:
                        prompts.append(current_prompt.strip())
                    current_prompt = ""
                    capturing = True
                elif capturing and line.strip():
                    current_prompt += line + "\n"

            if current_prompt.strip() and capturing:
                prompts.append(current_prompt.strip())

            self.prompt_history.extend(prompts)
            return prompts

        except Exception as e:
            console.print(f"[red]Error generating prompts: {str(e)}[/red]")
            return []

    def evaluate_prompt(
        self, prompt: str, test_case: str, evaluation_criteria: List[str]
    ) -> PromptEvaluation:
        """Evaluate a prompt's effectiveness on a specific test case."""

        # First, get the response using the prompt
        try:
            test_response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            prompt.format(input=test_case)
                            if "{input}" in prompt
                            else f"{prompt}\n\nInput: {test_case}"
                        ),
                    }
                ],
                temperature=0.3,
                max_tokens=800,
            )

            response_text = test_response.choices[0].message.content

        except Exception as e:
            response_text = f"Error: {str(e)}"

        # Now evaluate the prompt and response
        criteria_text = "\n".join(
            [f"- {criterion}" for criterion in evaluation_criteria]
        )

        evaluation_prompt = f"""
        Evaluate the effectiveness of this prompt and its generated response:
        
        PROMPT:
        {prompt}
        
        TEST INPUT:
        {test_case}
        
        GENERATED RESPONSE:
        {response_text}
        
        Evaluation Criteria:
        {criteria_text}
        
        For each criterion, provide a score from 1-10 and brief explanation.
        Then provide an overall score (1-10) and suggestions for improvement.
        
        Format your response as:
        CRITERION SCORES:
        [criterion name]: [score]/10 - [explanation]
        
        OVERALL SCORE: [score]/10
        
        FEEDBACK:
        [detailed feedback and suggestions for improvement]
        """

        try:
            eval_response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert evaluator of AI prompts and responses. Provide objective, constructive feedback.",
                    },
                    {"role": "user", "content": evaluation_prompt},
                ],
                temperature=0.2,
                max_tokens=600,
            )

            eval_content = eval_response.choices[0].message.content

            # Parse evaluation results
            overall_score = 5.0  # default
            criteria_scores = {}
            feedback = eval_content

            # Extract overall score
            if "OVERALL SCORE:" in eval_content:
                try:
                    score_line = eval_content.split("OVERALL SCORE:")[1].split("\n")[0]
                    overall_score = float(score_line.split("/")[0].strip())
                except:
                    pass

            # Extract criterion scores
            if "CRITERION SCORES:" in eval_content:
                scores_section = eval_content.split("CRITERION SCORES:")[1].split(
                    "OVERALL SCORE:"
                )[0]
                for line in scores_section.split("\n"):
                    if ":" in line and "/10" in line:
                        try:
                            parts = line.split(":")
                            criterion = parts[0].strip()
                            score_part = parts[1].split("/")[0].strip()
                            criteria_scores[criterion] = float(score_part)
                        except:
                            pass

            # Extract feedback
            if "FEEDBACK:" in eval_content:
                feedback = eval_content.split("FEEDBACK:")[1].strip()

            evaluation = PromptEvaluation(
                prompt=prompt,
                score=overall_score,
                criteria_scores=criteria_scores,
                feedback=feedback,
                test_case=test_case,
                response=response_text,
            )

            self.evaluation_history.append(evaluation)
            return evaluation

        except Exception as e:
            console.print(f"[red]Error evaluating prompt: {str(e)}[/red]")
            return PromptEvaluation(
                prompt=prompt,
                score=0.0,
                criteria_scores={},
                feedback=f"Evaluation error: {str(e)}",
                test_case=test_case,
                response=response_text,
            )

    def improve_prompt(self, evaluation: PromptEvaluation) -> str:
        """Generate an improved version of a prompt based on evaluation feedback."""

        improvement_prompt = f"""
        Based on the evaluation feedback below, create an improved version of the prompt.
        
        ORIGINAL PROMPT:
        {evaluation.prompt}
        
        EVALUATION SCORE: {evaluation.score}/10
        
        FEEDBACK:
        {evaluation.feedback}
        
        CRITERION SCORES:
        {chr(10).join([f"{k}: {v}/10" for k, v in evaluation.criteria_scores.items()])}
        
        Create an improved prompt that addresses the feedback and weaknesses identified.
        The improved prompt should:
        - Address specific issues mentioned in the feedback
        - Maintain the original intent and purpose
        - Incorporate best practices for prompt engineering
        - Be more likely to achieve higher scores on the evaluation criteria
        
        IMPROVED PROMPT:
        """

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a prompt engineering expert who specializes in iteratively improving prompts based on feedback.",
                    },
                    {"role": "user", "content": improvement_prompt},
                ],
                temperature=0.6,
                max_tokens=800,
            )

            improved_prompt = response.choices[0].message.content

            # Clean up the response to extract just the prompt
            if "IMPROVED PROMPT:" in improved_prompt:
                improved_prompt = improved_prompt.split("IMPROVED PROMPT:")[1].strip()

            self.prompt_history.append(improved_prompt)
            return improved_prompt

        except Exception as e:
            console.print(f"[red]Error improving prompt: {str(e)}[/red]")
            return evaluation.prompt

    def iterative_optimization(
        self,
        task_description: str,
        test_cases: List[str],
        evaluation_criteria: List[str],
        iterations: int = 3,
    ) -> Dict[str, Any]:
        """Perform iterative prompt optimization using meta prompting."""

        console.print(
            f"[bold blue]🔄 Starting iterative optimization for: {task_description}[/bold blue]"
        )

        # Generate initial prompts
        console.print("📝 Generating initial prompts...")
        initial_prompts = self.generate_initial_prompts(task_description, 3)

        if not initial_prompts:
            return {"error": "Failed to generate initial prompts"}

        best_prompt = initial_prompts[0]
        best_score = 0.0
        optimization_log = []

        for iteration in track(range(iterations), description="Optimizing prompts"):
            console.print(f"\n[cyan]Iteration {iteration + 1}[/cyan]")

            # Evaluate current best prompt on all test cases
            total_score = 0.0
            evaluations = []

            for test_case in test_cases:
                evaluation = self.evaluate_prompt(
                    best_prompt, test_case, evaluation_criteria
                )
                evaluations.append(evaluation)
                total_score += evaluation.score

            avg_score = total_score / len(test_cases) if test_cases else 0.0

            console.print(f"Average score: {avg_score:.2f}/10")

            # Improve the prompt based on evaluations
            if evaluations:
                # Use the evaluation with the lowest score for improvement
                worst_evaluation = min(evaluations, key=lambda x: x.score)
                improved_prompt = self.improve_prompt(worst_evaluation)

                optimization_log.append(
                    {
                        "iteration": iteration + 1,
                        "prompt": best_prompt,
                        "avg_score": avg_score,
                        "evaluations": evaluations,
                        "improved_prompt": improved_prompt,
                    }
                )

                # Update best prompt if improvement found
                if avg_score > best_score:
                    best_score = avg_score

                best_prompt = improved_prompt

        # Final evaluation
        console.print("\n[green]🎯 Final evaluation...[/green]")
        final_evaluations = []
        final_total = 0.0

        for test_case in test_cases:
            final_eval = self.evaluate_prompt(
                best_prompt, test_case, evaluation_criteria
            )
            final_evaluations.append(final_eval)
            final_total += final_eval.score

        final_avg_score = final_total / len(test_cases) if test_cases else 0.0

        return {
            "task_description": task_description,
            "initial_prompts": initial_prompts,
            "final_prompt": best_prompt,
            "final_score": final_avg_score,
            "optimization_log": optimization_log,
            "final_evaluations": final_evaluations,
            "improvement": final_avg_score
            - (optimization_log[0]["avg_score"] if optimization_log else 0),
        }


def demonstrate_prompt_optimization():
    """Demonstrate meta prompting for prompt optimization."""
    console.print(
        Panel("🎯 Prompt Optimization with Meta Prompting", style="bold blue")
    )

    meta_prompter = MetaPrompter()

    task_description = "Generate creative product names for a new line of eco-friendly kitchen appliances"
    test_cases = [
        "A blender made from recycled materials",
        "An energy-efficient coffee maker with solar charging",
        "A compost bin with built-in sensors",
    ]
    evaluation_criteria = [
        "Creativity and uniqueness",
        "Relevance to eco-friendly theme",
        "Market appeal and memorability",
        "Brand consistency",
    ]

    result = meta_prompter.iterative_optimization(
        task_description, test_cases, evaluation_criteria, iterations=2
    )

    # Display results
    console.print("\n[bold yellow]📊 Optimization Results:[/bold yellow]")

    results_table = Table(title="Prompt Evolution")
    results_table.add_column("Iteration", style="cyan")
    results_table.add_column("Score", style="green")
    results_table.add_column("Prompt Preview", style="white")

    # Initial prompt
    if result.get("optimization_log"):
        results_table.add_row(
            "Initial",
            f"{result['optimization_log'][0]['avg_score']:.1f}/10",
            result["initial_prompts"][0][:60] + "...",
        )

        # Show progression
        for log_entry in result["optimization_log"]:
            results_table.add_row(
                f"Iter {log_entry['iteration']}",
                f"{log_entry['avg_score']:.1f}/10",
                log_entry["improved_prompt"][:60] + "...",
            )

    # Final result
    results_table.add_row(
        "Final",
        f"{result['final_score']:.1f}/10",
        result["final_prompt"][:60] + "...",
        style="bold green",
    )

    console.print(results_table)

    console.print(f"\n[bold green]🚀 Final Optimized Prompt:[/bold green]")
    console.print(Panel(result["final_prompt"], title="Best Prompt"))

    console.print(
        f"\n[bold blue]📈 Improvement: +{result['improvement']:.1f} points[/bold blue]"
    )


def demonstrate_prompt_generation():
    """Demonstrate meta prompting for generating specialized prompts."""
    console.print(Panel("⚡ Automated Prompt Generation", style="bold magenta"))

    meta_prompter = MetaPrompter()

    # Generate prompts for different scenarios
    scenarios = [
        "Writing professional email responses to customer complaints",
        "Creating engaging social media captions for a fitness brand",
        "Explaining complex technical concepts to non-technical stakeholders",
    ]

    for scenario in scenarios:
        console.print(f"\n[bold cyan]Scenario:[/bold cyan] {scenario}")

        prompts = meta_prompter.generate_initial_prompts(scenario, num_prompts=2)

        if prompts:
            for i, prompt in enumerate(prompts, 1):
                console.print(f"\n[yellow]Generated Prompt {i}:[/yellow]")
                console.print(
                    Panel(prompt[:300] + "..." if len(prompt) > 300 else prompt)
                )


def demonstrate_prompt_analysis():
    """Demonstrate meta prompting for analyzing existing prompts."""
    console.print(Panel("🔍 Prompt Analysis and Improvement", style="bold green"))

    meta_prompter = MetaPrompter()

    # Example prompts to analyze
    prompts_to_analyze = [
        {
            "name": "Basic Creative Writing",
            "prompt": "Write a story.",
            "test_case": "A story about time travel",
        },
        {
            "name": "Improved Creative Writing",
            "prompt": "Write an engaging 300-word short story with vivid descriptions, compelling characters, and an unexpected twist. Focus on showing rather than telling, and create an emotional connection with the reader.",
            "test_case": "A story about time travel",
        },
    ]

    evaluation_criteria = [
        "Clarity and specificity",
        "Likelihood of generating quality output",
        "Completeness of instructions",
        "Use of prompting best practices",
    ]

    analysis_table = Table(title="Prompt Analysis Comparison")
    analysis_table.add_column("Prompt", style="cyan")
    analysis_table.add_column("Score", style="green")
    analysis_table.add_column("Key Feedback", style="yellow")

    for prompt_info in prompts_to_analyze:
        console.print(f"\n[bold blue]Analyzing: {prompt_info['name']}[/bold blue]")

        evaluation = meta_prompter.evaluate_prompt(
            prompt_info["prompt"], prompt_info["test_case"], evaluation_criteria
        )

        analysis_table.add_row(
            prompt_info["name"],
            f"{evaluation.score:.1f}/10",
            (
                evaluation.feedback[:100] + "..."
                if len(evaluation.feedback) > 100
                else evaluation.feedback
            ),
        )

        # Show detailed analysis
        console.print(f"[green]Score: {evaluation.score}/10[/green]")
        console.print(f"[yellow]Feedback:[/yellow] {evaluation.feedback[:200]}...")

        # Show improvement suggestion
        if evaluation.score < 8.0:
            console.print("[blue]Generating improvement...[/blue]")
            improved = meta_prompter.improve_prompt(evaluation)
            console.print(f"[bold green]Improved version:[/bold green]")
            console.print(
                Panel(improved[:200] + "..." if len(improved) > 200 else improved)
            )

    console.print(f"\n[bold]Analysis Summary:[/bold]")
    console.print(analysis_table)


def interactive_meta_prompting():
    """Interactive mode for meta prompting experimentation."""
    console.print(Panel("🧠 Interactive Meta Prompting Lab", style="bold cyan"))
    console.print("Experiment with meta prompting techniques!")
    console.print("Commands: 'optimize', 'generate', 'analyze', 'quit'\n")

    meta_prompter = MetaPrompter()

    while True:
        try:
            command = (
                input("Choose action (optimize/generate/analyze/quit): ")
                .strip()
                .lower()
            )

            if command in ["quit", "exit", "q"]:
                console.print("👋 Goodbye!")
                break

            elif command in ["optimize", "opt"]:
                task = input(
                    "Describe the task you want to optimize a prompt for: "
                ).strip()
                if not task:
                    continue

                test_case = input("Provide a test case/example input: ").strip()
                if not test_case:
                    continue

                console.print("\n[blue]🔄 Optimizing prompts...[/blue]")

                result = meta_prompter.iterative_optimization(
                    task,
                    [test_case],
                    ["Clarity", "Effectiveness", "Completeness"],
                    iterations=2,
                )

                console.print(f"\n[green]✨ Optimized Prompt:[/green]")
                console.print(Panel(result["final_prompt"]))
                console.print(f"Final Score: {result['final_score']:.1f}/10")

            elif command in ["generate", "gen"]:
                task = input("Describe what you need prompts for: ").strip()
                if not task:
                    continue

                console.print(f"\n[blue]⚡ Generating prompts...[/blue]")
                prompts = meta_prompter.generate_initial_prompts(task, 2)

                for i, prompt in enumerate(prompts, 1):
                    console.print(f"\n[yellow]Option {i}:[/yellow]")
                    console.print(Panel(prompt))

            elif command in ["analyze", "anal"]:
                prompt_text = input("Enter the prompt you want to analyze: ").strip()
                if not prompt_text:
                    continue

                test_input = input("Provide a test input for this prompt: ").strip()
                if not test_input:
                    continue

                console.print(f"\n[blue]🔍 Analyzing prompt...[/blue]")

                evaluation = meta_prompter.evaluate_prompt(
                    prompt_text,
                    test_input,
                    ["Clarity", "Effectiveness", "Completeness"],
                )

                console.print(f"\n[green]Score: {evaluation.score}/10[/green]")
                console.print(f"[yellow]Feedback:[/yellow] {evaluation.feedback}")

                if evaluation.score < 8.0:
                    improve = (
                        input("Generate improved version? (y/n): ").strip().lower()
                    )
                    if improve in ["y", "yes"]:
                        improved = meta_prompter.improve_prompt(evaluation)
                        console.print(f"\n[bold green]Improved Prompt:[/bold green]")
                        console.print(Panel(improved))

            else:
                console.print(
                    "Unknown command. Use: optimize, generate, analyze, or quit"
                )

            console.print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main function to run meta prompting demonstrations."""
    console.print(
        Panel.fit("🧠 Meta Prompting Demonstration", style="bold white on purple")
    )

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set![/red]")
        console.print("Please set your OpenAI API key in the .env file.")
        sys.exit(1)

    console.print("\n[bold]What is Meta Prompting?[/bold]")
    console.print(
        """
Meta prompting uses AI to optimize and generate better prompts. This creates
a self-improving prompting system where AI helps design more effective prompts
for various tasks, leading to better results through automated optimization.
    """
    )

    # Run demonstrations
    console.print("\n" + "=" * 70)
    demonstrate_prompt_optimization()

    console.print("\n" + "=" * 70)
    demonstrate_prompt_generation()

    console.print("\n" + "=" * 70)
    demonstrate_prompt_analysis()

    console.print("\n" + "=" * 70)

    # Ask if user wants interactive mode
    console.print(
        "\n[bold]Would you like to try interactive meta prompting? (y/n)[/bold]"
    )
    choice = input().strip().lower()

    if choice in ["y", "yes"]:
        interactive_meta_prompting()
    else:
        console.print("🧠 Meta prompting demonstration complete!")


if __name__ == "__main__":
    main()
