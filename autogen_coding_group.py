"""AG2 example: group chat with an engineer and critic collaborating on code."""

# Import AG2 agent classes, group chat components, and config loader
from autogen import (
    AssistantAgent,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
    config_list_from_json,
)

# Import the Cache class for disk-based response caching
from autogen.cache import Cache

# Import project-level settings for AG2
from config import AG2_CONFIG_FILE, AG2_USE_DOCKER, AG2_WORK_DIR

# Load the list of model configurations from the JSON config file
config_list = config_list_from_json(env_or_file=AG2_CONFIG_FILE)

# Create the shared LLM configuration dictionary
llm_config = {"config_list": config_list}

# Create a user proxy agent with no human input for fully autonomous operation
user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": AG2_WORK_DIR, "use_docker": AG2_USE_DOCKER},
    human_input_mode="NEVER",
)

# Create an engineer agent that writes clean Python code
engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message=(
        "You are a professional Python engineer. You write clean, "
        "well-structured code that is easy to read and maintain."
    ),
)

# Create a critic agent that scores code across multiple dimensions
critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message=(
        "You are a game engineer and master evaluator. Score code from 1 (bad) to 10 (good) "
        "across these dimensions:\n"
        "- Bugs: logic errors, syntax errors, missing imports. If ANY bug exists, score < 5.\n"
        "- Gameplay: engagement, fun, challenge.\n"
        "- Goal compliance: how well the code meets the specified goals.\n"
        "- Aesthetics: visual appropriateness for the game theme.\n\n"
        "Provide scores as: {bugs: N, gameplay: N, compliance: N, aesthetics: N}\n"
        "Do not suggest code. Instead, provide a concrete list of actions for the coder."
    ),
)

# Create a group chat with user proxy, engineer, and critic for 20 rounds max
groupchat = GroupChat(agents=[user_proxy, engineer, critic], messages=[], max_round=20)

# Create a manager agent that orchestrates turn-taking in the group chat
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Define the task to send to the group
task = "Write a snake game using Pygame."

# Use disk caching with a fixed seed for reproducible group conversations
with Cache.disk(cache_seed=43) as cache:

    # Start the group chat by sending the task to the manager
    user_proxy.initiate_chat(recipient=manager, message=task, cache=cache)
