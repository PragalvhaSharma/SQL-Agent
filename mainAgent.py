import os
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, tool
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from sqlAgent import sqlAgent
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from dotenv import load_dotenv
load_dotenv()

# Retrieve API keys from environment variables
myOpenAIkey = os.environ["OPENAI_API_KEY"]
googleSearchKey = os.environ["SERPER_API_KEY"]

print(myOpenAIkey)
#Database INFO
userName = "postgres"
password = "984138o35o"
host = "localhost"
port = "5432"
mydatabase = "awsData"
pg_uri = f"postgresql+psycopg2://{userName}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)

#Initialize llm
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-1106', api_key=myOpenAIkey)

# Initialize a wrapper for SerpAPI-(GOOGLE SEARCH)
search = SerpAPIWrapper(serpapi_api_key=googleSearchKey)

# Define a tool function for the SQLAgent
##Placed incase for agent
@tool()
def SQLAgentTool(query: str) -> str:
    """Performs sql queries. YOU CANNOT CREAte OR ADD NEW TABLES. 
    E.g If the user says: How many work orders are finished? --- The user is asking how many work orders are set to true for the column finished.

       """
    try:
        # Attempt to invoke the SQL agent with the provided query
        logging.info(f"Query executed successfully: {query}")
        return sqlAgent.run(query)
    except Exception as e:
        # Log any exceptions that occur during the query execution
        logging.error(f"Error executing query: {query}, Error: {str(e)}")
        # Optionally, return a user-friendly message or handle the error appropriately
        return "There was an error processing your SQL query. Please try again."

# Define a tool function for performing web searches
@tool
def browserSearchTool(query: str) -> str:
    """Performs web searches for current events or information outside the LLM's scope of information."""
    return search.run(query)

# List of available tools and their names
tools = [SQLAgentTool, browserSearchTool]
toolNames = ["SQLAgentTool", "searchTool", "getTableINFOforSQL"]

# Initialize memory for conversation history and add initial message for the user
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

MEMORY_KEY = "chat_history"

systemPrompt = "Your name is Hermes. Your primary role is to assist users by providing accurate information about their business or any other topic they might require assistance with."

# Prepare prompt template for conversation
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", systemPrompt),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Bind the tools to the language model
llm_with_tools = llm.bind_tools(tools)
chat_history = []

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True)

#TEST
print(agent_executor.invoke({"input": "how many bar codes are there?", "chat_history": chat_history}))