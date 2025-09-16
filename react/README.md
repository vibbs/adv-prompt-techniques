# ReAct (Reason + Act) Prompting

## Overview

ReAct (Reasoning and Acting) is a powerful prompting technique that combines reasoning capabilities with action-taking abilities. Unlike pure reasoning methods, ReAct enables AI agents to interact with external tools, gather information dynamically, and perform actions while maintaining logical thinking processes.

## How It Works

ReAct operates through an iterative cycle:

1. **Thought**: The AI reasons about the problem and current situation
2. **Action**: The AI decides to use a tool or take an action  
3. **Observation**: The AI observes the result of the action
4. **Repeat**: The cycle continues until the problem is solved

This creates a dynamic problem-solving loop that can adapt based on new information.

## Core Components

### 1. Reasoning Engine
- Analyzes the current problem state
- Plans the next steps
- Interprets action results
- Maintains problem-solving context

### 2. Action Framework
- Predefined set of available tools
- Structured action calling format
- Error handling and validation
- Result interpretation

### 3. Memory System
- Tracks action history
- Stores intermediate results
- Maintains conversation context
- Enables learning from experience

## Key Benefits

- ✅ **Interactive Problem Solving**: Can gather information as needed
- ✅ **Tool Integration**: Works with external systems and APIs
- ✅ **Adaptive Reasoning**: Adjusts approach based on results
- ✅ **Transparent Process**: Shows both thinking and actions
- ✅ **Error Recovery**: Can handle failures and try alternatives

## Use Cases

### 1. Mathematical Problem Solving
- Multi-step calculations
- Unit conversions
- Financial analysis
- Statistical computations

### 2. Research and Analysis
- Information gathering
- Data processing
- Content summarization
- Fact verification

### 3. Planning and Scheduling
- Calendar management
- Resource allocation
- Task prioritization
- Timeline creation

### 4. Data Management
- File operations
- Database queries
- Content organization
- Information retrieval

## Available Tools

The example implementation includes these tools:

| Tool               | Purpose                   | Example Use                   |
| ------------------ | ------------------------- | ----------------------------- |
| `calculator`       | Mathematical computations | Calculate totals, percentages |
| `search_memory`    | Find stored information   | Retrieve previous results     |
| `save_to_memory`   | Store information         | Save important findings       |
| `get_current_time` | Get date/time             | Time-sensitive operations     |
| `word_count`       | Text analysis             | Count words/characters        |
| `summarize_text`   | Content summarization     | Create text summaries         |

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
uv run react/main.py

# Or navigate to the folder first
cd react
uv run main.py
```

## Example Demonstrations

### 1. Mathematical Problem Solving
Calculates dinner party costs using the calculator tool, showing step-by-step reasoning and computation.

### 2. Research and Analysis
Analyzes text content using word counting and summarization tools, then saves results to memory.

### 3. Planning Task
Creates work schedules by calculating time requirements and organizing tasks logically.

## ReAct Agent Implementation

```python
class ReActAgent:
    def __init__(self):
        self.available_tools = {
            "calculator": self.calculator,
            "search_memory": self.search_memory,
            # ... other tools
        }
        
    def solve_with_react(self, problem: str, max_iterations: int = 5):
        """Main ReAct solving loop"""
        # 1. Generate initial reasoning
        # 2. Parse for actions
        # 3. Execute actions
        # 4. Observe results
        # 5. Continue reasoning
        # 6. Repeat until solved
```

## Action Format

ReAct uses a structured format for actions:

```
Thought: I need to calculate the total cost for the dinner party.
Action: calculator
Action Input: 12 * 0.5 * 8.50
Observation: Result: 51.0
Thought: Now I need to calculate the vegetable costs...
Action: calculator
Action Input: 12 * 3.25
Observation: Result: 39.0
```

## Best Practices

### 1. Tool Design
- **Single Responsibility**: Each tool should have one clear purpose
- **Error Handling**: Return meaningful error messages
- **Input Validation**: Validate inputs before processing
- **Consistent Interface**: Standardize input/output formats

### 2. Reasoning Guidance
- **Clear Thoughts**: Encourage explicit reasoning steps
- **Action Planning**: Think before acting
- **Result Interpretation**: Analyze action outcomes
- **Progress Tracking**: Monitor problem-solving progress

### 3. Iteration Management
- **Set Limits**: Prevent infinite loops with max iterations
- **Early Termination**: Stop when problem is solved
- **State Tracking**: Monitor agent state changes
- **Context Preservation**: Maintain conversation history

### 4. Error Recovery
- **Graceful Degradation**: Handle tool failures elegantly
- **Alternative Approaches**: Try different tools if one fails
- **User Feedback**: Explain errors clearly
- **Retry Logic**: Attempt failed actions with modifications

## Advanced Features

### 1. Multi-Tool Workflows
- Chain multiple tools together
- Pass outputs between tools
- Create complex data processing pipelines
- Maintain intermediate results

### 2. Adaptive Tool Selection
- Choose tools based on problem type
- Learn from previous successful patterns
- Optimize tool usage over time
- Handle tool availability changes

### 3. Memory Management
- Persistent storage across sessions
- Information retrieval and search
- Context-aware memory operations
- Memory cleanup and organization

## Comparison with Other Techniques

| Technique            | Interaction | Tools    | Best For             |
| -------------------- | ----------- | -------- | -------------------- |
| **Chain-of-Thought** | None        | No       | Linear reasoning     |
| **Tree-of-Thoughts** | Limited     | No       | Multiple approaches  |
| **ReAct**            | Dynamic     | Yes      | Interactive problems |
| **Prompt Chaining**  | Sequential  | Possible | Multi-step workflows |

## Limitations

- **Tool Dependency**: Limited by available tools
- **Complexity Management**: Can become unwieldy with many tools
- **Error Propagation**: Tool failures can derail reasoning
- **Token Consumption**: High usage due to iterative process

## Integration Examples

### API Integration
```python
def call_weather_api(self, location: str) -> str:
    """Get weather information for a location."""
    # Implementation would call actual weather API
    
def call_database(self, query: str) -> str:
    """Query database for information."""
    # Implementation would execute database query
```

### File System Operations
```python
def read_file(self, filename: str) -> str:
    """Read contents of a file."""
    
def write_file(self, filename: str, content: str) -> str:
    """Write content to a file."""
```

## Research Papers

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)

## Next Steps

After mastering ReAct, explore:
- **Multi-Agent ReAct**: Multiple agents working together
- **ReAct + Planning**: Long-term goal-oriented behavior
- **Tool Learning**: Agents that can learn new tools
- **ReAct with Memory**: Persistent knowledge and learning
