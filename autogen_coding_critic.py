"""AG2 example: engineer + code reviewer using nested chats for automatic review."""

# Import AG2 agent classes and config loader
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Import project-level settings for AG2
from config import AG2_CONFIG_FILE, AG2_USE_DOCKER, AG2_WORK_DIR

# Load the list of model configurations from the JSON config file
config_list = config_list_from_json(env_or_file=AG2_CONFIG_FILE)

# Create the shared LLM configuration dictionary
llm_config = {"config_list": config_list}

# Create a user proxy agent that executes code and handles human input
user_proxy = UserProxyAgent(
    name="User",
    code_execution_config={"work_dir": AG2_WORK_DIR, "use_docker": AG2_USE_DOCKER},
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
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

# Create a reviewer agent that critiques code for bugs and best practices
reviewer = AssistantAgent(
    name="Reviewer",
    llm_config=llm_config,
    system_message=(
        "You are a code reviewer known for thoroughness and commitment to standards. "
        "You scrutinize code for bugs, security issues, and adherence to best practices. "
        "Output a list of issues or improvements."
    ),
)


# Define a callback that extracts the last message for the reviewer to critique
def review_code(recipient, messages, sender, config):
    last_content = recipient.chat_messages_for_summary(sender)[-1]["content"]
    return f"Review and critique the following code:\n\n{last_content}"


# Register a nested chat so the reviewer automatically reviews engineer output
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

# Define the task to send to the engineer
task = "Write a snake game using Pygame."

# Start the conversation between user proxy and engineer with a 2-turn limit
user_proxy.initiate_chat(recipient=engineer, message=task, max_turns=2, summary_method="last_msg")
