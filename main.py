from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    error = ""
    result = ""
    
    if request.method == 'POST':
        topic = request.form.get('topic', 'test')
        try:
            print(f"🔍 Starting CrewAI for: {topic}")
            from intelligence_engine import run_perfected_analysis
            result = run_perfected_analysis(topic)
            print(f"✅ CrewAI complete: {len(str(result))} chars")
        except Exception as e:
            error = f"CREWAI CRASH: {str(e)}"
            print(f"❌ ERROR: {e}")
    
    return f'''
<html>
<body style="font-family:Arial;margin:50px auto;max-width:1000px;">
<h1>🤖 Debug Intelligence</h1>
<form method="POST">
<input name="topic" placeholder="india vs pakistan" style="width:70%;padding:20px;font-size:18px;">
<input type="submit" value="🔍 RUN CREWAI">
</form>

{"<h2 style='color:red;'>" + error + "</h2>" if error else ""}
<pre style="background:#f0f0f0;padding:20px;">{result}</pre>
</body>
</html>'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)