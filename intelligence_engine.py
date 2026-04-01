import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from cloud_tool import save_to_cloud

# 🔴 HARDCODED KEYS (your choice)
os.environ["GOOGLE_API_KEY"] = "AIzaSyAX008Hp4lj26WUB-FuxDfkwJ6XICJizpk"
os.environ["SERPER_API_KEY"] = "533f59ef8613a6d7733b31fafe39310d47a44fc0"

# --- LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash",
    temperature=0.3
)

search_tool = SerperDevTool()

# --- AGENTS ---
historian = Agent(
    role='Lead Historian',
    goal='Find historical parallels.',
    backstory='Expert in long-term historical patterns.',
    tools=[search_tool],
    llm=llm
)

critic = Agent(
    role='Logic Auditor',
    goal='Critique reasoning.',
    backstory='Finds flaws and bias.',
    llm=llm
)

philosopher = Agent(
    role='Intelligence Architect',
    goal='Write final report and save it.',
    backstory='Synthesizes insights.',
    tools=[save_to_cloud],
    llm=llm,
    verbose=True
)

# --- MAIN FUNCTION ---
def run_perfected_analysis(topic):
    try:
        task1 = Task(
            description=f"Research historical roots of '{topic}' with 2 parallels.",
            agent=historian
        )

        task2 = Task(
            description="Critically analyze the report.",
            agent=critic,
            context=[task1]
        )

        task3 = Task(
            description=f"Write final 500-700 word report on '{topic}' and save it.",
            agent=philosopher,
            context=[task1, task2]
        )

        crew = Crew(
            agents=[historian, critic, philosopher],
            tasks=[task1, task2, task3],
            process=Process.sequential,
            memory=False  # important for Vercel
        )

        return crew.kickoff()

    except Exception as e:
        return f"❌ Error: {str(e)}"


# --- LOCAL TEST ---
if __name__ == "__main__":
    query = input("Enter topic: ")
    print(run_perfected_analysis(query))