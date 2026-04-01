from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# ✅ YOUR KEY HARDCODED (works instantly)
genai.configure(api_key="AIzaSyAX008Hp4lj26WUB-FuxDfkwJ6XICJizpk")

HTML = """
<!DOCTYPE html>
<html><head><title>AI Research</title>
<style>body{max-width:800px;margin:50px auto;padding:20px;} input,button{padding:12px;font-size:16px;} #result{background:#f5f5f5;padding:20px;white-space:pre-wrap;}</style></head>
<body><h1>🧠 AI Research Bot</h1><input id="t" placeholder="india pakistan"><button onclick="go()">🔍 Research</button><div id="r"></div>
<script>
async function go(){ 
  const t=document.getElementById('t').value||'news';
  document.getElementById('r').innerHTML='Researching...';
  const r=await fetch('/research',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({topic:t})});
  const d=await r.json();
  document.getElementById('r').innerHTML='<strong>'+d.topic+':</strong>\\n\\n'+d.analysis;
}
</script></body></html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/research', methods=['POST'])
def research():
  try:
    topic = request.json['topic']
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Analyze: {topic}")
    return jsonify({'topic':topic, 'analysis':response.text})
  except Exception as e:
    return jsonify({'error':str(e)}), 500

if __name__=='__main__':
  port=int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port)