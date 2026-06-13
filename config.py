"""Centralized configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY", "")

# Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
MANAGER_MODEL = os.getenv("MANAGER_MODEL", "gpt-4o")

# AG2 Settings
AG2_WORK_DIR = os.getenv("AG2_WORK_DIR", "working")
AG2_USE_DOCKER = os.getenv("AG2_USE_DOCKER", "false").lower() == "true"
AG2_CONFIG_FILE = os.getenv("AG2_CONFIG_FILE", "OAI_CONFIG_LIST")

# CrewAI Settings
CREWAI_MAX_RPM = int(os.getenv("CREWAI_MAX_RPM", "100"))

# Vision Settings
DEFAULT_IMAGE_PATH = os.getenv("DEFAULT_IMAGE_PATH", "animals.png")
VISION_MAX_TOKENS = int(os.getenv("VISION_MAX_TOKENS", "300"))
