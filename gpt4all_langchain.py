from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Load the language model we're going to use to control the agent.
local_path = './models/ggml-gpt4all-j-v1.3-groovy.bin'

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)

# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
llm = GPT4All(model=local_path, backend='gptj', callbacks=callbacks, verbose=True)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["human","llm-math", "arxiv", "wikipedia", "python_repl", "open-meteo-api", "terminal"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Now let's test it out!
question = input('Question: ')
agent.run(question)
