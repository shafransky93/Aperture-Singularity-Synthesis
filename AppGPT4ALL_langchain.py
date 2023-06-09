from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.tools.base import StructuredTool
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from config import LOCAL_PATH

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
llm = GPT4All(model=LOCAL_PATH, backend='gptj', callbacks=callbacks, verbose=True)

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
