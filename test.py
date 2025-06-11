from tools.job_collector_tool import job_collector_tool_func
from tools.trend_analyzer_tool import trend_analyzer_tool_func

jobs = job_collector_tool_func("Python Docker")
print("Matched Jobs:", jobs)

trends = trend_analyzer_tool_func(jobs)
print("Top Skills:", trends)