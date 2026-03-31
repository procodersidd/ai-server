from crewai.tools import tool
from supabase import create_client, Client

@tool("DatabaseWriter")
def save_to_cloud(headline: str, content: str):
    try:
        # 🔴 HARDCODED
        url = "https://wlayjqoaofcwkzavctfh.supabase.co"
        key = "YOUR_SUPABASE_KEY"

        supabase: Client = create_client(url, key)

        data = {
            "headline": headline,
            "report_content": content
        }

        supabase.table("intelligence_reports").insert(data).execute()

        return "Saved to cloud"

    except Exception as e:
        return f"DB Error: {str(e)}"