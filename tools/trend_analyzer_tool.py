from langchain.tools import Tool
from collections import Counter

def trend_analyzer_tool_func(jobs):
    skills = []
    for job in jobs:
        skills.extend(job.get("skills", []))
    return dict(Counter(skills).most_common(10))

trend_analyzer_tool = Tool(
    name="TrendAnalyzer",
    func=trend_analyzer_tool_func,
    description="Analyzes most frequent skills in a list of jobs"
)
