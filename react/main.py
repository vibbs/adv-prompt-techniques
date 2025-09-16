#!/usr/bin/env python3
"""
ReAct (Reason + Act) Prompting Implementation

This module demonstrates ReAct prompting technique which combines reasoning
with action-taking capabilities for interactive problem solving.
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

# Load environment variables
load_dotenv()

# Initialize clients
console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
)  # if you have not set the env variable


class ReActAgent:
    """
    ReAct Agent that combines reasoning with actions.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.action_history = []
        self.thought_history = []
        self.available_tools = {
            "calculator": self.calculator,
            "search_memory": self.search_memory,
            "save_to_memory": self.save_to_memory,
            "get_current_time": self.get_current_time,
            "word_count": self.word_count,
            "summarize_text": self.summarize_text,
        }
        self.memory = {}

    def calculator(self, expression: str) -> str:
        """Simple calculator tool."""
        try:
            # Basic safety check - only allow numbers, operators, and parentheses
            if re.match(r"^[0-9+\-*/.() ]+$", expression):
                result = eval(expression)
                return f"Result: {result}"
            else:
                return "Error: Invalid expression. Only numbers and basic operators allowed."
        except Exception as e:
            return f"Error: {str(e)}"

    def search_memory(self, query: str) -> str:
        """Search stored information."""
        matches = []
        query_lower = query.lower()

        for key, value in self.memory.items():
            if query_lower in key.lower() or query_lower in str(value).lower():
                matches.append(f"{key}: {value}")

        if matches:
            return f"Found {len(matches)} matches:\n" + "\n".join(matches)
        else:
            return "No matches found in memory."

    def save_to_memory(self, key: str, value: str) -> str:
        """Save information to memory."""
        self.memory[key] = value
        return f"Saved '{key}' to memory."

    def get_current_time(self) -> str:
        """Get current date and time."""
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def word_count(self, text: str) -> str:
        """Count words in text."""
        words = len(text.split())
        characters = len(text)
        return f"Word count: {words}, Character count: {characters}"

    def summarize_text(self, text: str) -> str:
        """Summarize provided text using AI."""
        if len(text) > 1000:
            text = text[:1000] + "..."

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize the following text concisely.",
                    },
                    {"role": "user", "content": text},
                ],
                max_tokens=150,
            )
            return f"Summary: {response.choices[0].message.content}"
        except Exception as e:
            return f"Error summarizing: {str(e)}"

    def get_react_prompt(self, problem: str) -> str:
        """Create a ReAct prompt template."""
        tools_description = "\n".join(
            [f"- {name}: {func.__doc__}" for name, func in self.available_tools.items()]
        )

        return f"""
You are a helpful assistant that can think step by step and use tools to solve problems.
You have access to the following tools:

{tools_description}

To use a tool, format your response as:
Action: tool_name
Action Input: input_for_tool

You can think about the problem by starting with "Thought:" and then take actions.
After using a tool, you'll receive an "Observation:" with the result.

Problem: {problem}

Let me solve this step by step:
"""

    def parse_action(self, text: str) -> Optional[Dict[str, str]]:
        """Parse action from AI response."""
        action_pattern = r"Action:\s*([^\n]+)\nAction Input:\s*([^\n]+)"
        match = re.search(action_pattern, text, re.IGNORECASE)

        if match:
            return {"action": match.group(1).strip(), "input": match.group(2).strip()}
        return None

    def execute_action(self, action: str, action_input: str) -> str:
        """Execute a tool action."""
        if action in self.available_tools:
            try:
                result = self.available_tools[action](action_input)
                self.action_history.append(
                    {"action": action, "input": action_input, "result": result}
                )
                return result
            except Exception as e:
                error_msg = f"Error executing {action}: {str(e)}"
                self.action_history.append(
                    {"action": action, "input": action_input, "result": error_msg}
                )
                return error_msg
        else:
            return f"Unknown action: {action}. Available actions: {list(self.available_tools.keys())}"

    def solve_with_react(self, problem: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Solve a problem using ReAct methodology."""
        conversation = []
        initial_prompt = self.get_react_prompt(problem)
        conversation.append({"role": "user", "content": initial_prompt})

        for iteration in range(max_iterations):
            try:
                # Get AI response
                response = client.chat.completions.create(
                    model=self.model,
                    messages=conversation,
                    temperature=0.1,
                    max_tokens=800,
                )

                ai_response = response.choices[0].message.content
                conversation.append({"role": "assistant", "content": ai_response})

                self.thought_history.append(
                    {"iteration": iteration + 1, "response": ai_response}
                )

                # Check if there's an action to execute
                action_info = self.parse_action(ai_response)

                if action_info:
                    # Execute the action
                    result = self.execute_action(
                        action_info["action"], action_info["input"]
                    )

                    # Add observation to conversation
                    observation = f"Observation: {result}"
                    conversation.append({"role": "user", "content": observation})

                    # Check if this looks like a final answer
                    if (
                        "final answer" in ai_response.lower()
                        or "conclusion" in ai_response.lower()
                    ):
                        break
                else:
                    # No action found, might be final answer
                    if iteration > 0:  # Give at least one chance for actions
                        break

            except Exception as e:
                error_msg = f"Error in iteration {iteration + 1}: {str(e)}"
                self.thought_history.append(
                    {"iteration": iteration + 1, "response": error_msg}
                )
                break

        return {
            "problem": problem,
            "conversation": conversation,
            "thought_history": self.thought_history,
            "action_history": self.action_history,
            "final_response": (
                conversation[-1]["content"] if conversation else "No response"
            ),
        }


def demonstrate_math_problem():
    """Demonstrates ReAct on a mathematical problem requiring calculations."""
    problem = """
    I'm planning a dinner party for 12 people. Each person will eat approximately 0.5 pounds of meat.
    Meat costs $8.50 per pound. I also need vegetables that cost $3.25 per person.
    What's the total cost for the meat and vegetables? Also, if I have a budget of $80,
    will that be enough?
    """

    console.print(Panel("🧮 Mathematical Problem with ReAct", style="bold blue"))
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")

    agent = ReActAgent()
    result = agent.solve_with_react(problem)

    console.print("\n[bold yellow]🤔 Reasoning and Actions:[/bold yellow]")
    for i, thought in enumerate(result["thought_history"]):
        console.print(f"\n[bold]Step {thought['iteration']}:[/bold]")
        console.print(thought["response"])

        # Show corresponding actions if any
        step_actions = [
            a
            for a in result["action_history"]
            if len(result["action_history"]) >= thought["iteration"]
        ]
        if step_actions and len(step_actions) >= thought["iteration"]:
            action = step_actions[thought["iteration"] - 1]
            console.print(
                f"[green]→ Action: {action['action']}({action['input']}) = {action['result']}[/green]"
            )

    console.print(f"\n[bold green]🎯 Final Answer:[/bold green]")
    console.print(Markdown(result["final_response"]))


def demonstrate_research_task():
    """Demonstrates ReAct on a research and analysis task."""
    problem = """
    I need to analyze the word count and create a summary of this text about artificial intelligence:
    
    "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural 
    intelligence displayed by humans and animals. Leading AI textbooks define the field as the study 
    of 'intelligent agents': any device that perceives its environment and takes actions that maximize 
    its chance of successfully achieving its goals. Colloquially, the term 'artificial intelligence' 
    is often used to describe machines that mimic 'cognitive' functions that humans associate with 
    the human mind, such as 'learning' and 'problem solving'. As machines become increasingly capable, 
    tasks considered to require 'intelligence' are often removed from the definition of AI, a phenomenon 
    known as the AI effect."
    
    Please save this analysis to memory for future reference.
    """

    console.print(Panel("📊 Research and Analysis with ReAct", style="bold magenta"))
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")

    agent = ReActAgent()
    result = agent.solve_with_react(problem)

    console.print("\n[bold yellow]📝 Analysis Process:[/bold yellow]")

    # Create a table showing the actions taken
    action_table = Table(title="Actions Performed")
    action_table.add_column("Step", style="cyan")
    action_table.add_column("Tool Used", style="green")
    action_table.add_column("Input", style="yellow")
    action_table.add_column("Result", style="white")

    for i, action in enumerate(result["action_history"]):
        action_table.add_row(
            str(i + 1),
            action["action"],
            (
                action["input"][:50] + "..."
                if len(action["input"]) > 50
                else action["input"]
            ),
            (
                action["result"][:50] + "..."
                if len(action["result"]) > 50
                else action["result"]
            ),
        )

    console.print(action_table)

    console.print(f"\n[bold green]📋 Final Analysis:[/bold green]")
    console.print(Markdown(result["final_response"]))


def demonstrate_planning_task():
    """Demonstrates ReAct on a planning task with memory usage."""
    problem = """
    Help me plan a productive work schedule. I work from 9 AM to 5 PM (8 hours).
    I need to:
    1. Attend a 2-hour meeting from 10-12 PM
    2. Complete a report that takes about 3 hours
    3. Answer emails (1 hour total)
    4. Have lunch (1 hour)
    5. Review documents (1.5 hours)
    
    Calculate if this fits in my day, create a schedule, and save it to memory.
    Also check what time I'll be free if everything goes as planned.
    """

    console.print(Panel("📅 Work Planning with ReAct", style="bold green"))
    console.print(f"[bold]Problem:[/bold] {problem.strip()}")

    agent = ReActAgent()
    result = agent.solve_with_react(problem, max_iterations=8)

    console.print("\n[bold yellow]⚡ Planning Process:[/bold yellow]")
    for thought in result["thought_history"]:
        console.print(f"\n[cyan]Iteration {thought['iteration']}:[/cyan]")
        console.print(
            thought["response"][:200] + "..."
            if len(thought["response"]) > 200
            else thought["response"]
        )

    console.print("\n[bold blue]🛠️ Tools Used:[/bold blue]")
    for action in result["action_history"]:
        console.print(f"• {action['action']}: {action['result'][:100]}...")

    console.print(f"\n[bold green]📋 Final Schedule:[/bold green]")
    console.print(Markdown(result["final_response"]))


def interactive_react_mode():
    """Interactive mode for ReAct problem solving."""
    console.print(Panel("🤖 Interactive ReAct Agent", style="bold cyan"))
    console.print("Enter problems that can benefit from reasoning + actions!")
    console.print("Available tools: calculator, memory operations, text analysis, time")
    console.print("Type 'quit' to exit.\n")

    agent = ReActAgent()

    while True:
        try:
            problem = input("Your problem: ").strip()

            if problem.lower() in ["quit", "exit", "q"]:
                console.print("👋 Goodbye!")
                break

            if not problem:
                console.print("Please enter a problem to solve.")
                continue

            console.print("\n[bold blue]🤖 ReAct Agent Working...[/bold blue]")
            result = agent.solve_with_react(problem)

            console.print("\n[bold yellow]💭 Reasoning Process:[/bold yellow]")
            for thought in result["thought_history"]:
                console.print(
                    f"Step {thought['iteration']}: {thought['response'][:150]}..."
                )

            if result["action_history"]:
                console.print(f"\n[bold cyan]🔧 Actions Taken:[/bold cyan]")
                for action in result["action_history"]:
                    console.print(f"→ {action['action']}: {action['result'][:100]}...")

            console.print(f"\n[bold green]🎯 Solution:[/bold green]")
            console.print(Markdown(result["final_response"]))
            console.print("\n" + "=" * 60 + "\n")

        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main function to run ReAct demonstrations."""
    console.print(
        Panel.fit(
            "🤖 ReAct (Reason + Act) Prompting Demonstration",
            style="bold white on blue",
        )
    )

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set![/red]")
        console.print("Please set your OpenAI API key in the .env file.")
        sys.exit(1)

    console.print("\n[bold]What is ReAct (Reason + Act) Prompting?[/bold]")
    console.print(
        """
ReAct combines reasoning with action-taking capabilities. The AI thinks through
problems step by step while also using tools to gather information, perform
calculations, or interact with external systems. This creates more capable and
interactive AI agents.
    """
    )

    # Show available tools
    agent = ReActAgent()
    console.print(f"\n[bold]Available Tools:[/bold]")
    for tool_name, tool_func in agent.available_tools.items():
        console.print(f"• {tool_name}: {tool_func.__doc__}")

    # Run demonstrations
    console.print("\n" + "=" * 70)
    demonstrate_math_problem()

    console.print("\n" + "=" * 70)
    demonstrate_research_task()

    console.print("\n" + "=" * 70)
    demonstrate_planning_task()

    console.print("\n" + "=" * 70)

    # Ask if user wants interactive mode
    console.print(
        "\n[bold]Would you like to try ReAct on your own problems? (y/n)[/bold]"
    )
    choice = input().strip().lower()

    if choice in ["y", "yes"]:
        interactive_react_mode()
    else:
        console.print("🤖 ReAct demonstration complete!")


if __name__ == "__main__":
    main()
