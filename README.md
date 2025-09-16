# Advanced Prompting Techniques for Complex Reasoning

This repository contains code examples and implementations for advanced prompting techniques that enhance AI reasoning capabilities. Each technique is demonstrated with practical Python implementations using OpenAI's GPT models.

## 🚀 Quick Start

### Prerequisites
- Python 3.13.2 or higher
- OpenAI API key
- uv package manager

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd adv-prompt-techniques
```

2. Set up your environment:
```bash
# Copy the environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

3. Install dependencies using uv:
```bash
uv sync
```

## 📚 Techniques Covered

This repository demonstrates six advanced prompting techniques:

### 1. [Chain-of-Thought (CoT)](./chain-of-thought/)
Sequential reasoning that breaks down complex problems into logical steps, making AI reasoning more transparent and accurate.

**Use Cases:** Mathematical problems, logical reasoning, step-by-step analysis

### 2. [Tree-of-Thoughts (ToT)](./tree-of-thoughts/)
Explores multiple reasoning paths simultaneously, allowing the AI to backtrack and explore alternative solutions when needed.

**Use Cases:** Creative problem solving, strategic planning, complex decision making

### 3. [ReAct (Reason + Act)](./react/)
Combines reasoning with action-taking capabilities, enabling AI to interact with external tools and environments while maintaining logical thinking.

**Use Cases:** Tool usage, API interactions, multi-step workflows

### 4. [Prompt Chaining](./prompt-chaining/)
Connects multiple prompts in sequence, where each prompt builds upon the output of the previous one for complex, multi-stage tasks.

**Use Cases:** Content generation pipelines, data processing workflows, multi-step analysis

### 5. [Meta Prompting](./meta-prompting/)
Uses AI to optimize and generate better prompts, creating a self-improving prompting system.

**Use Cases:** Prompt optimization, automated prompt generation, prompt engineering

### 6. [RSIP (Recursive Self-Improvement Prompting)](./rsip/)
Implements recursive self-reflection and improvement, allowing AI to iteratively refine its own outputs.

**Use Cases:** Content refinement, iterative problem solving, quality improvement

## 🛠️ Project Structure

```
adv-prompt-techniques/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── chain-of-thought/
│   ├── main.py
│   └── README.md
├── tree-of-thoughts/
│   ├── main.py
│   └── README.md
├── react/
│   ├── main.py
│   └── README.md
├── prompt-chaining/
│   ├── main.py
│   └── README.md
├── meta-prompting/
│   ├── main.py
│   └── README.md
└── rsip/
    ├── main.py
    └── README.md
```

## 🏃‍♂️ Running the Examples

Each technique folder contains its own `main.py` file. To run any example:

```bash
# Navigate to the technique folder
cd chain-of-thought

# Run the example
uv run main.py
```

Or run from the root directory:

```bash
uv run chain-of-thought/main.py
```

Other folders can be run similarly by replacing `chain-of-thought` with the desired technique folder name.

```bash
uv run tree-of-thoughts/main.py
uv run react/main.py
uv run prompt-chaining/main.py
uv run meta-prompting/main.py
uv run rsip/main.py
```

## 📝 Configuration

All examples use the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from creating .pyc files

## 🧪 Development

To set up for development:

```bash
# Install development dependencies
uv sync --dev

# Format code
uv run black .

# Sort imports
uv run isort .

# Lint code
uv run flake8
```

## 📖 Blog Article

This repository supports the blog article: **"Advanced Prompting Techniques for Complex Reasoning"**

Each technique folder contains:
- **Implementation**: Working Python code demonstrating the technique
- **Documentation**: Detailed explanation of the technique, setup, and usage
- **Examples**: Practical use cases and sample outputs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Chain-of-Thought Prompting Paper](https://arxiv.org/abs/2201.11903)
- [Tree of Thoughts Paper](https://arxiv.org/abs/2305.10601)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)


## Result of Advanced Prompting Techniques
See the [results documentation](./docs/results.md) for example outputs from each technique.

## 📧 Contact

For questions or suggestions, please open an issue in this repository.

---


Built with ❤️ by [Vaibhav Doddihal](https://www.linkedin.com/in/vaibhavdoddihal/) | [BlockSimplified](https://www.blocksimplified.com/)

**Happy Prompting! 🎯**
