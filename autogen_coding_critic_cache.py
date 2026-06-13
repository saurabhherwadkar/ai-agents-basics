"""AG2 example: engineer + reviewer with disk caching for reproducible conversations."""

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen.cache import Cache

from config import AG2_CONFIG_FILE, AG2_USE_DOCKER, AG2_WORK_DIR

config_list = config_list_from_json(env_or_file=AG2_CONFIG_FILE)
llm_config = {"config_list": config_list}

user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": AG2_WORK_DIR, "use_docker": AG2_USE_DOCKER},
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message=(
        "You are a professional Python engineer. You write clean, "
        "well-structured code that is easy to read and maintain."
    ),
)

reviewer = AssistantAgent(
    name="Reviewer",
    llm_config=llm_config,
    system_message=(
        "You are a code reviewer known for thoroughness and commitment to standards. "
        "You scrutinize code for bugs, security issues, and adherence to best practices. "
        "Output a list of issues or improvements."
    ),
)


def review_code(recipient, messages, sender, config):
    last_content = recipient.chat_messages_for_summary(sender)[-1]["content"]
    return f"Review and critique the following code:\n\n{last_content}"


user_proxy.register_nested_chats(
    [
        {
            "recipient": reviewer,
            "message": review_code,
            "summary_method": "last_msg",
            "max_turns": 3,
        }
    ],
    trigger=engineer,
)

task = "Write a snake game using Pygame."

with Cache.disk(cache_seed=42) as cache:
    user_proxy.initiate_chat(
        recipient=engineer,
        message=task,
        max_turns=2,
        summary_method="last_msg",
        cache=cache,
    )
