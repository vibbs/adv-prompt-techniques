# Chain-of-Thought (CoT) Prompting

## Overview

Chain-of-Thought (CoT) prompting is a technique that encourages AI models to break down complex problems into sequential reasoning steps. This approach makes the AI's thinking process transparent and often leads to more accurate results by mimicking human step-by-step problem-solving.

## How It Works

CoT prompting works by:
1. **Explicit Step Labeling**: Breaking problems into numbered steps
2. **Sequential Reasoning**: Following a logical progression from problem to solution
3. **Transparent Thinking**: Making the reasoning process visible
4. **Intermediate Steps**: Showing work for each part of the problem

## Key Benefits

- ✅ **Improved Accuracy**: Better results on complex reasoning tasks
- ✅ **Transparency**: Clear understanding of the AI's reasoning process  
- ✅ **Debugging**: Easy to identify where reasoning goes wrong
- ✅ **Reliability**: More consistent results across similar problems

## Use Cases

### 1. Mathematical Problems
- Multi-step calculations
- Word problems
- Algebraic equations
- Geometry proofs

### 2. Logical Reasoning
- Deductive reasoning
- Pattern recognition
- Cause-and-effect analysis
- Decision trees

### 3. Complex Analysis
- Business case studies
- Scientific reasoning
- Strategic planning
- Data interpretation

## Setup

1. **Environment Setup**:
   ```bash
   # Make sure you're in the project root
   cd /path/to/adv-prompt-techniques
   
   # Install dependencies
   uv sync
   ```

2. **API Configuration**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Running the Example

```bash
# From the project root
uv run chain-of-thought/main.py

# Or navigate to the folder first
cd chain-of-thought
uv run main.py
```

## Example Demonstrations

The script includes three demonstration scenarios:

### 1. Mathematical Problem Solving
Solves algebra problems involving systems of equations with step-by-step reasoning.

### 2. Logical Reasoning
Works through set theory problems using Venn diagrams and logical deduction.

### 3. Business Analysis
Analyzes revenue patterns and makes predictions with detailed reasoning.

## Interactive Mode

The script also includes an interactive mode where you can input your own problems and see how CoT reasoning handles them.

## CoT Prompt Template

```python
def cot_prompt_template(problem: str) -> str:
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
```

## Best Practices

1. **Clear Step Labels**: Use explicit step numbering (Step 1, Step 2, etc.)
2. **Logical Flow**: Ensure each step follows logically from the previous
3. **Show Work**: Include intermediate calculations and reasoning
4. **Verify Results**: Add a final verification or sanity check
5. **Consistent Format**: Use the same structure across similar problems

## Limitations

- **Longer Responses**: CoT generates more verbose outputs
- **Token Usage**: Requires more tokens than direct answering
- **Not Always Needed**: Simple problems might not benefit from CoT
- **Model Dependent**: Effectiveness varies across different AI models

## Research Papers

- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916)

## Next Steps

After understanding CoT, explore:
- **Tree-of-Thoughts**: For exploring multiple reasoning paths
- **ReAct**: For combining reasoning with actions
- **Self-Consistency**: For improving CoT reliability through multiple samples
