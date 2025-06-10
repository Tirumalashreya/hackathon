from agent.coach_agent import career_coach_agent
from langchain_core.messages import HumanMessage, AIMessage

print("Career Coach Agent is ready! (type 'exit' to quit)")
chat_history = []

while True:
    user_input = input("User: ")  # Added prompt
    if user_input.lower() in {"exit", "quit"}:
        print("Career Coach Agent: Goodbye and best of luck!")
        break

    try:
        result = career_coach_agent.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })
        answer = result.get("output") or result
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))
        print(f"Career Coach Agent: {answer}")
    except Exception as e:
        print(f"❌ Error: {e}")
