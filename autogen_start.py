"""Basic AG2 example: a conversable agent that generates code from user requests."""

# Import the core AG2 agent classes and config loader
from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

# Import project-level settings for AG2
from config import AG2_CONFIG_FILE, AG2_USE_DOCKER, AG2_WORK_DIR

# Load the list of model configurations from the JSON config file
config_list = config_list_from_json(env_or_file=AG2_CONFIG_FILE)

# Create an AI assistant agent that can generate responses using the LLM
assistant = ConversableAgent(
    name="Assistant",
    llm_config={"config_list": config_list},
)

# Create a user proxy agent that executes code and relays human input
user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": AG2_WORK_DIR, "use_docker": AG2_USE_DOCKER},
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
)

# Start the conversation by asking the assistant to write a snake game
user_proxy.initiate_chat(assistant, message="Write a snake game using Pygame.")
