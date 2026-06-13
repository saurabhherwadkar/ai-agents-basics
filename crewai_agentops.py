"""CrewAI example: joke crew with AgentOps observability integration."""

# Import the AgentOps library for monitoring and tracing agent runs
import agentops

# Import core CrewAI classes for building agent workflows
from crewai import Agent, Crew, Process, Task

# Import the AgentOps API key and rate limit setting from project config
from config import AGENTOPS_API_KEY, CREWAI_MAX_RPM

# Initialize AgentOps session for observability and tracing
agentops.init(api_key=AGENTOPS_API_KEY)

# Create a joke researcher agent that analyzes what makes topics funny
joke_researcher = Agent(
    role="Senior Joke Researcher",
    goal="Research what makes things funny about the following {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "Driven by slapstick humor, you are a seasoned joke researcher "
        "who knows what makes people laugh. You have a knack for finding "
        "the funny in everyday situations and can turn a dull moment into "
        "a laugh riot."
    ),
    allow_delegation=True,
)

# Create a joke writer agent that crafts humorous one-liners
joke_writer = Agent(
    role="Joke Writer",
    goal="Write a humorous and funny joke on the following {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a joke writer with a flair for humor. You can turn a "
        "simple idea into a laugh riot. You have a way with words and "
        "can make people laugh with just a few lines."
    ),
    allow_delegation=False,
)

# Define the research task to analyze humor elements of the topic
research_task = Task(
    description=(
        "Identify what makes the following topic: {topic} so funny. "
        "Include the key elements that make it humorous. "
        "Provide an analysis of current social trends and how they "
        "impact the perception of humor."
    ),
    expected_output="A comprehensive 3-paragraph report on the topic's humor.",
    agent=joke_researcher,
)

# Define the writing task to produce the final joke output
write_task = Task(
    description=(
        "Compose an insightful, humorous, and socially aware joke on {topic}. "
        "Include the key elements that make it funny and relevant to current trends."
    ),
    expected_output="A concise one-line joke on {topic}.",
    agent=joke_writer,
    output_file="the_best_joke.md",
)

# Assemble the crew with both agents, running tasks in sequential order
crew = Crew(
    agents=[joke_researcher, joke_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=CREWAI_MAX_RPM,
)

# Kick off the crew with the topic input and print the final result
result = crew.kickoff(inputs={"topic": "AI engineer jokes"})
print(result)
