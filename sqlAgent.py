
import os
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate
from fewShotExamples import fewShot_examples
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from dotenv import load_dotenv
load_dotenv()

# Retrieve API keys from environment variables
myOpenAIkey = os.environ["OPENAI_API_KEY"]
googleSearchKey = os.environ["SERPER_API_KEY"]

#Database INFO
userName = "postgres"
password = "984138o35o"
host = "localhost"
port = "5432"
mydatabase = "awsData"
pg_uri = f"postgresql+psycopg2://{userName}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

#Returns the top 5 similar search results from the examples above - Uses openai embeddings for similarity search
example_selector = SemanticSimilarityExampleSelector.from_examples(
    fewShot_examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)

#System Prompt
system_prefix = """You are an agent designed to interact with a SQL database from a company known as AWS.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

Here are some examples of user inputs and their corresponding SQL queries:"""

#Few-shot prompt for the llm to bring everything together
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
)

#Combines fewshot prompt and to a chatprompttemplate to create a chat agent
full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

#Takes in the full_prompt as prompt to create the agent
sqlAgent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=full_prompt,
    verbose=True,
    agent_type="openai-tools",
    #Can PASS TOOLS HERE IF NEEDED for future iterations
)
