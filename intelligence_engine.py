import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from cloud_tool import save_to_cloud

# 🔴 HARDCODED KEYS (you asked for it)
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
os.environ["SERPER_API_KEY"] = "YOUR_SERPER_API_KEY"

# --- LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash",
    temperature=0.3
)

search_tool = SerperDevTool()

# --- AGENTS ---
historian = Agent(
    role="Historian",
    goal="Find historical parallels",
    tools=[search_tool],
    llm=llm
)

critic = Agent(
    role="Critic",
    goal="Find flaws in reasoning",
    llm=llm
)

philosopher = Agent(
    role="Writer",
    goal="Write final report and save it",
    tools=[save_to_cloud],
    llm=llm,
    verbose=True
)

# --- MAIN FUNCTION ---
def run_perfected_analysis(topic):
    try:
        t1 = Task(
            description=f"Find historical parallels for {topic}",
            agent=historian
        )

        t2 = Task(
            description="Critically analyze the findings",
            agent=critic,
            context=[t1]
        )

        t3 = Task(
            description=f"Write a 500-700 word report on {topic} and store it",
            agent=philosopher,
            context=[t1, t2]
        )

        crew = Crew(
            agents=[historian, critic, philosopher],
            tasks=[t1, t2, t3],
            process=Process.sequential,
            memory=False
        )

        return crew.kickoff()

    except Exception as e:
        return f"❌ Error: {str(e)}"