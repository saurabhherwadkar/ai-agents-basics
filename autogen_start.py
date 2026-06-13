"""Basic AG2 example: a conversable agent that generates code from user requests."""

from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

from config import AG2_CONFIG_FILE, AG2_USE_DOCKER, AG2_WORK_DIR

config_list = config_list_from_json(env_or_file=AG2_CONFIG_FILE)

assistant = ConversableAgent(
    name="Assistant",
    llm_config={"config_list": config_list},
)

user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": AG2_WORK_DIR, "use_docker": AG2_USE_DOCKER},
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
)

user_proxy.initiate_chat(assistant, message="Write a snake game using Pygame.")
