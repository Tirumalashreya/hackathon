from langchain.tools import Tool
import json

def job_collector_tool_func(query: str):
    with open("data/jobs_data.json", "r") as f:
        jobs = json.load(f)
    return [job for job in jobs if query.lower() in job['title'].lower()]

job_collector_tool = Tool(
    name="JobCollector",
    func=job_collector_tool_func,
    description="Collects job postings from a local JSON dataset based on a query"
)
