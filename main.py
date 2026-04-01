from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# 🔒 API Key
genai.configure(api_key=os.getenv("AIzaSyAX008Hp4lj26WUB-FuxDfkwJ6XICJizpk"))

# 📱 HTML UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🧠 Geopolitical Research AI</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        input, button { padding: 12px; font-size: 16px; margin: 10px 0; }
        input { width: 70%; }
        button { background: #4285f4; color: white; border: none; cursor: pointer; }
        #result { 
            background: #f5f5f5; padding: 20px; border-radius: 8px; 
            white-space: pre-wrap; line-height: 1.6; margin-top: 20px;
        }
        .loading { color: #666; }
        h1 { color: #4285f4; }
    </style>
</head>
<body>
    <h1>🧠 Geopolitical Research AI</h1>
    <p>Enter any topic → Get 500-word deep analysis with historical context</p>
    
    <input id="topic" placeholder="Ex: US-China trade war 2025, Israel-Palestine, AI regulation..." />
    <button onclick="research()">🔍 Research & Analyze</button>
    
    <div id="result" style="display:none;"></div>
    <div id="loading" class="loading" style="display:none;">🤖 AI researching... (10-30s)</div>

    <script>
        async function research() {
            const topic = document.getElementById('topic').value;
            if (!topic) return alert('Enter a topic!');
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const res = await fetch('/research', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({topic})
                });
                const data = await res.json();
                
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').innerHTML = 
                    `<strong>Topic:</strong> ${data.topic}<br><br>${data.analysis}`;
                document.getElementById('result').style.display = 'block';
            } catch(e) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').innerHTML = 'Error: ' + e;
                document.getElementById('result').style.display = 'block';
            }
        }
        
        // Enter key support
        document.getElementById('topic').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') research();
        });
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/research", methods=["POST"])
def research():
    try:
        data = request.get_json()
        topic = data.get("topic")

        if not topic:
            return jsonify({"error": "No topic provided"}), 400

        # 🧠 ADVANCED RESEARCH PROMPT
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are an elite geopolitical research analyst. RESEARCH MODE ON.

        TOPIC: "{topic}"

        Deliver a COMPREHENSIVE 500-700 word analysis:

        📊 RESEARCH REQUIREMENTS:
        1. Historical context (key events, 3+ examples)
        2. Current status (latest developments)
        3. Key players & motivations
        4. Critical analysis (what mainstream media misses)
        5. 3-5 future scenarios (2025-2030)
        6. Risks & opportunities

        💡 Style: Professional, objective, deeply researched.
        📏 Length: 500-700 words exactly.
        🔗 Cite specific events/dates when possible.

        BEGIN ANALYSIS:
        """

        response = model.generate_content(prompt)

        return jsonify({
            "status": "success",
            "topic": topic,
            "analysis": response.text,
            "tokens": getattr(response, 'usage_metadata', {}).total_token_count or 0,
            "research_time": "10-30 seconds"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)