#!/usr/bin/env python3
"""
Prompt Chaining Implementation

This module demonstrates prompt chaining technique which connects multiple
prompts in sequence, where each prompt builds upon the output of the previous one.
"""

import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
)  # if you have not set the env variable


@dataclass
class ChainStep:
    """Represents a single step in a prompt chain."""

    name: str
    prompt_template: str
    system_message: str = "You are a helpful assistant."
    temperature: float = 0.7
    max_tokens: int = 800
    input_variables: List[str] = None
    output_key: str = "output"


class PromptChain:
    """
    Implementation of Prompt Chaining for multi-step AI workflows.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.steps = []
        self.execution_history = []
        self.variables = {}

    def add_step(self, step: ChainStep) -> "PromptChain":
        """Add a step to the chain."""
        self.steps.append(step)
        return self

    def set_variable(self, key: str, value: str) -> "PromptChain":
        """Set a variable for use in the chain."""
        self.variables[key] = value
        return self

    def format_prompt(self, template: str, variables: Dict[str, str]) -> str:
        """Format a prompt template with variables."""
        try:
            return template.format(**variables)
        except KeyError as e:
            missing_var = str(e).strip("'")
            raise ValueError(f"Missing variable '{missing_var}' for prompt template")

    def execute_step(self, step: ChainStep, step_variables: Dict[str, str]) -> str:
        """Execute a single step in the chain."""
        try:
            # Format the prompt with available variables
            formatted_prompt = self.format_prompt(step.prompt_template, step_variables)

            # Make API call
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": step.system_message},
                    {"role": "user", "content": formatted_prompt},
                ],
                temperature=step.temperature,
                max_tokens=step.max_tokens,
            )

            result = response.choices[0].message.content

            # Store execution details
            self.execution_history.append(
                {
                    "step_name": step.name,
                    "formatted_prompt": formatted_prompt,
                    "result": result,
                    "variables_used": step_variables.copy(),
                }
            )

            return result

        except Exception as e:
            error_msg = f"Error executing step '{step.name}': {str(e)}"
            self.execution_history.append(
                {
                    "step_name": step.name,
                    "error": error_msg,
                    "variables_used": step_variables.copy(),
                }
            )
            raise RuntimeError(error_msg)

    def execute(self, initial_input: str = "") -> Dict[str, Any]:
        """Execute the entire prompt chain."""
        if not self.steps:
            raise ValueError("No steps defined in the chain")

        # Initialize with any provided input
        if initial_input:
            self.variables["input"] = initial_input

        current_variables = self.variables.copy()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            for i, step in enumerate(self.steps):
                task = progress.add_task(f"Executing step: {step.name}", total=1)

                try:
                    result = self.execute_step(step, current_variables)

                    # Store the result for next steps
                    current_variables[step.output_key] = result
                    current_variables[f"step_{i+1}_output"] = result

                    progress.advance(task)

                except Exception as e:
                    progress.stop()
                    raise e

        return {
            "final_output": current_variables.get(self.steps[-1].output_key, ""),
            "all_outputs": current_variables,
            "execution_history": self.execution_history,
        }


def create_blog_post_chain() -> PromptChain:
    """Create a chain for generating a complete blog post."""
    chain = PromptChain()

    # Step 1: Generate blog outline
    chain.add_step(
        ChainStep(
            name="Outline Generation",
            prompt_template="""
        Create a detailed outline for a blog post about: {topic}
        
        Target audience: {audience}
        
        The outline should include:
        - Compelling title
        - Introduction hook
        - 3-5 main sections with subsections
        - Conclusion
        - Estimated reading time
        
        Format as a structured outline.
        """,
            system_message="You are an expert content strategist who creates engaging blog post outlines.",
            temperature=0.8,
            output_key="outline",
        )
    )

    # Step 2: Write introduction
    chain.add_step(
        ChainStep(
            name="Introduction Writing",
            prompt_template="""
        Based on this blog post outline:
        {outline}
        
        Write an engaging introduction that:
        - Hooks the reader immediately
        - Clearly states what they'll learn
        - Sets the tone for the post
        - Is 2-3 paragraphs long
        
        Make it conversational and valuable.
        """,
            system_message="You are a skilled blog writer who creates compelling introductions.",
            temperature=0.7,
            output_key="introduction",
        )
    )

    # Step 3: Write main content
    chain.add_step(
        ChainStep(
            name="Main Content Creation",
            prompt_template="""
        Using this outline:
        {outline}
        
        And this introduction:
        {introduction}
        
        Write the main body content for the blog post. Include:
        - Detailed explanations for each main section
        - Practical examples and tips
        - Smooth transitions between sections
        - Subheadings for better readability
        
        Keep the tone consistent with the introduction.
        """,
            system_message="You are an expert content writer who creates informative and engaging blog content.",
            temperature=0.6,
            max_tokens=1500,
            output_key="main_content",
        )
    )

    # Step 4: Write conclusion and CTA
    chain.add_step(
        ChainStep(
            name="Conclusion and CTA",
            prompt_template="""
        For this blog post with:
        
        Outline: {outline}
        Introduction: {introduction}
        Main Content: {main_content}
        
        Write a strong conclusion that:
        - Summarizes key points
        - Reinforces the main value
        - Includes a clear call-to-action
        - Encourages engagement
        
        End with 2-3 relevant questions for readers to consider.
        """,
            system_message="You are a marketing-savvy writer who creates compelling conclusions and calls-to-action.",
            temperature=0.7,
            output_key="conclusion",
        )
    )

    # Step 5: Final assembly and polish
    chain.add_step(
        ChainStep(
            name="Final Assembly",
            prompt_template="""
        Combine these components into a final blog post:
        
        OUTLINE: {outline}
        INTRODUCTION: {introduction}
        MAIN CONTENT: {main_content}
        CONCLUSION: {conclusion}
        
        Assemble them into a cohesive, well-formatted blog post. Add:
        - A catchy title based on the outline
        - Smooth transitions where needed
        - Final polish and consistency check
        - Proper formatting with headers
        
        Output the complete, publication-ready blog post.
        """,
            system_message="You are an editor who assembles and polishes content into final form.",
            temperature=0.3,
            output_key="final_blog_post",
        )
    )

    return chain


def create_product_analysis_chain() -> PromptChain:
    """Create a chain for comprehensive product analysis."""
    chain = PromptChain()

    # Step 1: Market research
    chain.add_step(
        ChainStep(
            name="Market Research",
            prompt_template="""
        Conduct market research analysis for: {product_name}
        
        Product description: {product_description}
        
        Analyze:
        - Target market size and characteristics
        - Key competitors and their positioning
        - Market trends and opportunities
        - Potential customer segments
        
        Provide detailed insights for each area.
        """,
            system_message="You are a market research analyst with expertise in product analysis.",
            temperature=0.5,
            output_key="market_research",
        )
    )

    # Step 2: SWOT analysis
    chain.add_step(
        ChainStep(
            name="SWOT Analysis",
            prompt_template="""
        Based on this market research:
        {market_research}
        
        For the product: {product_name}
        Description: {product_description}
        
        Create a comprehensive SWOT analysis:
        - Strengths: Internal positive factors
        - Weaknesses: Internal negative factors  
        - Opportunities: External positive factors
        - Threats: External negative factors
        
        Provide specific, actionable insights for each category.
        """,
            system_message="You are a strategic business analyst specializing in SWOT analysis.",
            temperature=0.4,
            output_key="swot_analysis",
        )
    )

    # Step 3: Pricing strategy
    chain.add_step(
        ChainStep(
            name="Pricing Strategy",
            prompt_template="""
        Using the market research and SWOT analysis:
        
        MARKET RESEARCH: {market_research}
        SWOT ANALYSIS: {swot_analysis}
        
        For product: {product_name}
        
        Develop a pricing strategy that includes:
        - Recommended pricing model (subscription, one-time, freemium, etc.)
        - Price point recommendations with justification
        - Competitive pricing analysis
        - Value proposition alignment
        - Pricing for different customer segments
        
        Provide specific recommendations with rationale.
        """,
            system_message="You are a pricing strategist with expertise in product monetization.",
            temperature=0.5,
            output_key="pricing_strategy",
        )
    )

    # Step 4: Go-to-market recommendations
    chain.add_step(
        ChainStep(
            name="Go-to-Market Strategy",
            prompt_template="""
        Synthesize all previous analysis:
        
        MARKET RESEARCH: {market_research}
        SWOT ANALYSIS: {swot_analysis}  
        PRICING STRATEGY: {pricing_strategy}
        
        Create a go-to-market strategy for: {product_name}
        
        Include:
        - Launch timeline and phases
        - Marketing channels and tactics
        - Sales strategy and process
        - Key success metrics
        - Risk mitigation plans
        - Resource requirements
        
        Provide an actionable roadmap.
        """,
            system_message="You are a go-to-market strategist who creates comprehensive launch plans.",
            temperature=0.6,
            output_key="gtm_strategy",
        )
    )

    return chain


def create_learning_path_chain() -> PromptChain:
    """Create a chain for generating personalized learning paths."""
    chain = PromptChain()

    # Step 1: Skill assessment
    chain.add_step(
        ChainStep(
            name="Skill Assessment",
            prompt_template="""
        Create a skill assessment for someone wanting to learn: {subject}
        
        Current level: {current_level}
        Goal: {learning_goal}
        Available time: {time_commitment}
        
        Analyze:
        - Prerequisites and foundational knowledge needed
        - Skill gaps to address
        - Learning style preferences
        - Realistic timeline expectations
        
        Provide a comprehensive assessment.
        """,
            system_message="You are an educational consultant who assesses learning needs.",
            temperature=0.5,
            output_key="skill_assessment",
        )
    )

    # Step 2: Curriculum design
    chain.add_step(
        ChainStep(
            name="Curriculum Design",
            prompt_template="""
        Based on this skill assessment:
        {skill_assessment}
        
        For learning: {subject}
        Timeline: {time_commitment}
        
        Design a structured curriculum with:
        - Learning modules in logical sequence
        - Key concepts and skills for each module
        - Estimated time for each module
        - Prerequisites between modules
        - Practical projects and exercises
        
        Create a comprehensive learning roadmap.
        """,
            system_message="You are a curriculum designer who creates effective learning sequences.",
            temperature=0.6,
            output_key="curriculum",
        )
    )

    # Step 3: Resource recommendations
    chain.add_step(
        ChainStep(
            name="Resource Recommendations",
            prompt_template="""
        For this curriculum:
        {curriculum}
        
        Subject: {subject}
        Skill assessment: {skill_assessment}
        
        Recommend specific learning resources:
        - Books and textbooks
        - Online courses and platforms
        - Practice websites and tools
        - Communities and forums
        - Projects and exercises
        - Assessment methods
        
        Organize by learning module and priority.
        """,
            system_message="You are an educational resource specialist with deep knowledge of learning materials.",
            temperature=0.7,
            output_key="resources",
        )
    )

    # Step 4: Study plan
    chain.add_step(
        ChainStep(
            name="Study Plan Creation",
            prompt_template="""
        Create a detailed study plan using:
        
        CURRICULUM: {curriculum}
        RESOURCES: {resources}
        TIME COMMITMENT: {time_commitment}
        
        Include:
        - Weekly study schedule
        - Daily learning activities
        - Milestone checkpoints
        - Progress tracking methods
        - Motivation and accountability tips
        - Adjustment strategies
        
        Make it actionable and realistic.
        """,
            system_message="You are a study skills coach who creates effective learning plans.",
            temperature=0.5,
            output_key="study_plan",
        )
    )

    return chain


def demonstrate_blog_post_creation():
    """Demonstrate prompt chaining for blog post creation."""
    console.print(
        Panel("📝 Blog Post Creation with Prompt Chaining", style="bold blue")
    )

    chain = create_blog_post_chain()
    chain.set_variable("topic", "Advanced Prompting Techniques for Developers")
    chain.set_variable("audience", "Software developers and AI enthusiasts")

    console.print(
        "[bold]Creating a complete blog post through chained prompts...[/bold]"
    )

    result = chain.execute()

    console.print("\n[bold yellow]🔗 Chain Execution Steps:[/bold yellow]")
    for i, step in enumerate(chain.execution_history):
        console.print(f"\n[cyan]{i+1}. {step['step_name']}[/cyan]")
        console.print(f"Variables used: {list(step.get('variables_used', {}).keys())}")
        if "error" in step:
            console.print(f"[red]Error: {step['error']}[/red]")
        else:
            preview = (
                step["result"][:100] + "..."
                if len(step["result"]) > 100
                else step["result"]
            )
            console.print(f"Output preview: {preview}")

    console.print("\n[bold green]📄 Final Blog Post:[/bold green]")
    console.print(Markdown(result["final_output"]))


def demonstrate_product_analysis():
    """Demonstrate prompt chaining for product analysis."""
    console.print(
        Panel("📊 Product Analysis with Prompt Chaining", style="bold magenta")
    )

    chain = create_product_analysis_chain()
    chain.set_variable("product_name", "AI-Powered Code Review Assistant")
    chain.set_variable(
        "product_description",
        "A VS Code extension that uses AI to automatically review code, suggest improvements, and catch potential bugs before deployment.",
    )

    console.print("[bold]Conducting comprehensive product analysis...[/bold]")

    result = chain.execute()

    console.print("\n[bold yellow]📈 Analysis Pipeline:[/bold yellow]")
    steps = [
        "Market Research",
        "SWOT Analysis",
        "Pricing Strategy",
        "Go-to-Market Strategy",
    ]

    for i, step_name in enumerate(steps):
        step_data = next(
            (s for s in chain.execution_history if s["step_name"] == step_name), None
        )
        if step_data:
            console.print(f"\n[cyan]{i+1}. {step_name} ✓[/cyan]")
            preview = (
                step_data["result"][:150] + "..."
                if len(step_data["result"]) > 150
                else step_data["result"]
            )
            console.print(f"Key insights: {preview}")

    console.print("\n[bold green]🎯 Final Strategy Recommendation:[/bold green]")
    console.print(Markdown(result["final_output"]))


def demonstrate_learning_path():
    """Demonstrate prompt chaining for learning path creation."""
    console.print(
        Panel("🎓 Learning Path Creation with Prompt Chaining", style="bold green")
    )

    chain = create_learning_path_chain()
    chain.set_variable("subject", "Machine Learning and AI")
    chain.set_variable("current_level", "Beginner with some Python knowledge")
    chain.set_variable("learning_goal", "Build and deploy ML models professionally")
    chain.set_variable("time_commitment", "10 hours per week for 6 months")

    console.print("[bold]Creating personalized learning path...[/bold]")

    result = chain.execute()

    console.print("\n[bold yellow]🧠 Learning Design Process:[/bold yellow]")
    for i, step in enumerate(chain.execution_history):
        console.print(f"\n[cyan]{i+1}. {step['step_name']}[/cyan]")
        if "error" not in step:
            # Extract key points from each step
            output = step["result"]
            if len(output) > 200:
                lines = output.split("\n")[:3]
                preview = "\n".join(lines) + "..."
            else:
                preview = output
            console.print(preview)

    console.print("\n[bold green]📚 Complete Learning Plan:[/bold green]")
    console.print(Markdown(result["final_output"]))


def interactive_chain_builder():
    """Interactive mode for building custom prompt chains."""
    console.print(Panel("🔗 Interactive Prompt Chain Builder", style="bold cyan"))
    console.print("Build your own custom prompt chain!")
    console.print("Type 'quit' to exit.\n")

    chain = PromptChain()
    step_count = 0

    while True:
        try:
            console.print(f"\n[bold]Step {step_count + 1} Configuration:[/bold]")

            name = input("Step name (or 'done' to finish, 'quit' to exit): ").strip()

            if name.lower() in ["quit", "exit", "q"]:
                console.print("👋 Goodbye!")
                return

            if name.lower() in ["done", "finish"] and step_count > 0:
                break

            if not name:
                console.print("Please enter a step name.")
                continue

            prompt_template = input(
                "Prompt template (use {variable_name} for variables): "
            ).strip()
            if not prompt_template:
                console.print("Please enter a prompt template.")
                continue

            system_message = input(
                "System message (optional, press Enter for default): "
            ).strip()
            if not system_message:
                system_message = "You are a helpful assistant."

            step = ChainStep(
                name=name,
                prompt_template=prompt_template,
                system_message=system_message,
                output_key=f"step_{step_count + 1}_output",
            )

            chain.add_step(step)
            step_count += 1

            console.print(f"[green]✓ Added step: {name}[/green]")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            return

    if step_count == 0:
        console.print("No steps defined. Exiting.")
        return

    # Get variables
    console.print(f"\n[bold]Variable Setup:[/bold]")
    variables_needed = set()

    # Extract variables from all prompt templates
    for step in chain.steps:
        import re

        vars_in_template = re.findall(r"\{([^}]+)\}", step.prompt_template)
        variables_needed.update(vars_in_template)

    console.print(f"Variables needed: {list(variables_needed)}")

    for var in variables_needed:
        value = input(f"Value for '{var}': ").strip()
        if value:
            chain.set_variable(var, value)

    # Execute the chain
    console.print(f"\n[bold blue]🚀 Executing your custom chain...[/bold blue]")

    try:
        result = chain.execute()

        console.print(f"\n[bold yellow]⛓️ Execution Results:[/bold yellow]")
        for i, step in enumerate(chain.execution_history):
            console.print(f"\n{i+1}. {step['step_name']}")
            console.print(
                step["result"][:200] + "..."
                if len(step["result"]) > 200
                else step["result"]
            )

        console.print(f"\n[bold green]🎯 Final Output:[/bold green]")
        console.print(Markdown(result["final_output"]))

    except Exception as e:
        console.print(f"[red]Error executing chain: {str(e)}[/red]")


def main():
    """Main function to run prompt chaining demonstrations."""
    console.print(
        Panel.fit("🔗 Prompt Chaining Demonstration", style="bold white on blue")
    )

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set![/red]")
        console.print("Please set your OpenAI API key in the .env file.")
        sys.exit(1)

    console.print("\n[bold]What is Prompt Chaining?[/bold]")
    console.print(
        """
Prompt chaining connects multiple prompts in sequence, where each prompt builds
upon the output of previous prompts. This enables complex, multi-step workflows
that break down large tasks into manageable, sequential operations.
    """
    )

    # Run demonstrations
    console.print("\n" + "=" * 70)
    demonstrate_blog_post_creation()

    console.print("\n" + "=" * 70)
    demonstrate_product_analysis()

    console.print("\n" + "=" * 70)
    demonstrate_learning_path()

    console.print("\n" + "=" * 70)

    # Ask if user wants interactive mode
    console.print("\n[bold]Would you like to build your own prompt chain? (y/n)[/bold]")
    choice = input().strip().lower()

    if choice in ["y", "yes"]:
        interactive_chain_builder()
    else:
        console.print("🔗 Prompt chaining demonstration complete!")


if __name__ == "__main__":
    main()
