import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

from tools.job_collector_tool import job_collector_tool
from tools.trend_analyzer_tool import trend_analyzer_tool
from tools.matcher_tool import matcher_tool
from memory import memory

# Load env variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="gemma-2-9b-it"
)

# Register tools
tools = [
    Tool.from_function(
        name=job_collector_tool.name,
        func=job_collector_tool.func,
        description=job_collector_tool.description
    ),
    Tool.from_function(
        name=trend_analyzer_tool.name,
        func=trend_analyzer_tool.func,
        description=trend_analyzer_tool.description
    ),
    Tool.from_function(
        name=matcher_tool.name,
        func=matcher_tool.func,
        description=matcher_tool.description
    )
]

prompt_template = """You are a helpful job research assistant.

You can use the following tools:

{tools}

When given an input question, think step-by-step and decide what to do.
Use this format:

Question: the input question
Thought: you should think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(prompt_template)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)


def run_research_agent(query, skills):
    print("[Research Agent] Running pipeline...")

    jobs = job_collector_tool.func(query)
    trends = trend_analyzer_tool.func(jobs)
    matches = matcher_tool.func({"jobs": jobs, "skills": skills})

    return {
        "trending_skills": trends,
        "matched_jobs": matches
    }


if __name__ == "__main__":
    results = run_research_agent("Machine Learning", ["Python", "SQL", "TensorFlow"])
    print("\nTrending Skills:\n", results["trending_skills"])
    print("\nMatched Jobs:\n", results["matched_jobs"])
