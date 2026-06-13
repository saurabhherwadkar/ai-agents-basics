"""CrewAI example: a coding crew with engineer, QA, and chief QA agents."""

from textwrap import dedent

from crewai import Agent, Crew, Process, Task

import config  # noqa: F401 — ensures .env is loaded

print("## Welcome to the Game Crew")
print("-------------------------------")
game = input("What game would you like to build? Describe the mechanics:\n")

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

code_task = Task(
    description=dedent(f"""\
        Create a game using Python based on these instructions:
        {game}
        Write the complete code for the game."""),
    expected_output="The full Python code for the game, and nothing else.",
    agent=senior_engineer,
)

qa_task = Task(
    description=dedent(f"""\
        Review the game code for the following game:
        {game}
        Check for logic errors, syntax errors, missing imports, variable
        declarations, mismatched brackets, and security vulnerabilities."""),
    expected_output="A list of issues found in the code.",
    agent=qa_engineer,
)

evaluate_task = Task(
    description=dedent(f"""\
        Evaluate the game code for the following game:
        {game}
        Ensure the code is complete and does the job it is supposed to do.
        Apply any necessary fixes."""),
    expected_output="The corrected full Python code, and nothing else.",
    agent=chief_qa_engineer,
)

crew = Crew(
    agents=[senior_engineer, qa_engineer, chief_qa_engineer],
    tasks=[code_task, qa_task, evaluate_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
print("\n######################")
print(result)
