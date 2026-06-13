"""CrewAI example: hierarchical process with a manager coordinating agents."""

# Import dedent for clean multi-line string formatting
from textwrap import dedent

# Import core CrewAI classes for building agent workflows
from crewai import Agent, Crew, Process, Task

# Import the manager model setting from project config
from config import MANAGER_MODEL

# Print a welcome banner for the hierarchical game crew
print("## Welcome to the Game Crew (Hierarchical)")
print("--------------------------------------------")

# Prompt the user to describe the game they want built
game = input("What game would you like to build? Describe the mechanics:\n")

# Create a senior engineer agent responsible for writing the game code
senior_engineer = Agent(
    role="Senior Software Engineer",
    goal="Create software as needed",
    backstory=dedent("""\
        You are a Senior Software Engineer at a leading tech think tank.
        Your expertise is programming in Python, and you produce clean,
        well-structured, production-quality code."""),
    allow_delegation=False,
    verbose=True,
)

# Create a QA engineer agent that reviews code for errors and vulnerabilities
qa_engineer = Agent(
    role="Software Quality Control Engineer",
    goal="Analyze code for errors and produce a list of issues",
    backstory=dedent("""\
        You are a software engineer specializing in code review.
        You have an eye for detail and a knack for finding hidden bugs.
        You check for missing imports, variable declarations, mismatched
        brackets, syntax errors, security vulnerabilities, and logic errors."""),
    allow_delegation=False,
    verbose=True,
)

# Create a chief QA agent that validates the final code meets requirements
chief_qa_engineer = Agent(
    role="Chief Software Quality Control Engineer",
    goal="Ensure the code does the job it is supposed to do",
    backstory=dedent("""\
        You are a Chief Software Quality Control Engineer responsible for
        ensuring that code meets the highest quality standards. You verify
        correctness, completeness, and adherence to requirements."""),
    allow_delegation=True,
    verbose=True,
)

# Define the coding task for the senior engineer to implement the game
code_task = Task(
    description=dedent(f"""\
        Create a game using Python based on these instructions:
        {game}
        Write the complete code for the game."""),
    expected_output="The full Python code for the game, and nothing else.",
    agent=senior_engineer,
)

# Define the QA task to review the generated code for issues
qa_task = Task(
    description=dedent(f"""\
        Review the game code for the following game:
        {game}
        Check for logic errors, syntax errors, missing imports, variable
        declarations, mismatched brackets, and security vulnerabilities."""),
    expected_output="A list of issues found in the code.",
    agent=qa_engineer,
)

# Define the evaluation task for the chief QA to fix and finalize the code
evaluate_task = Task(
    description=dedent(f"""\
        Evaluate the game code for the following game:
        {game}
        Ensure the code is complete and does the job it is supposed to do.
        Apply any necessary fixes."""),
    expected_output="The corrected full Python code, and nothing else.",
    agent=chief_qa_engineer,
)

# Assemble the crew using hierarchical process with a manager LLM coordinating
crew = Crew(
    agents=[senior_engineer, qa_engineer, chief_qa_engineer],
    tasks=[code_task, qa_task, evaluate_task],
    process=Process.hierarchical,
    manager_llm=MANAGER_MODEL,
    verbose=True,
)

# Kick off the crew and print the final corrected code
result = crew.kickoff()
print("\n######################")
print(result)
