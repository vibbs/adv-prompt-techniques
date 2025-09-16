# Tree-of-Thoughts (ToT) Prompting

## Overview

Tree-of-Thoughts (ToT) is an advanced prompting technique that enables AI models to explore multiple reasoning paths simultaneously, evaluate different approaches, and backtrack when necessary. Unlike Chain-of-Thought which follows a linear path, ToT creates a branching structure of possibilities.

## How It Works

ToT operates through a multi-phase process:

1. **Thought Generation**: Create multiple different reasoning approaches
2. **Evaluation**: Assess each approach for feasibility and quality  
3. **Selection**: Choose the most promising path(s)
4. **Expansion**: Develop the selected approach(es) into complete solutions
5. **Backtracking**: Return to alternatives if the current path fails

## Key Components

### 1. Thought States
- Individual reasoning steps or approaches
- Can be partial solutions, strategies, or analysis frameworks
- Maintained in a tree-like structure

### 2. State Evaluation
- Systematic assessment of each thought state
- Criteria: feasibility, completeness, clarity, potential
- Helps guide exploration priorities

### 3. Search Strategy
- Breadth-first: Explore all options at each level
- Depth-first: Follow promising paths to completion
- Best-first: Always pursue the highest-rated options

## Benefits

- ✅ **Multiple Perspectives**: Explores diverse solution approaches
- ✅ **Adaptive Reasoning**: Can backtrack and try alternatives
- ✅ **Quality Control**: Evaluates approaches before committing
- ✅ **Creative Solutions**: Discovers non-obvious approaches
- ✅ **Robust Problem Solving**: Less likely to get stuck in dead ends

## Use Cases

### 1. Creative Problem Solving
- Design challenges
- Innovation projects
- Artistic composition
- Product development

### 2. Strategic Planning
- Business strategy
- Project planning  
- Resource allocation
- Risk management

### 3. Complex Decision Making
- Multi-criteria decisions
- Long-term planning
- Trade-off analysis
- Scenario planning

### 4. Research and Analysis
- Literature reviews
- Data interpretation
- Hypothesis generation
- Scientific reasoning

## Setup

1. **Environment Setup**:
   ```bash
   # Make sure you're in the project root
   cd /path/to/adv-prompt-techniques
   
   # Install dependencies
   uv sync
   ```

2. **API Configuration**:
   - Ensure your `.env` file contains:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Running the Example

```bash
# From the project root
uv run tree-of-thoughts/main.py

# Or navigate to the folder first
cd tree-of-thoughts
uv run main.py
```

## Example Demonstrations

### 1. Creative Problem Solving
Designs a public park with multiple constraints, exploring different architectural and community-focused approaches.

### 2. Strategic Planning  
Develops startup strategies by considering multiple business approaches and evaluation criteria.

### 3. Complex Decision Making
Analyzes family relocation decisions by exploring different prioritization frameworks.

## ToT Implementation Structure

```python
class TreeOfThoughts:
    def generate_thoughts(self, problem: str, num_thoughts: int = 3):
        """Generate multiple initial approaches"""
        
    def evaluate_thoughts(self, thoughts: List[str]):
        """Evaluate each approach systematically"""
        
    def expand_best_thought(self, best_thought: str):
        """Develop the selected approach fully"""
        
    def solve_problem(self, problem: str):
        """Complete ToT workflow"""
```

## Best Practices

### 1. Thought Generation
- Generate 3-5 diverse initial approaches
- Encourage different perspectives and methodologies
- Avoid similar or redundant thinking paths

### 2. Evaluation Criteria
- **Feasibility**: Can this approach actually work?
- **Completeness**: Does it address all aspects of the problem?
- **Clarity**: Is the reasoning clear and understandable?
- **Innovation**: Does it offer unique insights or solutions?

### 3. Path Management
- Keep track of explored paths to avoid repetition
- Set depth limits to prevent infinite exploration
- Maintain evaluation scores for comparison

### 4. Termination Conditions
- Solution quality threshold reached
- Maximum exploration depth exceeded
- Resource/token limits approached
- All viable paths explored

## Comparison with Other Techniques

| Technique            | Structure   | Exploration    | Best For                  |
| -------------------- | ----------- | -------------- | ------------------------- |
| **Chain-of-Thought** | Linear      | Single path    | Step-by-step problems     |
| **Tree-of-Thoughts** | Branching   | Multiple paths | Creative/complex problems |
| **ReAct**            | Interactive | Action-based   | Tool-using tasks          |

## Limitations

- **Computational Cost**: Requires multiple LLM calls
- **Complexity Management**: Can become unwieldy with deep trees
- **Evaluation Challenges**: Difficult to assess partial solutions
- **Token Consumption**: High usage due to multiple explorations

## Advanced Variations

### 1. Pruned ToT
- Automatically eliminate low-scoring branches
- Focus resources on promising paths
- Reduce computational overhead

### 2. Collaborative ToT  
- Multiple models explore different branches
- Combine diverse reasoning capabilities
- Cross-validate evaluations

### 3. Iterative ToT
- Multiple rounds of generation and evaluation
- Refine approaches based on learning
- Progressive solution improvement

## Research Papers

- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
- [Large Language Models are Human-Level Prompt Engineers](https://arxiv.org/abs/2211.01910)

## Next Steps

After mastering ToT, explore:
- **Self-Consistency with ToT**: Multiple ToT runs for robust solutions
- **ToT + ReAct**: Combining tree exploration with action execution  
- **Meta-ToT**: Using ToT to optimize ToT strategies
