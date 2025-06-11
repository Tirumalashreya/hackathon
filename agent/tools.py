agent/tools.py
from langchain_core.tools import tool

@tool
def recommend_courses_tool(goal: str) -> str:
    """
    Recommend relevant courses based on user's career goal.
    """
    if "full stack" in goal.lower():
        return (
            "To become a full stack developer, here are some recommended courses:\n"
            "- HTML, CSS, JavaScript\n"
            "- Front-end frameworks like React or Angular\n"
            "- Back-end frameworks like Node.js or Django\n"
            "- Database management with MySQL or MongoDB\n"
            "- Version control with Git"
        )
    elif "data scientist" in goal.lower():
        return (
            "To become a data scientist, consider courses like:\n"
            "- Python for Data Science\n"
            "- Statistics and Probability\n"
            "- Machine Learning with scikit-learn or TensorFlow\n"
            "- Data Visualization (matplotlib, seaborn)\n"
            "- SQL and Big Data tools"
        )
    else:
        return "Please provide a more specific career goal to get tailored course recommendations."

@tool
def plan_career_path_tool(goal: str) -> str:
    """
    Provide a step-by-step career path plan based on the user's goal.
    """
    return (
        f"Career path for {goal}:\n"
        "- Learn the fundamentals\n"
        "- Build projects\n"
        "- Contribute to open source\n"
        "- Network with professionals\n"
        "- Apply for internships/jobs"
    )

@tool
def build_learning_roadmap_tool(goal: str) -> str:
    """
    Generate a monthly learning roadmap tailored to the career goal.
    """
    return (
        f"Learning roadmap for {goal}:\n"
        "Month 1: Basics and core skills\n"
        "Month 2: Intermediate projects\n"
        "Month 3: Real-world projects & portfolio\n"
        "Month 4+: Job applications and networking"
    )
