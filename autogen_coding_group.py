"""AG2 example: group chat with an engineer and critic collaborating on code."""

from autogen import (
    AssistantAgent,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
    config_list_from_json,
)
from autogen.cache import Cache

from config import AG2_CONFIG_FILE, AG2_USE_DOCKER, AG2_WORK_DIR

config_list = config_list_from_json(env_or_file=AG2_CONFIG_FILE)
llm_config = {"config_list": config_list}

user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": AG2_WORK_DIR, "use_docker": AG2_USE_DOCKER},
    human_input_mode="NEVER",
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message=(
        "You are a professional Python engineer. You write clean, "
        "well-structured code that is easy to read and maintain."
    ),
)

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

groupchat = GroupChat(agents=[user_proxy, engineer, critic], messages=[], max_round=20)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

task = "Write a snake game using Pygame."

with Cache.disk(cache_seed=43) as cache:
    user_proxy.initiate_chat(recipient=manager, message=task, cache=cache)
