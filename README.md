# AI Agents Basics

A collection of introductory examples demonstrating how to build AI agents using [AG2](https://github.com/ag2ai/ag2) (formerly AutoGen) and [CrewAI](https://github.com/crewai/crewai).

## Examples

### AG2 (AutoGen)

| Script | Description |
|--------|-------------|
| `autogen_start.py` | Basic conversable agent that generates code from user prompts |
| `autogen_coding_critic.py` | Engineer + reviewer using nested chats for automatic code review |
| `autogen_coding_critic_cache.py` | Same as above with disk caching for reproducible conversations |
| `autogen_coding_group.py` | Group chat with engineer and critic agents collaborating |

### CrewAI

| Script | Description |
|--------|-------------|
| `crewai_introduction.py` | Joke researcher + writer crew (sequential process) |
| `crewai_coding_crew.py` | Coding crew with engineer, QA, and chief QA agents |
| `crewai_hierarchy.py` | Hierarchical process with a manager LLM coordinating agents |
| `crewai_agentops.py` | Joke crew with [AgentOps](https://agentops.ai/) observability |

### Utilities

| Script | Description |
|--------|-------------|
| `describe_image.py` | Describe an image using OpenAI Vision API |

## Setup

### Prerequisites

- Python 3.11+
- An OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ai-agents-basics.git
cd ai-agents-basics

# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Configuration

All configuration is externalized into environment variables via a `.env` file and `OAI_CONFIG_LIST` for AG2.

1. Copy the example files:

```bash
cp .env.example .env
cp OAI_CONFIG_LIST.example OAI_CONFIG_LIST
```

2. Edit `.env` with your settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | (required) |
| `AGENTOPS_API_KEY` | AgentOps key for observability | (optional) |
| `MODEL_NAME` | Model used for vision and general tasks | `gpt-4o` |
| `MANAGER_MODEL` | Model for CrewAI hierarchical manager | `gpt-4o` |
| `AG2_WORK_DIR` | Directory where AG2 writes generated code | `working` |
| `AG2_USE_DOCKER` | Run AG2 code execution in Docker | `false` |
| `AG2_CONFIG_FILE` | Path to the AG2 model config list | `OAI_CONFIG_LIST` |
| `CREWAI_MAX_RPM` | CrewAI max requests per minute | `100` |
| `DEFAULT_IMAGE_PATH` | Image file for `describe_image.py` | `animals.png` |
| `VISION_MAX_TOKENS` | Max tokens for vision response | `300` |

3. Edit `OAI_CONFIG_LIST` with your OpenAI (or Azure OpenAI) API key.

The shared `config.py` module loads these values and is imported by all scripts.

## Running Examples

```bash
# AG2 examples
python autogen_start.py
python autogen_coding_critic.py
python autogen_coding_group.py

# CrewAI examples
python crewai_introduction.py
python crewai_coding_crew.py
python crewai_hierarchy.py

# Image description
python describe_image.py
```

## Project Structure

```
ai-agents-basics/
├── config.py                     # Centralized config (reads .env)
├── autogen_start.py              # AG2 basic agent
├── autogen_coding_critic.py      # AG2 nested chat review
├── autogen_coding_critic_cache.py# AG2 cached review
├── autogen_coding_group.py       # AG2 group chat
├── crewai_introduction.py        # CrewAI joke crew
├── crewai_coding_crew.py         # CrewAI coding crew
├── crewai_hierarchy.py           # CrewAI hierarchical
├── crewai_agentops.py            # CrewAI + AgentOps
├── describe_image.py             # OpenAI Vision
├── animals.png                   # Sample image for vision
├── pyproject.toml                # Project dependencies
├── .env.example                  # Environment variable template
└── OAI_CONFIG_LIST.example       # AG2 model config template
```

## License

MIT
