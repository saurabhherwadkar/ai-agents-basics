"""Centralized configuration loaded from environment variables."""

# Import the os module for accessing environment variables
import os

# Import load_dotenv to read variables from a .env file
from dotenv import load_dotenv

# Load environment variables from the .env file into os.environ
load_dotenv()

# Retrieve the required OpenAI API key (raises KeyError if missing)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Retrieve the optional AgentOps API key with empty string default
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY", "")

# Set the default LLM model name for general use
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# Set the model used by CrewAI's hierarchical manager agent
MANAGER_MODEL = os.getenv("MANAGER_MODEL", "gpt-4o")

# Set the working directory where AG2 agents save generated code
AG2_WORK_DIR = os.getenv("AG2_WORK_DIR", "working")

# Determine whether AG2 should execute code inside Docker containers
AG2_USE_DOCKER = os.getenv("AG2_USE_DOCKER", "false").lower() == "true"

# Path to the AG2 JSON config file containing model endpoints
AG2_CONFIG_FILE = os.getenv("AG2_CONFIG_FILE", "OAI_CONFIG_LIST")

# Maximum requests per minute allowed for CrewAI API calls
CREWAI_MAX_RPM = int(os.getenv("CREWAI_MAX_RPM", "100"))

# Default file path for the image used in vision examples
DEFAULT_IMAGE_PATH = os.getenv("DEFAULT_IMAGE_PATH", "animals.png")

# Maximum number of tokens the vision model can return
VISION_MAX_TOKENS = int(os.getenv("VISION_MAX_TOKENS", "300"))
