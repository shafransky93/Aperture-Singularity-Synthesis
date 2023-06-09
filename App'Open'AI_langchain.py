from langchain import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from config import OPENAI_API_KEY
import os
import sys

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# First, let's load the language model we're going to use to control the agent.
dv = OpenAI(model_name='text-davinci-003')
llm = dv

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["llm-math", "arxiv", "wikipedia", "python_repl", "open-meteo-api", "terminal"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Start the user input loop
while True:
    # Prompt the user for input
    user_input = input("Enter a command: ")

    # Pass the user input to the agent
    print(user_input)
    agent.run(user_input)
