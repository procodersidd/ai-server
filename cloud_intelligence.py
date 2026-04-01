from crewai.tools import tool
from supabase import create_client, Client
import os

@tool("DatabaseWriter")
def save_to_cloud(headline: str, content: str):
    """
    Saves geopolitical intelligence report to Supabase.
    """
    try:
        # 🔑 Railway ENV vars
        url = os.getenv("SUPABASE_URL", "https://xicixcsmuivrjzpzgdgf.supabase.co")
        key = os.getenv("SUPABASE_KEY", "sb_secret_N_u1TNBSBKD3PDPDmlGvNQ_xKocV1Iw")
        
        supabase: Client = create_client(url, key)
        
        data = {
            "headline": headline,
            "report_content": content,
            "created_at": "now()"
        }
        
        result = supabase.table("intelligence_reports").insert(data).execute()
        return f"✅ Saved report ID: {result.data[0]['id']}"
        
    except Exception as e:
        return f"❌ DB Error: {str(e)}"