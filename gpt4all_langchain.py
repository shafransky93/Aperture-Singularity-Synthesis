from langchain import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# First, let's load the language model we're going to use to control the agent.
local_path = './ggml-gpt4all-j-v1.3-groovy.bin'
callbacks = [StreamingStdOutCallbackHandler()]
llm = GPT4All(model=local_path, backend='gptj', callbacks=callbacks, verbose=True)


# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["human","llm-math", "arxiv", "wikipedia", "python_repl", "open-meteo-api", "terminal"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Now let's test it out!
user_input = input("Question: ")
agent.run(user_input)
