from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai.chat import OpenAIChat
from agno.tools.shell import ShellTools
from phi.tools.sql import SQLTools
from phi.tools.file import FileTools
from phi.tools.website import WebsiteTools
from tools import APIData
import json
import os

def simple_agent(): 
    agent = Agent(
        name="Simple Agent",
        model = Groq(id="llama-3.3-70b-versatile")
    )

    agent.print_response("Tell me a Dad Joke")

def openai_agent():
    agent = Agent(
        name="simple OpenAi Agent",
        model=OpenAIChat(id="gpt-4o"),
        markdown=True
    )

    agent.print_response("Tell me a Dad Joke")


def automator_agent(command: str, ):

    base_dir = os.path.join(os.getcwd(), "temp")
    pwd = os.path.abspath(os.path.dirname(__file__))
    db_url = f'sqlite:///{os.path.join(pwd, "database.db")}'

    agent = Agent(
        name="Automator Agent",
        model = Groq(id="llama-3.3-70b-versatile"),
        # model= Groq(id="mixtral-8x7b-32768"),
        tools=[ShellTools(), FileTools(), APIData(),SQLTools(db_url=db_url), WebsiteTools()],
        instructions=["""
        Anytime you are asked to download or generate data from a script 
        make sure you download it in current directory. Python scripts are to be stored in scripts folder. 
        Data generated by any script should be under data folder. If director exists, override it or create a new versioned folder in it.
        """,
        """
            - If asked to write information in a separate file and it does not exist, create it.
            - If asked to clone a repo, make a repo dir and inside it clone it with repo name as folder.
            - If asked to scrape, use tools given and print scrapped data in tabular format
        """
        """
            Base working directory is: {base_dir}
        """,
        "Use FileTools for performing file operations."
        ],
        show_tool_calls=True
    )

    agent.print_response(command)

    # Get the response from the agent
    response = agent.run(command)

    result = {
        "agent_response": response.to_json(),
        "command": command,
        "agent_name": agent.name
    }

    print("\nAPI Response:")
    print(json.dumps(result, indent=2))

    return result