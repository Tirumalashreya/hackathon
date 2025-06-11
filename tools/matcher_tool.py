from langchain.tools import Tool

def matcher_tool_func(input_data):
    jobs = input_data["jobs"]
    skills = input_data["skills"]

    matches = []
    for job in jobs:
        job_skills = set(job.get("skills", []))
        score = len(job_skills.intersection(skills))
        if score > 0:
            matches.append({**job, "match_score": score})
    return sorted(matches, key=lambda x: x["match_score"], reverse=True)

matcher_tool = Tool(
    name="JobMatcher",
    func=matcher_tool_func,
    description="Matches user skills with job requirements and ranks them"
)
